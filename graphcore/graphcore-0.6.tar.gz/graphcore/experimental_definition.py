@gc.property
def name(id):
    return str(id)


# is the same as this:


gc.rule(['filename.id'], 'filename.name')
def name(id):
    return str(id)
