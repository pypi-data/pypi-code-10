#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import appier

import digitalriver

class DropletController(appier.Controller):

    @appier.route("/droplets", "GET")
    @appier.ensure("base")
    def list(self):
        return self.template(
            "droplet/list.html.tpl",
            link = "droplets"
        )

    @appier.route("/droplets.json", "GET", json = True)
    @appier.ensure("base")
    def list_json(self):
        api = self.get_api()
        start = self.field("start_record", 0, cast = int)
        count = self.field("number_records", 10, cast = int)
        droplets = api.list_droplets()
        droplets = droplets["droplets"][start:start + count]
        return droplets

    @appier.route("/droplets/<int:id>", "GET")
    @appier.ensure("base")
    def show(self, id):
        instance = self._ensure(id)
        is_url = type(instance) == str
        if is_url: return self.redirect(instance)
        return self.template(
            "droplet/show.html.tpl",
            link = "droplets",
            sub_link = "info",
            droplet = instance.droplet,
            instance = instance
        )

    @appier.route("/droplets/<int:id>/features", "GET")
    @appier.ensure("base")
    def features(self, id):
        instance = digitalriver.Instance.by_id(id)
        return self.template(
            "droplet/features.html.tpl",
            link = "droplets",
            sub_link = "features",
            droplet = instance.droplet,
            instance = instance
        )

    @appier.route("/droplets/<int:id>/config", "GET")
    @appier.ensure("base")
    def config(self, id):
        instance = digitalriver.Instance.by_id(id)
        return self.template(
            "droplet/config.html.tpl",
            link = "droplets",
            sub_link = "config",
            droplet = instance.droplet,
            instance = instance,
            errors = {}
        )

    @appier.route("/droplets/<int:id>/config", "POST")
    @appier.ensure("base")
    def do_config(self, id):
        instance = digitalriver.Instance.by_id(id)
        instance.apply()
        try: instance.save()
        except appier.ValidationError as error:
            return self.template(
                "droplet/config.html.tpl",
                link = "droplets",
                sub_link = "config",
                droplet = error.model.droplet,
                instance = error.model,
                errors = error.errors
            )
        return self.redirect(
            self.url_for("droplet.show", id = id)
        )

    @appier.route("/droplets/<int:id>/provision", "GET")
    @appier.ensure("base")
    def new_provision(self, id):
        instance = digitalriver.Instance.by_id(id)
        return self.template(
            "droplet/provision.html.tpl",
            link = "droplets",
            sub_link = "provision",
            droplet = instance.droplet,
            provision = {},
            errors = {}
        )

    @appier.route("/droplets/<int:id>/provision", "POST")
    @appier.ensure("base")
    def create_provision(self, id):
        provision = digitalriver.Provision.new()
        try: provision.save()
        except appier.ValidationError as error:
            instance = digitalriver.Instance.by_id(id)
            return self.template(
                "droplet/provision.html.tpl",
                link = "droplets",
                sub_link = "provision",
                droplet = instance.droplet,
                provision = error.model,
                errors = error.errors
            )
        return self.redirect(
            self.url_for("provision.log", pid = provision.pid)
        )

    @appier.route("/droplets/<int:id>/feature/delete", "GET")
    @appier.ensure("base")
    def remove_feature(self, id):
        feature = self.field("feature", mandatory = True)
        instance = digitalriver.Instance.by_id(id)
        droplet = instance.droplet
        provision = digitalriver.Provision.new()
        provision.ptype = "undeploy"
        provision.droplet_id = droplet["id"]
        provision.droplet_address = instance.address
        provision.url = feature
        provision.save()
        return self.redirect(
            self.url_for("provision.log", pid = provision.pid)
        )

    @appier.route("/droplets/<int:id>/feature/rebuild", "GET")
    @appier.ensure("base")
    def rebuild_feature(self, id):
        url = self.field("feature", mandatory = True)
        instance = digitalriver.Instance.by_id(id)
        droplet = instance.droplet
        feature = instance.get_feature(url)
        config = feature.config
        provision = digitalriver.Provision.new()
        provision.ptype = "redeploy"
        provision.droplet_id = droplet["id"]
        provision.droplet_address = instance.address
        provision.url = url
        provision.config = config
        provision.save()
        return self.redirect(
            self.url_for("provision.log", pid = provision.pid)
        )

    @appier.route("/droplets/<int:id>/sync", "GET")
    @appier.ensure("base")
    def sync(self, id):
        self._ensure(id, force = True)
        instance = digitalriver.Instance.by_id(id)
        instance.sync()
        return self.redirect(
            self.url_for(
                "droplet.show",
                id = id,
                message = "Sync successful"
            )
        )

    @appier.route("/droplets/<int:id>/process", "GET")
    @appier.ensure("base")
    def process(self, id):
        url = self.field("url", mandatory = True)
        info = appier.get(url)
        if not type(info) == dict:
            info = info.decode("utf-8")
            info = json.loads(info)
        return info

    def _ensure(self, id, force = False):
        instance = digitalriver.Instance.by_id(id)
        use_cached = hasattr(instance, "id") and not force
        if use_cached: return instance
        api = self.get_api()
        droplet = api.get_droplet(id)
        instance = digitalriver.Instance.ensure(droplet)
        return instance
