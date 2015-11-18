#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import threading

import pushi
import appier

from . import base

class Provision(base.DRBase):

    pid = appier.field(
        index = True,
        immutable = True,
        default = True
    )

    ptype = appier.field(
        index = True
    )

    pstatus = appier.field()

    droplet_id = appier.field(
        type = int,
        index = True,
        immutable = True
    )

    droplet_address = appier.field(
        index = True,
        immutable = True
    )

    url = appier.field(
        index = True,
        immutable = True
    )

    force = appier.field(
        type = bool,
        index = True,
        immutable = True
    )

    names = appier.field(
        type = list,
        immutable = True
    )

    values = appier.field(
        type = list,
        immutable = True
    )

    config = appier.field(
        type = list,
        immutable = True
    )

    log = appier.field(
        type = list
    )

    @classmethod
    def validate(cls):
        return super(Provision, cls).validate() + [
            appier.not_null("pid"),
            appier.not_empty("pid"),

            appier.not_null("droplet_id"),

            appier.not_null("droplet_address"),
            appier.not_empty("droplet_address"),

            appier.not_null("url"),
            appier.not_empty("url"),
            appier.is_url("url"),

            appier.not_null("force")
        ]

    @classmethod
    def list_names(cls):
        return ["id", "created", "pid", "droplet_id"]

    def pre_validate(self):
        base.DRBase.pre_validate(self)
        if self.is_new(): self.pid = str(uuid.uuid4())
        is_valid = hasattr(self, "names") and hasattr(self, "values")
        if not is_valid: self.names = self.values = []

    def pre_save(self):
        base.DRBase.pre_save(self)
        self.split_config()
        self.join_config()

    def post_create(self):
        base.DRBase.post_create(self)
        method = getattr(self, self.ptype)
        thread = threading.Thread(target = method)
        thread.start()

    def split_config(self):
        if not hasattr(self, "config") or not self.config: return
        if hasattr(self, "names") and self.names: return
        if hasattr(self, "values") and self.values: return
        self.names, self.values = zip(*self.config)

    def join_config(self):
        if hasattr(self, "config") and self.config: return self.config
        self.config = zip(self.names, self.values)
        return self.config

    def extra_config(self):
        instance = self.get_instance()
        self.join_config()
        config = list(self.config)
        for name, value in instance.config:
            if name in self.names: continue
            config.append([name, value])
        return config

    @appier.operation(name = "Deploy")
    def deploy(self):
        self.start()
        try:
            logger = self.create_logger()
            deployer = self.owner.get_deployer(
                address = self.droplet_address,
                username = "root",
                provision = self
            )
            deployer.bind("stdout", logger)
            deployer.bind("deployed", self.mark)
            deployer.deploy_url(
                self.url,
                force = self.force
            )
        except: self.cancel(); raise
        else: self.finish()

    @appier.operation(name = "Undeploy")
    def undeploy(self):
        self.start()
        try:
            logger = self.create_logger()
            deployer = self.owner.get_deployer(
                address = self.droplet_address,
                username = "root",
                provision = self
            )
            deployer.bind("stdout", logger)
            deployer.bind("undeployed", self.unmark)
            deployer.undeploy_url(
                self.url,
                force = self.force
            )
        except: self.cancel(); raise
        else: self.finish()

    @appier.operation(name = "Re-Deploy")
    def redeploy(self):
        self.start()
        try:
            logger = self.create_logger()
            deployer = self.owner.get_deployer(
                address = self.droplet_address,
                username = "root",
                provision = self
            )
            deployer.bind("stdout", logger)
            deployer.bind("deployed", self.mark)
            deployer.bind("undeployed", self.unmark)
            deployer.undeploy_url(
                self.url,
                force = self.force
            )
            deployer.instance = self.get_instance()
            deployer.deploy_url(
                self.url,
                force = self.force
            )
        except: self.cancel(); raise
        else: self.finish()

    def mark(self, url, data = None):
        instance = self.get_instance()
        if instance.has_feature(url): return
        instance.add_feature(
            url,
            name = instance.fname(url),
            data = data,
            config = self.join_config()
        )
        instance.save()

    def unmark(self, url, data = None):
        instance = self.get_instance()
        if not instance.has_feature(url): return
        instance.remove_feature(url)
        instance.save()

    def create_logger(self):
        data_logger = self.create_data()
        pushi_logger = self.create_pushi()

        def logger(message):
            data_logger(message)
            pushi_logger(message)

        return logger

    def create_data(self):

        def logger(message):
            provision = Provision.get(pid = self.pid)
            provision.log.append(message)
            provision.save()

        return logger

    def create_pushi(self):

        def on_connect(connection):
            connection.subscribe_pushi(self.pid)

        client_key = appier.conf("PUSHI_KEY")
        client = pushi.PushiClient(client_key = client_key)
        connection = client.connect_pushi(callback = on_connect)

        def logger(message):
            connection.send_channel("stdout", message, self.pid, persist = False)

        return logger

    def start(self):
        self.set_status("started")

    def stop(self):
        self.set_status("stopped")

    def finish(self):
        self.set_status("finished")

    def cancel(self):
        self.set_status("canceled")

    def set_status(self, value, reload = True):
        self = self.reload() if reload else self
        self.pstatus = value
        self.save()

    def get_name(self, url = None):
        url = url or self.url
        return url.rsplit("/", 2)[1]

    def get_instance(self):
        from . import instance
        instance = instance.Instance.by_id(self.droplet_id)
        return instance
