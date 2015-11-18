#!/usr/bin/python
# -*- coding: utf-8 -*-

import digitalocean

import appier
import appier_extras

class DigitalriverApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(
            self,
            name = "digitalriver",
            parts = (
                appier_extras.AdminPart,
            )
        )
        self.theme = "modern"
        self.style = "romantic"
        self.libs = "current"
        self.login_route = "base.signin"

    @appier.exception_handler(appier.OAuthAccessError)
    def oauth_error(self, error):
        self.reset_session()
        return self.redirect(
            self.url_for("base.index")
        )

    def reset_session(self):
        if "do.access_token" in self.session: del self.session["do.access_token"]
        if "username" in self.session: del self.session["username"]
        if "tokens" in self.session: del self.session["tokens"]

    def ensure_api(self, state = None):
        access_token = self.session.get("do.access_token", None)
        if access_token: return
        api = self._get_api()
        return api.oauth_authorize(state = state)

    def get_api(self):
        access_token = self.session and self.session.get("do.access_token", None)
        api = self._get_api()
        api.access_token = access_token
        return api

    def get_deployer(self, *args, **kwargs):
        import digitalriver.util
        return digitalriver.util.Deployer(*args, **kwargs)

    def _get_api(self):
        return digitalocean.Api(
            client_id = appier.conf("DO_ID"),
            client_secret = appier.conf("DO_SECRET"),
            redirect_url = appier.conf("DO_REDIRECT_URL")
        )

if __name__ == "__main__":
    app = DigitalriverApp()
    app.serve()
