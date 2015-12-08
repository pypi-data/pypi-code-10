# -*- coding: utf-8 -*-
from collections import defaultdict

from django.core.management.base import NoArgsCommand

from aldryn_forms.models import FormData, FormPlugin


class Command(NoArgsCommand):
    help = 'Prints out corruptions in aldryn_forms.FormData records.'

    def handle_noargs(self, **options):
        ignored_forms = []
        bad_forms = defaultdict(lambda: defaultdict(list))
        submissions_by_form_name = defaultdict(list)

        for form_submission in FormData.objects.iterator():
            submissions_by_form_name[form_submission.name].append(form_submission)

        for form_name in submissions_by_form_name:
            submissions = submissions_by_form_name[form_name]

            forms = FormPlugin.objects.filter(name=form_name)
            known_field_labels = []

            if forms.exists():
                for form in forms.iterator():
                    try:
                        fields = form.get_form_fields()
                    except KeyError:
                        import ipdb;ipdb.set_trace()
                    known_field_labels.extend(field.label for field in fields)

                known_field_labels = frozenset(known_field_labels)

                for submission in submissions:
                    data = submission.get_data()
                    field_labels = [field.label for field in data]
                    missing_field_labels = (
                        label for label in field_labels
                        if not label in known_field_labels
                    )
                    for field_label in missing_field_labels:
                        bad_forms[form_name][field_label].append(unicode(submission.pk))
            else:
                # Form is no longer available
                # we can't do any verification without the form.
                ignored_forms.append(form_name)

        if bad_forms:
            for form, fields in bad_forms.items():
                self.stdout.write(u"Form %s has %s corrupt field labels:\n" % (form, len(fields)))

                for field, ids in fields.items():
                    self.stdout.write(u"Field %s found in form data ids %s \n" % (field, ', '.join(ids)))

                self.stdout.write('\n')

        if ignored_forms:
            form_txt = '\n'.join(ignored_forms)
            self.stdout.write(u"Ignoring all submissions for forms:\n")
            self.stdout.write(form_txt)
