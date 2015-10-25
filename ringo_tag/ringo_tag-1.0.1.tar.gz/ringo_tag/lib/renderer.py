from ringo.lib.helpers import get_item_modul
from ringo.lib.renderer.form import ListingFieldRenderer


class TagFieldRenderer(ListingFieldRenderer):
    """Renderer to render tags  listings. The renderer will only show
    tags which are either associated to no module or the the items
    module."""

    def __init__(self, field, translate):
        ListingFieldRenderer.__init__(self, field, translate)

    def _get_all_items(self):
        tags = []
        alltags = ListingFieldRenderer._get_all_items(self)
        item_modul = get_item_modul(self._field._form._request,
                                    self._field._form._item).id
        for tag in alltags:
            if not tag.modul or (tag.modul.id == item_modul):
                tags.append(tag)
        alltags.items = tags
        return alltags
