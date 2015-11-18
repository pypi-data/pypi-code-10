#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

import appier

try: import paramiko
except: paramiko = None

class Deployer(appier.Observable):
    """
    Base deployer class responsible for the deploying operations
    under the Torus infra-structure. It's design should respect
    a modular design so that it may be used in multiple back-ends.
    """

    CONFIG_FILE = "config.env"
    """ The name of the file that is going to be used to store the
    bash related variable exporting, to be used during runtime """

    DATA_DIRECTORY = "/data"
    """ The directory where all the ephemeral/persistent data will
    be stored and it's considered the state of the machine """

    BASE_DIRECTORY = "/torus"
    """ The base directory where the instance configuration of the
    torus infra-structure will be positioned for execution """

    TEMP_DIRECTORY = "/tmp/torus"
    """ The temporary directory that is going to be used in the
    build process and any other ephemeral operations """

    BASE_PACKAGES = ("python", "python-dev", "ruby", "nodejs")
    """ Sequence containing the various packages that are considered
    to be foundation and that should always be installed """

    def __init__(
        self,
        address = None,
        username = None,
        password = None,
        id_rsa_path = None,
        provision = None,
        instance = None,
        environment = None,
        config_file = None,
        data_directory = None,
        base_directory = None,
        temp_directory = None,
        base_packages = None
    ):
        appier.Observable.__init__(self)
        cls = self.__class__
        self.address = appier.conf("DR_ADDRESS", None)
        self.username = appier.conf("DR_USERNAME", None)
        self.password = appier.conf("DR_PASSWORD", None)
        self.id_rsa_path = appier.conf("DR_KEY_PATH", None)
        self.address = address or self.address
        self.username = username or self.username
        self.password = password or self.password
        self.id_rsa_path = id_rsa_path or self.id_rsa_path
        self.provision = provision or None
        self.instance = instance or (self.provision.get_instance() if
            self.provision else None)
        self.environment = environment or (self.provision.extra_config() if
            self.provision else [])
        self.config_file = config_file or cls.CONFIG_FILE
        self.data_directory = data_directory or cls.DATA_DIRECTORY
        self.base_directory = base_directory or cls.BASE_DIRECTORY
        self.temp_directory = temp_directory or cls.TEMP_DIRECTORY
        self.base_packages = base_packages or cls.BASE_PACKAGES
        self.ssh = None
        self.sftp = None

    def deploy_url(self, url, force = False):
        data = appier.get(url)
        is_dict = type(data) == dict

        if not is_dict:
            data = data.decode("utf-8")
            data = json.loads(data)

        self.deploy_torus(url, data, force = force)

    def deploy_torus(self, url, data, force = False):
        skip = self.instance.has_provision(url) and not force
        if skip: self.trigger("stdout", "Skipped '%s'" % url); return

        build = data.get("build", None)
        build = self._to_absolute(url, build)
        dependencies = data.get("depends", [])

        for dependency in dependencies:
            dependency = self._to_absolute(url, dependency)
            if self.instance.has_provision(dependency): continue
            self.deploy_url(dependency)

        self.build_all(data = data)
        build and self.run_script(build, env = True)
        self.close_ssh()

        self.trigger("deployed", url, data = data)

    def undeploy_url(self, url, force = False):
        data = appier.get(url)
        is_dict = type(data) == dict

        if not is_dict:
            data = data.decode("utf-8")
            data = json.loads(data)

        self.undeploy_torus(url, data, force = force)

    def undeploy_torus(self, url, data, force = False):
        skip = not self.instance.has_provision(url)
        if skip: self.trigger("stdout", "Skipped '%s'" % url); return

        destroy = data.get("destroy", None)
        destroy = self._to_absolute(url, destroy)

        self.destroy_feature()
        destroy and self.run_script(destroy, env = True)
        self.close_ssh()

        self.trigger("undeployed", url, data = data)

    def sync_torus(self):
        self.build_base()
        self.build_exec()
        self.build_config()

    def start_torus(self, url, data):
        start = data.get("start", None)
        if not start: return
        self.run_command(start)

    def stop_torus(self, url, data):
        stop = data.get("stop", None)
        if not stop: return
        self.run_command(stop)

    def has_base(self):
        return self.run_command(
            "ls %s" % self.base_directory,
            output = False,
            raise_e = False
        ) == 0

    def build_all(self, data = None):
        self.build_base()
        self.build_exec()
        self.build_config()
        self.build_feature(data = data)

    def build_base(self):
        if self.has_base(): return
        base_path = "%s/%s" % (self.base_directory, self.config_file)
        data_path = "%s/%s" % (self.data_directory, self.config_file)
        base_s = " ".join(self.base_packages)
        self.run_command("mkdir -p %s" % self.base_directory)
        self.run_command("mkdir -p %s" % self.data_directory)
        self.run_command("ln -s %s %s" % (base_path, data_path))
        self.run_command("apt-get update")
        self.run_command("apt-get -y install %s" % base_s)

    def build_exec(self):
        base_path = os.path.dirname(__file__)
        scripts_path = os.path.join(base_path, "scripts")
        start_path = "%s/%s" % (self.base_directory, "start.sh")
        exec_s = "#!/bin/sh -e\n%s\nexit 0" % start_path
        self.run_command("echo \"%s\" > /etc/rc.local" % exec_s)
        self.copy_directory(scripts_path, self.base_directory)
        self.run_command("chmod +x %s/*.sh" % self.base_directory)

    def build_config(self):
        items = self.instance.config
        config_path = "%s/%s" % (self.base_directory, self.config_file)
        config_s = "\\n".join(["export " + key + "=\\${" + key + "-" + value + "}" for key, value in items])
        self.run_command("printf \"%s\" > %s" % (config_s, config_path))

    def build_feature(self, data = None):
        name = self.provision.get_name()
        items = self.provision.join_config()
        provision_directory = "%s/features/%s" % (self.base_directory, name)
        config_path = "%s/%s" % (provision_directory, self.config_file)
        start_path = "%s/%s" % (provision_directory, "start.sh")
        stop_path = "%s/%s" % (provision_directory, "stop.sh")
        torus_path = "%s/%s" % (provision_directory, "torus.json")
        config_s = "\\n".join(["export " + key + "=\\${" + key + "-" + value + "}" for key, value in items])
        self.run_command("rm -rf %s && mkdir -p %s" % (provision_directory, provision_directory))
        self.run_command("printf \"%s\" > %s" % (config_s, config_path))
        if not data: return
        start_s = data.get("start", "")
        stop_s = data.get("stop", "")
        data_s = json.dumps(data)
        self.run_command("cat > %s << \"EOF\"\n%s\nEOF\n" % (torus_path, data_s))
        self.run_command("cat > %s << \"EOF\"\n%s\nEOF\n" % (start_path, start_s))
        self.run_command("cat > %s << \"EOF\"\n%s\nEOF\n" % (stop_path, stop_s))
        self.run_command("chmod +x %s" % start_path)
        self.run_command("chmod +x %s" % stop_path)

    def destroy_feature(self):
        name = self.provision.get_name()
        provision_directory = "%s/features/%s" % (self.base_directory, name)
        self.run_command("rm -rf %s" % provision_directory)

    def run_script(self, url, env = False):
        name = url.rsplit("/", 1)[1]
        self.run_command("rm -rf %s && mkdir -p %s" % (self.temp_directory, self.temp_directory))
        self.run_command("cd %s && wget %s" % (self.temp_directory, url))
        self.run_command("cd %s && chmod +x %s && ./%s" % (self.temp_directory, name, name), env = env)
        self.run_command("rm -rf %s" % self.temp_directory)

    def run_command(
        self,
        command,
        env = False,
        output = True,
        timeout = None,
        bufsize = -1,
        raise_e = True
    ):
        # builds the prefix string containing the various environment
        # variables for the execution so that the command runs in context
        prefix = " ".join([key + "=\"" + value + "\"" for key, value in self.environment])
        if not env: prefix = ""

        # retrieves the reference to the current ssh connection and
        # then creates a new channel stream for command execution
        ssh = self.get_ssh()
        transport = ssh.get_transport()
        channel = transport.open_session()

        try:
            # sets the proper timeout for the connection and then combines
            # both the stdout and the stderr into the same channel, after
            # that creates two files for the operation and executes the
            # command itself around the provided buffer
            channel.settimeout(timeout)
            channel.set_combine_stderr(True)
            _stdin = channel.makefile("wb", bufsize)
            stdout = channel.makefile("r", bufsize)
            channel.exec_command(prefix + " $SHELL -c '" + command + "'")

            while True:
                data = stdout.readline()
                if not data: break
                if not output: continue
                sys.stdout.write(data)
                sys.stdout.flush()
                self.trigger("stdout", data)

            code = channel.recv_exit_status()
        except:
            channel.close()

        if code == 0 or not raise_e: return code
        raise RuntimeError("invalid return code '%d' in command execution '%s'" % (code, command))

    def copy_directory(self, local_path, remote_path):
        names = os.listdir(local_path)
        for name in names:
            _local_path = os.path.join(local_path, name)
            _remote_path = "%s/%s" % (remote_path, name)
            self.copy_file(_local_path, _remote_path)

    def copy_file(self, local_path, remote_path, replace = True, sftp = None):
        owner = sftp == None
        sftp = sftp or self.get_sftp()
        try:
            exists = self.exists_file(remote_path, sftp = sftp)
            if exists and replace: sftp.remove(remote_path)
            sftp.put(local_path, remote_path)
        finally:
            owner and self.close_sftp()

    def exists_file(self, remote_path, sftp = None):
        owner = sftp == None
        sftp = sftp or self.get_sftp()
        try: sftp.stat(remote_path)
        except IOError: return False
        finally: owner and self.close_sftp()
        return True

    def get_ssh(self, force = False):
        # in case the ssh connection already exists and no
        # forced is ensured, returns the current connection
        if self.ssh and not force: return self.ssh

        # creates the proper ssh client with the remote host
        # adding the proper policies and then runs the connection
        # with the provided credentials and key file values
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            self.address,
            username = self.username,
            password = self.password,
            key_filename = self.id_rsa_path
        )
        return self.ssh

    def close_ssh(self):
        if not self.ssh: return
        self.ssh.close()
        self.ssh = None

    def get_sftp(self, force = False):
        if self.sftp and not force: return self.sftp
        ssh = self.get_ssh(force = force)
        self.sftp = ssh.open_sftp()
        return self.sftp

    def close_sftp(self):
        if not self.sftp: return
        self.sftp.close()
        self.sftp = None

    def _to_absolute(self, base, url):
        if not base: return url
        if not url: return url
        is_absolute = url.startswith("http://") or url.startswith("https://")
        if is_absolute: return url
        base = base.rsplit("/", 1)[0]
        return base + "/" + url
