# coding: utf-8
import logging
import os
import sys
import time
from os.path import join

import django.dispatch
import ijson
from dateutil.parser import parse as date_parse
from django.db import transaction
from django.utils.timezone import make_aware as date_make_aware
from pytz import timezone as date_timezone

from representatives.models import Representative
from representatives_votes.models import Dossier, Proposal, Vote


logger = logging.getLogger(__name__)
vote_pre_import = django.dispatch.Signal(providing_args=['vote_data'])



def _parse_date(date_str):
    return date_make_aware(
        date_parse(date_str),
        date_timezone('Europe/Brussels'))

JSON_URL = 'http://parltrack.euwiki.org/dumps/ep_votes.json.xz'
DESTINATION = join('/tmp', 'ep_votes.json')


class Command(object):
    def init_cache(self):
        self.cache = dict()
        self.index_representatives()
        self.index_dossiers()

    def manage_vote(self, vote_data):
        self._travis()

        proposal = self.parse_vote_data(vote_data)

        return proposal

    def parse_vote_data(self, vote_data):
        """
        Parse data from parltrack votes db dumps (1 proposal)
        """
        if 'epref' not in vote_data.keys():
            logger.debug('Could not import data without epref %s', vote_data)
            return

        dossier_pk = self.get_dossier(vote_data['epref'])

        if not dossier_pk:
            logger.debug('Cannot find dossier with remote id %s',
                         vote_data['epref'])
            return

        return self.parse_proposal_data(
            proposal_data=vote_data,
            dossier_pk=dossier_pk
        )

    @transaction.atomic
    def parse_proposal_data(self, proposal_data, dossier_pk):
        """Get or Create a proposal model from raw data"""
        proposal_display = '{} ({})'.format(proposal_data['title'].encode(
            'utf-8'), proposal_data.get('report', '').encode('utf-8'))

        if 'issue_type' not in proposal_data.keys():
            logger.debug('This proposal data without issue_type: %s',
                         proposal_data['epref'])
            return

        changed = False
        try:
            proposal = Proposal.objects.get(
                dossier_id=dossier_pk,
                reference=proposal_data.get('report'),
                kind=proposal_data.get('issue_type'))
        except Proposal.DoesNotExist:
            proposal = Proposal(dossier_id=dossier_pk,
                                reference=proposal_data.get('report'),
                                kind=proposal_data.get('issue_type'))
            changed = True

        data_map = dict(
            title=proposal_data['title'],
            datetime=_parse_date(proposal_data['ts']),
        )

        for position in ('For', 'Abstain', 'Against'):
            position_data = proposal_data.get(position, {})
            position_total = position_data.get('total', 0)

            if isinstance(position_total, str) and position_total.isdigit():
                position_total = int(position_total)

            data_map['total_%s' % position.lower()] = position_total

        for key, value in data_map.items():
            if value != getattr(proposal, key, None):
                setattr(proposal, key, value)
                changed = True

        if changed:
            proposal.save()

        responses = vote_pre_import.send(sender=self, vote_data=proposal_data)

        for receiver, response in responses:
            if response is False:
                logger.debug(
                    'Skipping dossier %s', proposal_data.get(
                        'epref', proposal_data['title']))
                return

        votes = proposal.votes.all() if proposal.pk else []

        positions = ['For', 'Abstain', 'Against']
        logger.info(
            'Looking for votes in proposal {}'.format(proposal_display))
        for position in positions:
            for group_vote_data in proposal_data.get(
                    position,
                    {}).get(
                    'groups',
                    {}):
                for vote_data in group_vote_data['votes']:
                    if not isinstance(vote_data, dict):
                        logger.error('Skipping vote data %s for proposal %s',
                                     vote_data, proposal_data['_id'])
                        continue

                    representative_pk = self.get_representative(vote_data)

                    if representative_pk is None:
                        logger.error('Could not find mep for %s', vote_data)
                        continue

                    representative_name = vote_data.get('orig', '')

                    found = False
                    for vote in votes:
                        if representative_pk is None:
                            continue

                        if representative_pk == vote.representative_id:
                            found = True
                            break

                        elif vote.representative_name == representative_name:
                            found = True
                            break

                    changed = False
                    if not found:
                        vote = Vote(proposal_id=proposal.pk,
                                    representative_id=representative_pk,
                                    representative_name=representative_name)

                        changed = True

                    if vote.position != position.lower():
                        changed = True
                        vote.position = position.lower()

                    if changed:
                        vote.save()

        return proposal

    def index_dossiers(self):
        self.cache['dossiers'] = {
            d[0]: d[1] for d in Dossier.objects.values_list('reference', 'pk')
        }

    def get_dossier(self, reference):
        return self.cache['dossiers'].get(reference, None)

    def index_representatives(self):
        self.cache['meps'] = {int(l[0]): l[1] for l in
            Representative.objects.values_list('remote_id', 'pk')}

    def get_representative(self, vote_data):
        if vote_data.get('ep_id', None) is None:
            return
        return self.cache['meps'].get(int(vote_data['ep_id']), None)

    def _travis(self):
        """ Avoid being killed after 10 minutes without output """
        if not os.environ.get('TRAVIS', False):
            return

        now = time.time()
        last_output = getattr(self, '_travis_last_output', None)

        if last_output is None or now - last_output >= 530:
            print('Do not kill me !')
            self._travis_last_output = now


def parltrack_import_votes():
    import django
    django.setup()

    command = Command()
    command.init_cache()

    i = 0
    for vote_data in ijson.items(sys.stdin, 'item'):
        i += 1
        command.manage_vote(vote_data)
