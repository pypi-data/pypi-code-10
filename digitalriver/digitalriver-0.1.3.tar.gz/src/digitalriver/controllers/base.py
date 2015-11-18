#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import appier

class BaseController(appier.Controller):

    @appier.route("/", "GET")
    @appier.route("/index", "GET")
    @appier.ensure("base")
    def index(self):
        return self.template(
            "index.html.tpl",
            link = "home"
        )

    @appier.route("/signin", "GET")
    def signin(self):
        next = self.field("next")
        return self.template(
            "signin.html.tpl",
            next = next
        )

    @appier.route("/signin_do", "GET")
    def do_login(self):
        next = self.field("next")
        url = self.ensure_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
            next or self.url_for("base.index")
        )

    @appier.route("/logout", "GET")
    def logout(self):
        next = self.field("next")
        self.reset_session()
        return self.redirect(
            next or self.url_for("base.index")
        )

    @appier.route("/about", "GET")
    @appier.ensure("base")
    def about(self):
        return self.template(
            "about.html.tpl",
            link = "about"
        )

    @appier.route("/oauth", "GET")
    def oauth(self):
        code = self.field("code")
        state = self.field("state")
        api = self.get_api()
        access_token = api.oauth_access(code)
        self.session["do.access_token"] = access_token
        self.session["username"] = api.email
        self.session["tokens"] = ("base",)
        return self.redirect(
            state or self.url_for("base.index"),
        )

    @appier.route("/deploy", ("GET", "POST"))
    @appier.ensure("base")
    def deploy(self):
        api = self.get_api()
        droplet = dict(
            name = self.field("name", "digitalriver"),
            region = self.field("region", "ams1"),
            size = self.field("size", "512mb"),
            image = self.field("image", "ubuntu-14-04-x64"),
            ssh_keys = self.field("ssh_keys", None),
            backups = self.field("backups", False, cast = bool),
            ipv6 = self.field("ipv6", False, cast = bool),
            private_networking = self.field("private_networking", None),
            user_data = self.field("user_data", None)
        )
        droplet = api.create_droplet(droplet)

        links = droplet.get("links", {})
        actions = links.get("actions", [])
        action_id = actions[0]["id"]

        while True:
            action = api.get_action(action_id)
            status = action["status"]
            if status == "completed": break
            print("waiting for complete")
            time.sleep(1.0)

        droplet = droplet["droplet"]
        droplet_id = droplet["id"]
        droplet = api.get_droplet(droplet_id)

        return self.redirect(
            self.url_for("base.index")
        )
