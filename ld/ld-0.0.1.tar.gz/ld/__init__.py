# /etc/issue
# uname -mrs
# /etc/system-release

import os
import re
import constants as const


class LinuxDistribution(object):
    def __init__(self):
        self._os_release_info = self.os_release_info()
        self._lsb_release_info = self.lsb_release_info()
        self._distro_release_info = {}
        self.set_distribution_properties()

    def os_release_info(self):
        if os.path.isfile(const.OS_RELEASE):
            with open(const.OS_RELEASE, 'r') as f:
                return self._parse_os_release_file(f)

    def lsb_release_info(self):
        if os.path.isfile(const.LSB_RELEASE):
            with open(const.LSB_RELEASE, 'r') as f:
                return self._parse_lsb_release_file(f)

    def distro_release_info(self, release_file):
        if os.path.isfile(release_file):
            with open(release_file, 'r') as f:
                return self._parse_distro_specific_release_file(f.read())

    def get_distro_release_attr(self, attribute):
        return self._distro_release_info.get(attribute)

    def get_os_release_attr(self, attribute):
        return self._os_release_info.get(attribute)

    def get_lsb_release_attr(self, attribute):
        return self._lsb_release_info.get(attribute)

    def id(self):
        return self.get_os_release_attr('id') or self.dist

    def name(self, pretty=False):
        if pretty:
            dist = self.get_os_release_attr('pretty')
        else:
            dist = self.get_os_release_attr('name')
        return dist

    def version(self, full=False):
        if full:
            version = self.get_os_release_attr('version')
        else:
            version = self.get_os_release_attr('version_id')
        return version or self.ver

    def like(self):
        return self.get_os_release_attr('id_like')

    def codename(self):
        return self.code

    def family(self):
        return const.DIST_TO_FAMILY.get(self.name(), self.like())

    def linux_distribution(self, full_distribution_name=False):
        return (
            self.name() if full_distribution_name else self.id(),
            self.version(),
            self.codename()
        )

    def _parse_lsb_release_file(self, content):
        return self._parse_files(content)

    def _parse_os_release_file(self, content):
        return self._parse_files(content)

    def _parse_distro_specific_release_file(self, content):
        return self._parse_release_file(content)

    @staticmethod
    def _parse_files(content):
        os_release_info = {}
        for l in content:
            if '=' in l:
                k, v = l.split('=')
                os_release_info[k.lower()] = v.replace('"', '').rstrip('\n\r')
        return os_release_info

    @staticmethod
    def _parse_release_file(content):
        version = re.search(r'(\d+.\d+)(.\d+)?', content)
        codename = re.search(r'\(\w+\)', content)
        distro_release_info = {
            'version': version.group() if version else None,
            'codename': codename.group().strip('()') if codename else None
        }
        return distro_release_info

    def set_distribution_properties(self):
        self.code = None

        if os.path.isfile(const.ORACLE_RELEASE):
            self._distro_release_info = \
                self.distro_release_info(const.ORACLE_RELEASE)
            self.dist = 'oracle'
            self.ver = self.get_distro_release_attr('version')
        elif os.path.isfile(const.ORACLE_RELEASE):
            self._distro_release_info = \
                self.distro_release_info(const.ORACLE_RELEASE)
            self.dist = 'oracle'
            self.ver = self.get_distro_release_attr('version')
        elif os.path.isfile(const.CENTOS_RELEASE):
            self._distro_release_info = \
                self.distro_release_info(const.CENTOS_RELEASE)
            self.dist = 'centos'
            self.ver = self.get_distro_release_attr('version')
            self.code = self.get_distro_release_attr('codename')
        elif os.path.isfile('/etc/fedora-release'):
            self._distro_release_info = \
                self.distro_release_info('/etc/fedora-release')
            self.dist = 'fedora'
            self.ver = self.get_distro_release_attr('version')
            self.code = self.get_distro_release_attr('codename')
        elif os.path.isfile(const.REDHAT_RELEASE):
            self._distro_release_info = \
                self.distro_release_info(const.REDHAT_RELEASE)
            self.dist = 'redhat'
            self.ver = self.get_distro_release_attr('version')
            self.code = self.get_distro_release_attr('codename')

        elif os.path.isfile(const.ARCH_RELEASE):
            self._distro_release_info = \
                self.distro_release_info(const.ARCH_RELEASE)
            self.dist = 'arch'
            self.ver = self.get_distro_release_attr('version')
        elif os.path.isfile(const.SUSE_RELEASE):
            with open(const.SUSE_RELEASE, 'r') as f:
                if re.search('opensuse', f.read()):
                    self.dist = 'opensuse'
                else:
                    self.dist = 'suse'
                self.ver = self.get_distro_release_attr('version')
        elif os.path.isfile(const.SLACKWARE_VERSION):
            self._distro_release_info = \
                self.distro_release_info(const.SLACKWARE_VERSION)
            self.dist = 'slackware'
            self.ver = self.get_distro_release_attr('version')
        elif os.path.isfile(const.EXHERBO_RELEASE):
            self.dist = 'exherbo'
            self.ver = None
        elif os.path.isfile(const.DEBIAN_VERSION):
            dist = self.get_lsb_release_attr('distrib_id').lower()
            if dist:
                self.dist = dist
                self.ver = self.get_lsb_release_attr(
                    'distrib_release').lower()
                self.code = self.get_lsb_release_attr(
                    'distrib_codename').lower()
            else:
                if os.path.isfile('/usr/bin/raspi-config'):
                    self.dist = 'raspbian'
                else:
                    self._distro_release_info = \
                        self.distro_release_info(const.DEBIAN_VERSION)
                    self.dist = 'debian'
                self.ver = self.get_distro_release_attr('version')
        elif os.path.isfile(const.PARALLELS_RELEASE):
            self._distro_release_info = \
                self.distro_release_info(const.PARALLELS_RELEASE)
            self.dist = 'parallels'
            self.ver = self.get_distro_release_attr('version')


ld = LinuxDistribution()


def id():
    return ld.id()


def name(pretty=False):
    return ld.name(pretty)


def version(full=False):
    return ld.version(full)


def like():
    return ld.like()


def codename():
    return ld.codename()


def family():
    return ld.family()


def linux_distribution(full_distribution_name=False):
    return ld.linux_distribution(full_distribution_name)
