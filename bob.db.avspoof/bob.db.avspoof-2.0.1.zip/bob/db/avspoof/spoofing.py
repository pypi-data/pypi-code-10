#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 19 Aug 13:43:50 2015

"""AVSpoof database implementation as antispoofing.utils.db.Database"""

from .query import Database as AVSpoofDatabase
import antispoofing.utils
import six


class File(antispoofing.utils.db.File):
    def __init__(self, f):
        """
        Initializes this File object with our own File equivalent
        """

        self.__f = f

    # type object 'File' has no attribute 'audiofile'
    def videofile(self, directory=None):
        return self.__f.audiofile(directory=directory)

    videofile.__doc__ = antispoofing.utils.db.File.videofile.__doc__

    def facefile(self, directory=None):
        return None

    facefile.__doc__ = antispoofing.utils.db.File.facefile.__doc__

    def bbx(self, directory=None):
        return None

    bbx.__doc__ = antispoofing.utils.db.File.bbx.__doc__

    def load(self, directory=None, extension='.hdf5'):
        return self.__f.load(directory=directory, extension=extension)

    load.__doc__ = antispoofing.utils.db.File.load.__doc__

    def save(self, data, directory=None, extension='.hdf5'):
        return self.__f.save(data, directory=directory, extension=extension)

    save.__doc__ = antispoofing.utils.db.File.save.__doc__

    def make_path(self, directory=None, extension=None):
        return self.__f.make_path(directory=directory, extension=extension)

    make_path.__doc__ = antispoofing.utils.db.File.make_path.__doc__

    def get_client_id(self):
        return self.__f.client_id

    get_client_id.__doc__ = antispoofing.utils.db.File.get_client_id.__doc__

    def is_real(self):
        return self.__f.is_real()

    is_real.__doc__ = antispoofing.utils.db.File.is_real.__doc__



