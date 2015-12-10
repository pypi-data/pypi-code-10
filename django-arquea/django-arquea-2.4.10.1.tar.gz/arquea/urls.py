
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

try:
    import ckeditor.urls
    ck = ''
except ImportError:
    ck = '_uploader'


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^files/(?P<filename>.*)', 'utils.views.serve_files'),
    url(r'^protocolo/', include('protocolo.urls')),
    url(r'^patrimonio/', include('patrimonio.urls')),
    url(r'^financeiro/', include('financeiro.urls')),
    url(r'^outorga/', include('outorga.urls')),
    url(r'^memorando/', include('memorando.urls')),
    url(r'^identificacao/', include('identificacao.urls')),
    url(r'^membro/', include('membro.urls')),
    url(r'^rede/', include('rede.urls')),
    url(r'^processo/', include('processo.urls')),
    url(r'^verificacao/', include('verificacao.urls')),
    url(r'^repositorio/', include('repositorio.urls')),
    url(r'^carga/', include('carga.urls')),
    url(r'^configuracao/', include('configuracao.urls')),
    url(r'^verifica$', 'utils.views.verifica'),
    url(r'^sempermissao$', TemplateView.as_view(template_name="401.html")),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^ckeditor/', include('ckeditor%s.urls' % ck)),
    url(r'^', include(admin.site.urls)),
)
        