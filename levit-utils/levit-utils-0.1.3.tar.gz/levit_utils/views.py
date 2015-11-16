from django.views.generic import View, TemplateResponseMixin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredView(View):

  @method_decorator(login_required())
  def dispatch(self, request, *args, **kwargs):
    return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


class AjaxResponseMixin(TemplateResponseMixin):

  html_template_name = None
  ajax_template_name = None

  def get_template_names(self):
    if self.ajax_template_name is None or self.html_template_name is None:
      raise ImproperlyConfigured(
        "AjaxResponseMixin requires either a definition of "
        "'html_template_name' and 'ajax_template_name' or an implementation of 'get_template_names()'")
    if self.request.is_ajax():
      return [self.ajax_template_name]
    else:
      return [self.html_template_name]

