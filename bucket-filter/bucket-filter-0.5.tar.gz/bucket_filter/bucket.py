class Bucket():
    def __init__(self, condition, elements=None):
        self.condition = condition
        self.elements = {}
        self.__check_validity_of_elements(elements)

    def __check_validity(self, element):
        if isinstance(element, dict):
            if "id" in element:
                self.elements[element["id"]]= element
        elif hasattr(element, "id"):
            self.elements[getattr(element, "id")]= element

    def __check_validity_of_elements(self, elements):
        if elements:
            if not isinstance(elements, list):
                elements = [elements]
            for element in elements:
                self.__check_validity(element)

    def add_elements(self, elements):
        if isinstance(elements, list):
            self.elements.extend(elements)
        else:
            self.elements.append(elements)

    def evict_elements(self, keys):
        if not isinstance(keys, list):
            keys = [keys]
        for key in keys:
            self.elements.pop(key, None)

    def __repr__(self):
        return self.condition + "/" + "{}".format(len(self.elements))