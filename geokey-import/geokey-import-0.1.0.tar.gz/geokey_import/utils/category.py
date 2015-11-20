from django.template.defaultfilters import slugify

from geokey.categories.models import Category, Field


def create(project, user, input_dict):
    fields = []

    category = Category.objects.create(
        name=input_dict.get('name'),
        description=input_dict.get('description'),
        project=project,
        creator=user
    )

    for key in sorted(input_dict):
        if key.startswith('field'):
            order = key[key.find('_'):]
            field_type = input_dict.get('type' + order)
            imp = input_dict.get('import' + order)

            if imp == 'true':
                field = Field.create(
                    input_dict.get(key),
                    slugify(input_dict.get(key)),
                    '',
                    False,
                    category,
                    field_type
                )

                fields.append(field.key)
            else:
                fields.append('-1')

    return category, fields


def get_field_order(input_dict):
    count = 0
    read_more_fields = True
    fields = []
    field_dict = {
        key: input_dict[key]
        for key in input_dict
        if key.startswith('field_')
    }

    while read_more_fields:
        count += 1
        field = field_dict.get('field_' + str(count).zfill(2))

        if field:
            fields.append(field)
        else:
            fields.append('-1')

        read_more_fields = len(field_dict) > (len(fields) - fields.count('-1'))

    return fields
