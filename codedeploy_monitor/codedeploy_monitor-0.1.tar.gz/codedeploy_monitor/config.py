
# (c) Head In Cloud BVBA, Belgium
# http://www.headincloud.be


class AppConfig:

    class __AppConfig__:

        monitor_only = False

        def __init__(self):
            pass

    instance = None

    def __init__(self):
        if not AppConfig.instance:
            AppConfig.instance = AppConfig.__AppConfig__()

    def __getattr__(self, name):
        return getattr(AppConfig.instance, name)

    def __setattr__(self, name, value):
        return setattr(AppConfig.instance, name, value)
