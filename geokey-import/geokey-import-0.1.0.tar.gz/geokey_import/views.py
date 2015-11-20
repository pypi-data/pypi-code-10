from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages

from braces.views import LoginRequiredMixin

from geokey.core.decorators import handle_exceptions_for_admin
from geokey.categories.models import Field
from geokey.contributions.models import Observation
from geokey.projects.models import Project
from geokey.projects.views import ProjectContext

from .models import DataImport
from .utils import csv_parser, category
from .exceptions import DataImportError


class ImportIndex(LoginRequiredMixin, TemplateView):
    template_name = 'import_index.html'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        projects = Project.objects.get_list(user).filter(admins=user)
        imports = DataImport.objects.filter(project=projects)

        incomplete = []

        for data_import in imports:
            to_review = data_import.project.observations.filter(
                    status='pending', id__in=data_import.imported).count()
            if to_review > 0:
                data_import.to_review = to_review
                incomplete.append(data_import)

        return super(ImportIndex, self).get_context_data(
            imports=incomplete,
            *args,
            **kwargs
        )


class ImportNew(LoginRequiredMixin, TemplateView):
    template_name = 'import_new.html'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        projects = Project.objects.get_list(user).filter(admins=user)
        return super(ImportNew, self).get_context_data(
            projects=projects,
            *args,
            **kwargs
        )


class ImportUpload(LoginRequiredMixin, ProjectContext, TemplateView):
    template_name = 'upload.html'

    def post(self, request, project_id):
        context = self.get_context_data(project_id)

        if context.get('project'):
            the_file = self.request.FILES.get('csv')

            category = None
            geometry_field = self.request.POST.get('geometry_field')
            redirect_url = 'geokey_import:import_createcategory'

            if self.request.POST.get('create_category') == 'false':
                category_id = self.request.POST.get('category')
                category = context['project'].categories.get(pk=category_id)
                redirect_url = 'geokey_import:import_existingcategory'

            import_object = DataImport.objects.create(
                csv_file=the_file,
                project=context['project'],
                category=category,
                geom_field=geometry_field
            )

            return redirect(
                redirect_url,
                import_id=import_object.id
            )

        return self.render_to_response(context)


class DataImportContext(object):
    @handle_exceptions_for_admin
    def get_context_data(self, import_id, *args, **kwargs):
        import_obj = DataImport.objects.get(pk=import_id)

        if import_obj.project.is_admin(self.request.user):
            return super(DataImportContext, self).get_context_data(
                data_import=import_obj,
                *args,
                **kwargs
            )
        else:
            return {
                'error_description': 'Project matching query does not exist.',
                'error': 'Not found.'
            }


class ImportCreateCategory(
        LoginRequiredMixin, DataImportContext, TemplateView):
    template_name = 'create_category.html'

    def get_context_data(self, import_id, *args, **kwargs):
        context = super(ImportCreateCategory, self).get_context_data(
            import_id,
            *args,
            **kwargs
        )

        if context.get('data_import'):
            context['csv_fields'] = csv_parser.get_fields(
                context['data_import'].csv_file.path)

            context['field_types'] = Field.get_field_types()

        return context

    def post(self, request, import_id):
        context = self.get_context_data(import_id)

        if context.get('data_import'):
            data_import = context.get('data_import')

            category_created, fields = category.create(
                data_import.project,
                request.user,
                request.POST
            )

            data_import.category = category_created
            data_import.fields = fields
            data_import.save()

            try:
                data_import.import_csv(request.user)
            except DataImportError, e:
                messages.error(request, e.to_html())
                return redirect(
                    'geokey_import:import_error',
                    import_id=data_import.id
                )
            else:
                return redirect(
                    'geokey_import:import_done',
                    import_id=data_import.id
                )

        return self.render_to_response(context)


