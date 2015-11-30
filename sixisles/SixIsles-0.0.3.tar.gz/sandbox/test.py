#-*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from sixisles import Structure, Document, get_client
from sixisles.types import String, Boolean, ObjectId, Integer, DateTime


class HogeFoo(Document):
    struct = Structure(
        _id=ObjectId(),
        title=String(),
        number=Integer(),
        banned=Boolean(),
        Dt=DateTime()
    )

    class Meta:
        database = get_client("hoge", "localhost")

    def pk(self):
        return self._id


class Repository(Document):
    struct = Structure(
        _id = ObjectId(),
        name = String(),
        author = String(),
        url = String(),
        Dt=DateTime()
    )

    class Meta:
        database = get_client("test_db_name", "localhost")

document = Repository({
    "name": "SixIsles",
    "author": "teitei-tk",
    "url": "https://github.com/teitei-tk/SixIsles"
})
print document.insert()

#   hoges = map(lambda x: HogeFoo(), xrange(10000))
#   HogeFoo.insert_all(hoges)

#   documents = [x for x in HogeFoo.find()]
#   HogeFoo.update_all(documents, {'$set': {'banned': True}})
