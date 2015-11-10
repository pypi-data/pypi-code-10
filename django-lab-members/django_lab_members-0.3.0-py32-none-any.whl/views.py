from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from lab_members.models import Scientist

class ScientistListView(ListView):
    model = Scientist

    def get_context_data(self, **kwargs):
        context = super(ScientistListView, self).get_context_data(**kwargs)
        context['current_list'] = Scientist.objects.filter(current=True, visible=True)
        context['alumni_list'] = Scientist.objects.filter(current=False, visible=True)
        context['request'] = self.request
        return context

    def render_to_response(self, context, **response_kwargs):
        # Shim to affect the CMS Toolbar only
        if ('cms_lab_members' in settings.INSTALLED_APPS and self.request.toolbar):

            menu = self.request.toolbar.get_or_create_menu('lab-members-list-menu', 'Lab Members')

            url_change = reverse('admin:lab_members_scientist_changelist')
            url_addnew = reverse('admin:lab_members_scientist_add')
            menu.add_sideframe_item(u'Edit Scientists', url=url_change)
            menu.add_modal_item('Add New Scientist', url=url_addnew)
            menu.add_break()

            url_change = reverse('admin:lab_members_position_changelist')
            url_addnew = reverse('admin:lab_members_position_add')
            menu.add_sideframe_item(u'Edit Positions', url=url_change)
            menu.add_modal_item('Add New Position', url=url_addnew)
            menu.add_break()

            url_change = reverse('admin:lab_members_institution_changelist')
            url_addnew = reverse('admin:lab_members_institution_add')
            menu.add_sideframe_item(u'Edit Institutions', url=url_change)
            menu.add_modal_item('Add New Institution', url=url_addnew)
            menu.add_break()

            url_change = reverse('admin:lab_members_field_changelist')
            url_addnew = reverse('admin:lab_members_field_add')
            menu.add_sideframe_item(u'Edit Fields of Study', url=url_change)
            menu.add_modal_item('Add New Field of Study', url=url_addnew)
            menu.add_break()

            url_change = reverse('admin:lab_members_degree_changelist')
            url_addnew = reverse('admin:lab_members_degree_add')
            menu.add_sideframe_item(u'Edit Degrees', url=url_change)
            menu.add_modal_item('Add New Degree', url=url_addnew)
            menu.add_break()

            url_change = reverse('admin:lab_members_advisor_changelist')
            url_addnew = reverse('admin:lab_members_advisor_add')
            menu.add_sideframe_item(u'Edit Advisors', url=url_change)
            menu.add_modal_item('Add New Advisor', url=url_addnew)

            context['CMS'] = True

        return super(ScientistListView, self).render_to_response(context, **response_kwargs)


class ScientistDetailView(DetailView):
    queryset = Scientist.objects.filter(visible=True)

    def get_context_data(self, **kwargs):
        context = super(ScientistDetailView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def render_to_response(self, context, **response_kwargs):
        # Shim to affect the CMS Toolbar and CMS PlaceholderField
        if ('cms_lab_members' in settings.INSTALLED_APPS and self.request.toolbar):

            menu = self.request.toolbar.get_or_create_menu('lab-members-detail-menu', self.object.full_name)

            url_change = reverse('admin:lab_members_scientist_change', args=[self.object.id])
            url_delete = reverse('admin:lab_members_scientist_delete', args=[self.object.id])
            menu.add_modal_item('Edit %s' % self.object.full_name, url=url_change)
            menu.add_modal_item('Delete %s' % self.object.full_name, url=url_delete)
            menu.add_break()

            url_change = reverse('admin:lab_members_scientist_changelist')
            url_addnew = reverse('admin:lab_members_scientist_add')
            menu.add_sideframe_item(u'Edit Scientists', url=url_change)
            menu.add_modal_item('Add New Scientist', url=url_addnew)

            context['CMS'] = True

        return super(ScientistDetailView, self).render_to_response(context, **response_kwargs)
