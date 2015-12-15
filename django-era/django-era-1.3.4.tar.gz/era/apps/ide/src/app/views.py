from era.apps.user.decorators import login_required
from era.views import RedirectView


class IndexView(RedirectView):
    decorators = [login_required]
    permanent = True

    def get_redirect_url(self):
        self.pattern_name = 'users'
        return super().get_redirect_url()
