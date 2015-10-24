from flask import flash, redirect

def flashy(msg, etype="danger", path="/"):
    """
    Flashes a message and redirects a user. Returns a flask Response that can
    be returned to the user.
    """
    flash(msg, etype)
    return redirect(path)

