
from webportfolio import WebPortfolio, register_package

register_package(__name__)

def view(template=None):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    MaintenanceView = maintenance_view()

    :param view_template_: The directory containing the view pages
    :return:
    """
    if not template:
        template = "WebPortfolio/Package/MaintenancePage/index.html"

    class Maintenance(WebPortfolio):
        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)

            if cls.config_("MODULE_MAINTENANCE_PAGE_ON"):
                app.logger.info("MAINTENANCE PAGE IS ON")

                @app.before_request
                def on_maintenance():
                    return cls.render_(layout_=template), 503

    return Maintenance

Maintenance = view()