
collection = {}

def save(name, template):
    collection[name] = template

def has(name):
    return name in collection

def get(name):
    return collection[name]