class ImportExistingCategory(
        LoginRequiredMixin, DataImportContext, TemplateView):
    template_name = 'existing_category.html'

    def get_context_data(self, import_id, *args, **kwargs):
        context = super(ImportExistingCategory, self).get_context_data(
            import_id,
            *args,
            **kwargs
        )

        if context.get('data_import'):
            context['csv_fields'] = csv_parser.get_fields(
                context['data_import'].csv_file.path)

        return context

    def post(self, request, import_id):
        context = self.get_context_data(import_id)

        if context.get('data_import'):
            data_import = context.get('data_import')

            data_import.fields = category.get_field_order(self.request.POST)
            data_import.save()

            try:
                data_import.import_csv(request.user)
            except DataImportError, e:
                messages.error(request, e.to_html())
                return redirect(
                    'geokey_import:import_error',
                    import_id=data_import.id
                )
            else:
                return redirect(
                    'geokey_import:import_done',
                    import_id=data_import.id
                )

        return self.render_to_response(context)


class ImportFailed(LoginRequiredMixin, DataImportContext, TemplateView):
    template_name = 'import_error.html'

    def post(self, request, import_id):
        context = self.get_context_data(import_id)

        if context.get('data_import'):
            data_import = context.get('data_import')
            the_file = self.request.FILES.get('csv')

            data_import.csv_file = the_file
            data_import.save()

            try:
                data_import.import_csv(request.user)
            except DataImportError, e:
                messages.error(request, e.to_html())
                return redirect(
                    'geokey_import:import_error',
                    import_id=data_import.id
                )
            else:
                return redirect(
                    'geokey_import:import_done',
                    import_id=data_import.id
                )

        return self.render_to_response(context)


class ImportPending(LoginRequiredMixin, DataImportContext, TemplateView):
    template_name = 'pending_contributions.html'

    def get_context_data(self, import_id, *args, **kwargs):
        context = super(ImportPending, self).get_context_data(
            import_id,
            *args,
            **kwargs
        )

        if context.get('data_import'):
            data_import = context.get('data_import')
            context['pending_contributions'] = data_import.project.observations.filter(
                status='pending',
                id__in=data_import.imported
            )

        return context

    def get(self, request, import_id):
        context = self.get_context_data(import_id)

        if context.get('data_import'):
            if context['pending_contributions'].count() < 0:
                return redirect(
                    'geokey_import:index'
                )

        return self.render_to_response(context)

    def post(self, request, import_id):
        context = self.get_context_data(import_id)

        if context.get('data_import'):
            approve = request.POST.getlist('approve')
            to_approve = Observation.objects.filter(id__in=approve)
            to_approve.update(status='active')

            messages.success(
                self.request,
                '%s contributions have been approved.' % len(approve)
            )

            if not Observation.objects.filter(
                    status='pending',
                    id__in=context['data_import'].imported).exists():

                return redirect(
                    'geokey_import:index'
                )

        return self.render_to_response(context)


class ImportReview(LoginRequiredMixin, DataImportContext, TemplateView):
    template_name = 'review.html'

    @handle_exceptions_for_admin
    def get_context_data(self, import_id, observation_id, *args, **kwargs):
        context = super(ImportReview, self).get_context_data(
            import_id,
            *args,
            **kwargs
        )

        if context.get('data_import'):
            data_import = context['data_import']
            observation = data_import.project.observations.get(pk=observation_id)
            context['observation'] = observation

        return context

    def post(self, request, import_id, observation_id):
        context = self.get_context_data(import_id, observation_id)

        if context.get('observation'):
            data = self.request.POST.dict()
            observation = context['observation']

            location = observation.location
            location.geometry = GEOSGeometry(data.pop('location'))
            location.save()

            observation.properties = data
            observation.status = 'active'
            observation.save()

            messages.success(self.request, 'The contribution has been approved.')

            return redirect(
                'geokey_import:import_done',
                import_id=context['data_import'].id
            )

        return self.render_to_response(context)
