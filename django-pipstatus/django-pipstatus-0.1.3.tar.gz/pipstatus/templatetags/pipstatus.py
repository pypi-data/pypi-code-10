import pip
from collections import namedtuple

from django import template

register = template.Library()

PipEntry = namedtuple('PipEntry', ['name', 'version', 'available', 'dependencies'])
# I don't know if this is a good idea, but it works fine.
PipEntry.outdated = lambda self: self.version != self.available


class PipStatus(template.Node):
    def __init__(self):
        self.entries = []
        # workaround to avoid error of uninitialized var
        pip.utils.logging._log_state.indentation = 0
        # Getting the pip command 'list'
        c = pip.commands.list.ListCommand()
        # Getting some basic args
        o = c.parse_args([])
        for package, y, unused in c.find_packages_latest_versions(o[0]):
            x = PipEntry(name=package.key,
                         version=package.version,
                         available=y.public,
                         dependencies=[str(i) for i in package.requires()])
            self.entries.append(x)

    @property
    def outdated(self):
        # check if ALL packages are outdated
        return reduce(lambda x, y: x or y, [i.version == i.available for i in self.entries], True)


@register.assignment_tag()
def get_pipstatus():
    return PipStatus()
