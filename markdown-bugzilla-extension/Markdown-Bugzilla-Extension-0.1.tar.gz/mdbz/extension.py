import re
from markdown import util, Extension
from markdown.inlinepatterns import Pattern

class BugzillaExtensionException(Exception):
    pass

class BugzillaExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "bugzillaURL"  : [ "%s", "Bugzilla URL to use, e.g. http://bugzilla.redhat.com/%s, default None" ],
        }

        for key, value in kwargs.items():
            if (key == "bugzillaURL") and (value.count('%s') != 1):
                raise BugzillaExtensionException("Invalid format string '" + value + "' ! ONE %s needed")

        Extension.__init__(self, *args, **kwargs)

    def add_inline(self, md, name, pattern_class):
        pattern = r'\[(?P<prefix>%s#)(?P<bug_number>\d+)\]' % name
        objPattern = pattern_class(pattern, self.config)
        objPattern.md = md
        objPattern.ext = self
        md.inlinePatterns.add(name, objPattern, "<reference")

    def extendMarkdown(self, md, md_globals):
        self.add_inline(md, "bz", BugzillaPattern)


class BugzillaPattern(Pattern):
    def __init__(self, pattern, config):
        Pattern.__init__(self, pattern)
        self.config = config

    def getCompiledRegExp(self):
        return re.compile("^(.*?)%s(.*)$" % self.pattern, re.DOTALL | re.UNICODE | re.IGNORECASE)

    def handleMatch(self, match):
        if match :
            bug_number = match.group('bug_number')
            bug_url = self.config['bugzillaURL'][0] % bug_number

            element = util.etree.Element('a')
            element.set("href", bug_url )
            element.text = match.group('prefix') + bug_number

            return element
        else:
            return ""


def makeExtension(*args, **kwargs):
    return BugzillaExtension(*args, **kwargs)
