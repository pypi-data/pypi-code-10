from termcolor import cprint


class PrecacheCollection(Exception):
    def __init__(self, field, handler, values_count=None, recomendation=None):
        cprint("Cant create collection", "red", attrs=["bold"])

        cprint("\tHandler: %s" % handler, "red")
        cprint("\tModel: %s" % field.model, "red")
        cprint("\tField: %s" % field.attname, "red")
        cprint("\tRecommendations: %s" % recomendation, "green")
