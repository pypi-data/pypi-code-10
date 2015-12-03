
def extsetup(ui):
    ui.warn("""Update Version is not working!
Extension module was renamed from update_version to mercurial_update_version.
Please update your ~/.hgrc (or mercurial.ini) to:
    [extensions]
    mercurial_update_version =
or (if you specify full path)
    [extensions]
    mercurial_update_version = path/to/mercurial_update_version.py

""")


