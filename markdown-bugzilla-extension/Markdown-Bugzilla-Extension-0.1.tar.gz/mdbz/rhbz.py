from extension import BugzillaExtension, BugzillaPattern

class RedHatBugzillaExtension(BugzillaExtension):
    def __init__(self, *args, **kwargs):
        kwargs["bugzillaURL"] = "https://bugzilla.redhat.com/show_bug.cgi?id=%s"
        BugzillaExtension.__init__(self, *args, **kwargs)


    def extendMarkdown(self, md, md_globals):
        self.add_inline(md, "rhbz", BugzillaPattern)


def makeExtension(*args, **kwargs):
    return RedHatBugzillaExtension(*args, **kwargs)
