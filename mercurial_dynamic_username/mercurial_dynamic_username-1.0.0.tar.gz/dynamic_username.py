


def extsetup(ui):
    ui.warn("""Dynamic Username is not working!
Extension module was renamed from dynamic_username to mercurial_dynamic_username.
Please update your ~/.hgrc (or mercurial.ini) to:
    [extensions]
    mercurial_dynamic_username =
or (if you specify full path)
    [extensions]
    mercurial_dynamic_username = path/to/mercurial_dynamic_username.py

""")


