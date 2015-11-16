import mimetypes

from django.views.generic.detail import BaseDetailView

from django.http import HttpResponse
from django.conf import settings

from relatorio.templates.opendocument import Template

from .models import Document

class DocumentFileView(BaseDetailView):

    model = Document

    def get(self, request, *args, **kwargs):
        document = self.get_object()
        obj_id = kwargs.get('object_id')
        document.source.open()

        klass = document.content_type.model_class()
        object = klass.objects.get(pk=obj_id)
        if hasattr(object, 'print_str'):
          object_name = object.print_str()
        else:
          object_name = '{}'.format(object.pk)

        tpl = Template(source=None, filepath=document.source)
        generated = tpl.generate(o=object).render()

        if document.convert_to is None or document.convert_to == '':
          extension = document.source.path.split('.')[-1]

          output = generated.getvalue()

        else:
          extension = document.convert_to

          import subprocess
          import shlex
          import tempfile
          import os

          input = tempfile.NamedTemporaryFile(delete=False)
          input.write(generated.getvalue())
          input.close()

          command_line = '/usr/bin/loffice --headless --convert-to {} --outdir {} {}'.format(extension, os.path.dirname(input.name), input.name)
          subprocess.call(shlex.split(command_line))

          output_filename = '{}.{}'.format(input.name, extension)
          if document.merge_with_tos and extension == 'pdf':
            final_name = os.path.join('/tmp','{}_{}.{}'.format(document.name, object_name, extension))
            command_line = 'pdfunite {} {} {}'.format(output_filename, settings.TOS_FILE, final_name)
            print(command_line)
            subprocess.call(shlex.split(command_line))
            os.unlink(output_filename)
            output_filename = final_name

          output_stream = open(output_filename, 'rb')
          output = output_stream.read()
          os.unlink(input.name)
          os.unlink(output_filename)


        type = mimetypes.guess_type('brol.{}'.format(extension))
        rv = HttpResponse(output, content_type=type[0])
        rv['Content-Disposition'] = 'attachment; filename={}_{}.{}'.format(document.name, object_name, extension)

        return rv
