


def extsetup(ui):
    ui.warn("""Path Pattern is not working!
Extension module was renamed from path_pattern to mercurial_path_pattern.
Please update your ~/.hgrc (or mercurial.ini) to:
    [extensions]
    mercurial_path_pattern =
or (if you specify full path)
    [extensions]
    mercurial_path_pattern = path/to/mercurial_path_pattern.py

""")


