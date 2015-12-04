import pywikibase
import json
from revscoring.datasources import Datasource
from revscoring.datasources.revision import text


def process_item(text):
    item = pywikibase.ItemPage()
    item.get(content=json.loads(text))
    return item


item = Datasource("parsed_revision_text.item", process_item, depends_on=[text])
