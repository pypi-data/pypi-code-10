from django.http import Http404
from taiga.base import filters
from taiga.base.api import ModelCrudViewSet
from taiga.base.decorators import list_route
from taiga.base.api.utils import get_object_or_404
from taiga.projects.models import Project

from .models import IframePlugin
from .serializers import IframePluginSerializer
from .permissions import IframePluginPermissions


class IframePluginViewSet(ModelCrudViewSet):
    model = IframePlugin
    serializer_class = IframePluginSerializer
    permission_classes = (IframePluginPermissions,)
    filter_backends = (filters.IsProjectAdminFilterBackend,)
    filter_fields = ("project", "slug")

    @list_route(methods=["GET"])
    def by_slug(self, request):
        iframe_slug = request.QUERY_PARAMS.get("slug", None)
        project_slug = request.QUERY_PARAMS.get("pslug", None)
        if iframe_slug and project_slug:
            iframe = get_object_or_404(IframePlugin, slug=iframe_slug,
                                       project__slug=project_slug)
            return self.retrieve(request, pk=iframe.pk)
        if project_slug:  # no iframe slug, return iframes for this project
            project = get_object_or_404(Project, slug=project_slug)
            self.queryset = IframePlugin.objects.filter(
                project__slug=project.slug)
            return self.list(IframePlugin, request)
        raise Http404(self.empty_error)
