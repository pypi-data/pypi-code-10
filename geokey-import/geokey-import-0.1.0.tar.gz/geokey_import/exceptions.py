from django.utils.safestring import mark_safe


class DataImportError(Exception):
    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

    def to_html(self):
        html = ('<p>The import failed because the CSV contains invalid data. '
                'Please update the CSV and upload the file again. </p>')
        html += '<ul>'
        for e in self.errors:
            html += '<li>Line: %s</li>' % e.get('line')

            for m in e.get('messages'):
                html += '<ul>'
                html += '<li>%s</li>' % m
                html += '</ul>'

        html += '</ul>'
        return mark_safe(html)
