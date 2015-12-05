from m2x.v2.resource import Resource

# Wrapper for AT&T M2X Collections API
# https://m2x.att.com/developer/documentation/v2/collections
class Collection(Resource):
    COLLECTION_PATH = 'collections'
    ITEM_PATH = 'collections/{id}'
    ITEMS_KEY = 'collections'
