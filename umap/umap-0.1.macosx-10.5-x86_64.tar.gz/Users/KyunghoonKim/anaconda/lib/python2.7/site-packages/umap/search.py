# -*- coding: utf-8 -*-

from vincenty import vincenty # 1 = 1km
from bson.son import SON

def nearest(database, name, location, maxkm):
    """
    MongoDB GeoSpatial Search
    :param database: db.test
    :param name: field name 'gps'
    :param location: [lat, lon]
    :param maxkm: limit of distance
    :return: count, database
    """
    query = {name: SON([("$near", location),
                         ("$maxDistance", maxkm/111.12)])}
    data = database.find(query)
    return data.count(), data

def nearest(data, location, dist=10):
    for d in data:
        cand = vincenty(location, d['loc'])
#         print dist, cand
        if dist > cand:
            dist = cand
#             result = d
    return dist



# 시장_쇼핑센터
# one degree is approximately 111.12 kilometers
for m in MB:
    maps = db.maps.find({'cat': m})
    for mm in maps:
        location = mm['loc']
        query = {"loc": SON([("$near", location), ("$maxDistance", 0.001/111.12)]), "cat": "시장_쇼핑센터"}
        data = db.maps.find(query)
        count = data.count()
        ite = 1
        while count < 1:
            query = {"loc": SON([("$near", location), ("$maxDistance", (0.001+0.1*ite)/111.12)]), "cat": "시장_쇼핑센터"}
            data = db.maps.find(query)
            count = data.count()
            ite += 1
#         print data.count(),
        dist = nearest(data, location)
        db.maps.update({'_id':mm['_id']}, {'$set': {'market': dist}})
    print m