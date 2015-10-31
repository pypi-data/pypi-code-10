from itertools import chain

from django.http import HttpResponse

from .models import Group, Human, OtherPeople, Person

def humanstxt(request):
    html = ""
    groups = list(Group.objects.all())
    groups.insert(0, None)

    for group in groups:
        if group:
            html += '/* {} */\n\n'.format(group.name.upper())

        persons = list(chain(OtherPeople.objects.filter(group=group), Human.objects.filter(group=group)))
        persons = sorted(persons, key=lambda p: p.order)

        for person in persons:
            if hasattr(person, 'first_name'):
                html += '\t{role}: {first_name} {last_name}\n'.format(role=person.role, first_name=person.first_name, last_name=person.last_name)

                if person.email:
                    html += '\tContact: {email}\n'.format(email=person.email_safe())

                for extra in person.extras.all():
                    html += '\t{field}: {value}'.format(field=extra.field_name, value=extra.value)

                if person.location:
                    html += '\tFrom: {location}\n'.format(location=person.location)

            else:
                html += '\t{text}\n'.format(text=person.text)
                for extra in person.extras.all():
                    html += '\t{field}: {value}\n'.format(field=extra.field_name, value=extra.value)

            html += '\n'
        html += '\n'

    return HttpResponse(html, content_type="text/plain; charset=utf-8")
