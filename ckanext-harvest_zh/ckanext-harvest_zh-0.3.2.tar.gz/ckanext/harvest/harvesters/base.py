import logging
import re
import uuid

from sqlalchemy.sql import update,and_, bindparam
from sqlalchemy.exc import InvalidRequestError
from pylons import config

from ckan import plugins as p
from ckan import model
from ckan.model import Session, Package
from ckan.logic import ValidationError, NotFound, get_action

from ckan.logic.schema import default_create_package_schema
from ckan.lib.navl.validators import ignore_missing,ignore
from ckan.lib.munge import munge_title_to_name,substitute_ascii_equivalents

from ckanext.harvest.model import HarvestJob, HarvestObject, HarvestGatherError, \
                                    HarvestObjectError

from ckan.plugins.core import SingletonPlugin, implements
from ckan.plugins.toolkit import get_converter

from ckanext.harvest.interfaces import IHarvester


log = logging.getLogger(__name__)


def munge_tag(tag):
    tag = substitute_ascii_equivalents(tag)
    tag = tag.lower().strip()
    return re.sub(r'[^a-zA-Z0-9 -]', '', tag).replace(' ', '-')


class HarvesterBase(SingletonPlugin):
    '''
    Generic class for  harvesters with helper functions
    '''
    implements(IHarvester)

    config = None

    _user_name = None

    def _gen_new_name(self, title):
        '''
        Creates a URL friendly name from a title

        If the name already exists, it will add some random characters at the end
        '''

        name = munge_title_to_name(title).replace('_', '-')
        while '--' in name:
            name = name.replace('--', '-')
        pkg_obj = Session.query(Package).filter(Package.name == name).first()
        if pkg_obj:
            return name + str(uuid.uuid4())[:5]
        else:
            return name


    def _save_gather_error(self, message, job):
        err = HarvestGatherError(message=message, job=job)
        try:
            err.save()
        except InvalidRequestError:
            Session.rollback()
            err.save()
        finally:
            log.error(message)


    def _save_object_error(self, message, obj, stage=u'Fetch', line=None):
        err = HarvestObjectError(message=message,
                                 object=obj,
                                 stage=stage,
                                 line=line)
        try:
            err.save()
        except InvalidRequestError, e:
            Session.rollback()
            err.save()
        finally:
            log_message = '{0}, line {1}'.format(message,line) if line else message
            log.debug(log_message)

    def _get_user_name(self):
        '''
        Returns the name of the user that will perform the harvesting actions
        (deleting, updating and creating datasets)

        By default this will be the old 'harvest' user to maintain
        compatibility. If not present, the internal site admin user will be
        used. This is the recommended setting, but if necessary it can be
        overridden with the `ckanext.harvest.user_name` config option:

           ckanext.harvest.user_name = harvest

        '''
        if self._user_name:
            return self._user_name

        config_user_name = config.get('ckanext.harvest.user_name')
        if config_user_name:
            self._user_name = config_user_name
            return self._user_name

        context = {'model': model,
                   'ignore_auth': True,
                   }

        # Check if 'harvest' user exists and if is a sysadmin
        try:
            user_harvest = p.toolkit.get_action('user_show')(
                context, {'id': 'harvest'})
            if user_harvest['sysadmin']:
                self._user_name = 'harvest'
                return self._user_name
        except p.toolkit.ObjectNotFound:
            pass

        context['defer_commit'] = True  # See ckan/ckan#1714
        self._site_user = p.toolkit.get_action('get_site_user')(context, {})
        self._user_name = self._site_user['name']

        return self._user_name

    def _create_harvest_objects(self, remote_ids, harvest_job):
        '''
        Given a list of remote ids and a Harvest Job, create as many Harvest Objects and
        return a list of their ids to be passed to the fetch stage.

        TODO: Not sure it is worth keeping this function
        '''
        try:
            object_ids = []
            if len(remote_ids):
                for remote_id in remote_ids:
                    # Create a new HarvestObject for this identifier
                    obj = HarvestObject(guid = remote_id, job = harvest_job)
                    obj.save()
                    object_ids.append(obj.id)
                return object_ids
            else:
               self._save_gather_error('No remote datasets could be identified', harvest_job)
        except Exception, e:
            self._save_gather_error('%r' % e.message, harvest_job)


    def _create_or_update_package(self, package_dict, harvest_object):
        '''
        Creates a new package or updates an exisiting one according to the
        package dictionary provided. The package dictionary should look like
        the REST API response for a package:

        http://ckan.net/api/rest/package/statistics-catalunya

        Note that the package_dict must contain an id, which will be used to
        check if the package needs to be created or updated (use the remote
        dataset id).

        If the remote server provides the modification date of the remote
        package, add it to package_dict['metadata_modified'].


        TODO: Not sure it is worth keeping this function. If useful it should
        use the output of package_show logic function (maybe keeping support
        for rest api based dicts
        '''
        try:
            # Change default schema
            schema = default_create_package_schema()
            schema['id'] = [ignore_missing, unicode]
            schema['__junk'] = [ignore]
            schema['resources']['field_names'] = [ignore_missing, unicode]

            # Check API version
            if self.config:
                try:
                    api_version = int(self.config.get('api_version', 2))
                except ValueError:
                    raise ValueError('api_version must be an integer')
            else:
                api_version = 2

            user_name = self._get_user_name()
            context = {
                'model': model,
                'session': Session,
                'user': user_name,
                'api_version': api_version,
                'schema': schema,
                'ignore_auth': True,
            }

            if self.config and self.config.get('clean_tags', False):
                tags = package_dict.get('tags', [])
                tags = [munge_tag(t) for t in tags if munge_tag(t) != '']
                tags = list(set(tags))
                package_dict['tags'] = tags

            # Check if package exists
            data_dict = {}
            data_dict['id'] = package_dict['id']
            try:
                existing_package_dict = get_action('package_show')(context, data_dict)

                # In case name has been modified when first importing. See issue #101.
                package_dict['name'] = existing_package_dict['name']

                # Check modified date
                if not 'metadata_modified' in package_dict or \
                   package_dict['metadata_modified'] > existing_package_dict.get('metadata_modified'):
                    log.info('Package with GUID %s exists and needs to be updated' % harvest_object.guid)
                    # Update package
                    context.update({'id':package_dict['id']})
                    package_dict.setdefault('name',
                            existing_package_dict['name'])
                    new_package = get_action('package_update_rest')(context, package_dict)

                else:
                    log.info('Package with GUID %s not updated, skipping...' % harvest_object.guid)
                    return

                # Flag the other objects linking to this package as not current anymore
                from ckanext.harvest.model import harvest_object_table
                conn = Session.connection()
                u = update(harvest_object_table) \
                        .where(harvest_object_table.c.package_id==bindparam('b_package_id')) \
                        .values(current=False)
                conn.execute(u, b_package_id=new_package['id'])

                # Flag this as the current harvest object

                harvest_object.package_id = new_package['id']
                harvest_object.current = True
                harvest_object.save()

            except NotFound:
                # Package needs to be created

                # Get rid of auth audit on the context otherwise we'll get an
                # exception
                context.pop('__auth_audit', None)

                # Set name for new package to prevent name conflict, see issue #117
                if package_dict.get('name', None):
                    package_dict['name'] = self._gen_new_name(package_dict['name'])
                else:
                    package_dict['name'] = self._gen_new_name(package_dict['title'])

                log.info('Package with GUID %s does not exist, let\'s create it' % harvest_object.guid)
                harvest_object.current = True
                harvest_object.package_id = package_dict['id']
                # Defer constraints and flush so the dataset can be indexed with
                # the harvest object id (on the after_show hook from the harvester
                # plugin)
                harvest_object.add()

                model.Session.execute('SET CONSTRAINTS harvest_object_package_id_fkey DEFERRED')
                model.Session.flush()

                new_package = get_action('package_create_rest')(context, package_dict)

            Session.commit()

            return True

        except ValidationError,e:
            log.exception(e)
            self._save_object_error('Invalid package with GUID %s: %r'%(harvest_object.guid,e.error_dict),harvest_object,'Import')
        except Exception, e:
            log.exception(e)
            self._save_object_error('%r'%e,harvest_object,'Import')

        return None
