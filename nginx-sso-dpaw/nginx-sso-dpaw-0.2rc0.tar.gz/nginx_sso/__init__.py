import os

def config(settings):
    """
    config project to support nginx sso
    """
    #read env config; defaut is enabled
    enabled = os.environ.get('SSO_ENABLED', None)
    if enabled:
        if enabled.lower() in ["true","on","yes","y","t","ok"]:
            enabled = True
        else:
            enabled = False
    else:
        enabled = True

    if not enabled :
        return

    #Add ngins sso middleware
    middlewares = settings['MIDDLEWARE_CLASSES']
    if "nginx_sso.django.middleware.NginxAuthMiddleware" in middlewares:
        #already configured
        pass
    else:
        #add the sso middleware after "django.contrib.auth.middleware.AuthenticationMiddleware"
        pos = 0
        try:
            pos = middlewares.index("django.contrib.auth.middleware.AuthenticationMiddleware")
        except:
            #not found django.contrib.auth.middleware.AuthenticationMiddleware
            return
        new_middlewares = [m for m in middlewares[0:pos + 1]]
        new_middlewares.append("nginx_sso.django.middleware.NginxAuthMiddleware")
        new_middlewares = new_middlewares + [m for m in middlewares[pos + 1:]]
        settings['MIDDLEWARE_CLASSES'] = tuple(new_middlewares)

    #Add nginx sso into INSTALLED_APPS
    installed_apps = settings['INSTALLED_APPS']
    if "nginx_sso" not in installed_apps:
        new_installed_apps = [a for a in installed_apps]
        new_installed_apps.append("nginx_sso")
        settings["INSTALLED_APPS"] = tuple(new_installed_apps)

    #Add nginx sso authentication backend
    backends = settings.get('AUTHENTICATION_BACKENDS')
    if backends:
        if "nginx_sso.django.backends.NginxAuthBackend" in backends:
            #already configured
            pass
        else:
            new_backends = [b for b in backends]
            new_backends.insert(0,"nginx_sso.django.backends.NginxAuthBackend")
            settings["AUTHENTICATION_BACKENDS"] = tuple(new_backends)
    else:
        settings["AUTHENTICATION_BACKENDS"] = ("nginx_sso.django.backends.NginxAuthBackend",)

    
    


    