class Database(antispoofing.utils.db.Database):
    """ Implements API for antispoofing interface of AVspoof database"""

    def __init__(self, args=None):
        self.__db = AVSpoofDatabase()

        self.__kwargs = {}

        if args is not None:
            self.__kwargs = {
                'protocol': args.avspoof_protocol,
                'support': args.avspoof_support,
                'devices': args.avspoof_devices,
                'attackdevices': args.avspoof_attackdevices,
                'clients': args.avspoof_client if args.avspoof_client else None,
            }

    __init__.__doc__ = antispoofing.utils.db.Database.__init__.__doc__

    def set_kwargs(self, params):
        """
        Set internal __kwargs variable, since it is used as a filter to retrieve data from the database
        :param params: dictionary of pairs {"param":"value"} that are accepted by the database as filters,
        for instance, it can be "protocol":"specific_protocol_name".
        :return: None
        """
        self.__kwargs.update(params)

    def get_protocols(self):
        return [k.name for k in self.__db.protocols()]

    def get_attack_types(self):
        # In the case of this DB, this method does not precisely return the attack types
        return [k.name for k in self.__db.protocols()]

    def create_subparser(self, subparser, entry_point_name):
        from .models import Attack as AVSpoofAttackModel, File as AVSpoofFileModel
        from argparse import RawDescriptionHelpFormatter

        ## remove '.. ' lines from rst
        #    desc = '\n'.join([k for k in self.long_description().split('\n') if k.strip().find('.. ') != 0])

        p = subparser.add_parser(entry_point_name,
                                 help=self.short_description(),
                                 description="temp description",
                                 formatter_class=RawDescriptionHelpFormatter)

        protocols = [k.name for k in self.__db.protocols()]
        p.add_argument('--protocol', type=str, default='grandtest',
                       choices=protocols, dest="avspoof_protocol", nargs='+',
                       help='The protocol type may be specified instead of the the id switch to subselect a smaller number of files to operate on (defaults to "%(default)s")')

        supports = AVSpoofAttackModel.attack_support_choices
        p.add_argument('--support', type=str, dest='avspoof_support', choices=supports,
                       help="If you would like to select a specific support to be used, use this option (if unset, the default, use all)")

        attackdevices = AVSpoofAttackModel.attack_device_choices
        p.add_argument('--attackdevices', type=str, dest='avspoof_attackdevices', choices=attackdevices,
                       help="If you would like to select a specific attack device to be used, use this option (if unset, the default, use all)")

        devices = AVSpoofFileModel.device_choices
        p.add_argument('--device', type=str, choices=devices, dest='avspoof_devices',
                       help="Types of devices used during recording (if unset, the default, use all)")

        identities = [k.id for k in self.__db.clients()]
        p.add_argument('--client', type=int, action='append', choices=identities, dest='avspoof_client',
                       help="Client identifier (if unset, the default, use all)")

        p.set_defaults(name=entry_point_name)
        p.set_defaults(cls=Database)

        return

    create_subparser.__doc__ = antispoofing.utils.db.Database.create_subparser.__doc__

    def name(self):
        from .driver import Interface
        i = Interface()
        return "AVSpoof Database (%s)" % i.name()

    def short_name(self):
        from .driver import Interface
        i = Interface()
        return i.name()

    def version(self):
        from .driver import Interface
        i = Interface()
        return i.version()

    def short_description(self):
        return "Speech spoofing database produced at Idiap, Switzerland"

    short_description.__doc__ = antispoofing.utils.db.Database.short_description.__doc__

    def long_description(self):
        return Database.__doc__

    long_description.__doc__ = antispoofing.utils.db.Database.long_description.__doc__

    def implements_any_of(self, propname):
        if isinstance(propname, (tuple, list)):
            return 'audio' in propname
        elif propname is None:
            return True
        elif isinstance(propname, six.string_types):
            return 'audio' == propname

        # does not implement the given access protocol
        return False

    def get_clients(self, group=None):
        clients = self.__db.clients()
        if group == None:
            return [client.id for client in clients]
        else:
            return [client.id for client in clients if client.set == group]

    def get_data(self, group):
        """Returns either all objects or objects for a specific group"""
        real = dict(self.__kwargs)
        real.update({'groups': group, 'cls': 'real'})
        attack = dict(self.__kwargs)
        attack.update({'groups': group, 'cls': 'attack'})
        return [File(k) for k in self.__db.objects(**real)], \
               [File(k) for k in self.__db.objects(**attack)]

    def get_enroll_data(self, group=None):
        """Returns either all enrollment objects or enrollment objects for a specific group"""
        #    real = dict(self.__kwargs)
        #    real.update({'groups': group, 'cls': 'enroll'})
        #    return [File(k) for k in self.__db.objects(**real)]
        return get_data(group=group)

    def get_train_data(self):
        return self.get_data('train')

    get_train_data.__doc__ = antispoofing.utils.db.Database.get_train_data.__doc__

    def get_devel_data(self):
        return self.get_data('devel')

    get_devel_data.__doc__ = antispoofing.utils.db.Database.get_devel_data.__doc__

    def get_test_data(self):
        return self.get_data('test')

    get_test_data.__doc__ = antispoofing.utils.db.Database.get_test_data.__doc__

    def get_test_filters(self):
        return ('attackdevice', 'support', 'device')

    def get_filtered_test_data(self, filter):

        def device_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        def support_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        def attackdevice_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        def protocol_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        real, attack = self.get_test_data()

        if filter == 'device':
            return {
                'laptop': (
                [k for k in real if device_filter(k, 'laptop')], [k for k in attack if device_filter(k, 'laptop')]),
                'phone1': (
                [k for k in real if device_filter(k, 'phone1')], [k for k in attack if device_filter(k, 'phone1')]),
                'phone2': (
                [k for k in real if device_filter(k, 'phone2')], [k for k in attack if device_filter(k, 'phone2')]),
            }
        elif filter == 'support':
            return {
                'replay': (real, [k for k in attack if support_filter(k, 'replay')]),
                'voice_conversion': (real, [k for k in attack if support_filter(k, 'voice_conversion')]),
                'speech_synthesis': (real, [k for k in attack if support_filter(k, 'speech_synthesis')]),
            }
        elif filter == 'protocol':
            return {
                'grandtest': (real, [k for k in attack if protocol_filter(k, 'grandtest')]),
                'smalltest': (real, [k for k in attack if protocol_filter(k, 'smalltest')]),
                'replay': (real, [k for k in attack if protocol_filter(k, 'replay')]),
            }
        elif filter == 'attackdevice':
            return {
                'laptop': (real, [k for k in attack if attackdevice_filter(k, 'laptop')]),
                'laptop_HQ_speaker': (real, [k for k in attack if attackdevice_filter(k, 'laptop_HQ_speaker')]),
                'phone1': (real, [k for k in attack if attackdevice_filter(k, 'phone1')]),
                'phone1': (real, [k for k in attack if attackdevice_filter(k, 'phone1')]),
                'logical_access': (real, [k for k in attack if attackdevice_filter(k, 'logical_access')]),
                'physical_access_HQ_speaker': (
                real, [k for k in attack if attackdevice_filter(k, 'physical_access_HQ_speaker')]),
                'physical_access': (real, [k for k in attack if attackdevice_filter(k, 'physical_access')]),
            }

    def get_filtered_devel_data(self, filter):

        def device_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        def support_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        def attackdevice_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        def protocol_filter(obj, filter):
            return obj.make_path().find(filter) != -1

        real, attack = self.get_devel_data()

        if filter == 'device':
            return {
                'laptop': (
                [k for k in real if device_filter(k, 'laptop')], [k for k in attack if device_filter(k, 'laptop')]),
                'phone1': (
                [k for k in real if device_filter(k, 'phone1')], [k for k in attack if device_filter(k, 'phone1')]),
                'phone2': (
                [k for k in real if device_filter(k, 'phone2')], [k for k in attack if device_filter(k, 'phone2')]),
            }
        elif filter == 'support':
            return {
                'replay': (real, [k for k in attack if support_filter(k, 'replay')]),
                'voice_conversion': (real, [k for k in attack if support_filter(k, 'voice_conversion')]),
                'speech_synthesis': (real, [k for k in attack if support_filter(k, 'speech_synthesis')]),
            }
        elif filter == 'protocol':
            return {
                'grandtest': (real, [k for k in attack if protocol_filter(k, 'grandtest')]),
                'smalltest': (real, [k for k in attack if protocol_filter(k, 'smalltest')]),
                'replay': (real, [k for k in attack if protocol_filter(k, 'replay')]),
            }
        elif filter == 'attackdevice':
            return {
                'laptop': (real, [k for k in attack if attackdevice_filter(k, 'laptop')]),
                'laptop_HQ_speaker': (real, [k for k in attack if attackdevice_filter(k, 'laptop_HQ_speaker')]),
                'phone1': (real, [k for k in attack if attackdevice_filter(k, 'phone1')]),
                'phone1': (real, [k for k in attack if attackdevice_filter(k, 'phone1')]),
                'logical_access': (real, [k for k in attack if attackdevice_filter(k, 'logical_access')]),
                'physical_access_HQ_speaker': (
                real, [k for k in attack if attackdevice_filter(k, 'physical_access_HQ_speaker')]),
                'physical_access': (real, [k for k in attack if attackdevice_filter(k, 'physical_access')]),
            }

        raise RuntimeError("filter parameter should specify a valid filter among `%s'" % \
                           self.get_test_filters())

    def get_all_data(self):
        return self.get_data(None)

    # get_all_data.__doc__ = DatabaseBase.get_all_data.__doc__
    get_all_data.__doc__ = antispoofing.utils.db.Database.get_all_data.__doc__
