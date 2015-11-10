def is_authenticated(request):
    if hasattr(request.identity):
        return True
    return False
