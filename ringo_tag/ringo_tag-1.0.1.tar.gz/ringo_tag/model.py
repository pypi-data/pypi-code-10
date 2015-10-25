import cgi
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from ringo.lib.helpers import literal
from ringo.model import Base
from ringo.model.base import BaseItem, BaseFactory
from ringo.model.mixins import Owned


class TagFactory(BaseFactory):

    def create(self, user=None, values=None):
        new_item = BaseFactory.create(self, user, values)
        return new_item


class Tag(BaseItem, Owned, Base):
    """Tags (keywords) can be used to mark items."""

    __tablename__ = 'tags'
    """Name of the table in the database for this modul. Do not
    change!"""
    _modul_id = None
    """Will be set dynamically. See include me of this modul"""

    # Define columns of the table in the database
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Text, default=None)
    description = sa.Column('description', sa.Text, default=None)
    tagtype = sa.Column('type', sa.Integer, default=None)

    # Relation to a modul. Tags can be assigned to a module for
    # filtering.
    mid = sa.Column(sa.Integer, sa.ForeignKey('modules.id'))
    modul = sa.orm.relationship("ModulItem", backref="tags")

    @classmethod
    def get_item_factory(cls):
        return TagFactory(cls)

    def render(self):
        mapping = {
            0: "label label-default",
            1: "label label-primary",
            2: "label label-success",
            3: "label label-info",
            4: "label label-warning",
            5: "label label-danger"}
        return literal('<span class="%s">%s</span>'
                       % (mapping.get(self.tagtype), cgi.escape(self.name)))


class Tagged(object):
    """Mixin to add tag (keyword) functionallity to a modul. Adding this Mixin
    the item of a modul will have a "tags" relationship containing all
    the tag entries for this item."""

    @declared_attr
    def tags(cls):
        tbl_name = "nm_%s_tags" % cls.__name__.lower()
        nm_table = sa.Table(tbl_name, Base.metadata,
                            sa.Column('iid', sa.Integer,
                                      sa.ForeignKey(cls.id)),
                            sa.Column('tid', sa.Integer,
                                      sa.ForeignKey("tags.id")))
        tags = sa.orm.relationship(Tag, secondary=nm_table)
        return tags
