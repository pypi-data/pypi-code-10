#=================#
# Clear Tile Statistics

def clearStats(list_stats, host='localhost', port='27017', dbname='tilejet', GEVENT_MONKEY_PATCH=False):
    if GEVENT_MONKEY_PATCH:
        # Import Gevent and monkey patch
        try:
            from gevent import monkey
            monkey.patch_all()
        except:
            print "gevent monkey patch failed"

    # Update MongoDB
    from pymongo import MongoClient
    client = MongoClient(host, port)
    db = client[dbname]
    for stat in list_stats:
        db.drop_collection(stat['collection'])


#=================#
# Build Tile Statistics
def reloadStats(list_stats, host='localhost', port='27017', dbname='tilejet', collection_logs='logs', MONGO_AGG_FLAG=True, GEVENT_MONKEY_PATCH=False):
    print "Reloading Stats"
    if GEVENT_MONKEY_PATCH:
        # Import Gevent and monkey patch
        try:
            from gevent import monkey
            monkey.patch_all()
        except:
            print "gevent monkey patch failed"

    # Update MongoDB
    from pymongo import MongoClient
    client = MongoClient(host, port)
    db = client[dbname]
    #Clear Stats
    for stat in list_stats:
        db.drop_collection(stat['collection'])
    # Reload Stats
    logs = db[collection_logs]
    stats = []
    for desc in list_stats:
        attributes = {}
        for a in desc['attributes']:
            attributes[a] = "$"+a
        stat = {'name': desc['name'],'collection': desc['collection'], 'attributes': attributes}
        stats.append(stat)
    # Calculate Statistics
    values = []
    for stat in stats:
        print stat['name']
        if len(stat['attributes']) == 0:
            doc = {u'stat': stat['name'], u'value': logs.count()}
            db[stat['collection']].insert(doc)
        else:
            query = [
                { "$group": {
                    "_id": stat['attributes'],
                    "value": {
                        "$sum": 1
                    }
                }}
            ]
            agg = logs.aggregate(query)
            values = None
            if MONGO_AGG_FLAG:
                values = list(agg)
            else:
                if u'ok' in agg and u'result' in agg and len(agg[u'result']) == 0:
                    result = agg[u'result']
                    if len(result) > 0:
                        doc = {
                            u'stat': stat['name'],
                            u'value': result[0][u'value']}
                        doc.update(result[0][u'_id'])
                        db[stat['collection']].insert(doc)
                else:
                    values = list(agg[u'result'])

            if values:
                docs = []
                for v in values:
                    doc = {u'stat': stat['name'], u'value': v[u'value']}
                    doc.update(v[u'_id'])
                    docs.append(doc)
                db[stat['collection']].insert(docs, continue_on_error=False)


def buildStats(list_stats, r):
    stats = []
    for desc in list_stats:
        stat = {'collection': desc['collection'], 'attributes': {'stat': desc['name']}}
        for attribute in desc['attributes']:
            stat['attributes'][attribute] = r[attribute]
        stats.append(stat)
    return stats


#=================#
# Get Tile Statistics
def getStat(collection, name, fallback):
    if not collection:
        return fallback

    doc = collection.find_one({'stat': name})

    if doc:
        return doc['value']
    else:
        return fallback


def getStats(collection, fallback, query=None):
    if not collection:
        return fallback

    docs = None
    if query:
        docs = collection.find(query)
    else:
        docs = collection.find()

    if docs:
        return docs
    else:
        return fallback


#=================#
# Increment Tile Statistics
def incStats(db, stats):
    for stat in stats:
        incStat(db[stat['collection']], stat['attributes'])


def incStat(collection, attributes):
    #stat = collection.find_one({'stat': name})
    collection.update(attributes, {'$set': attributes, '$inc': {'value': 1}}, upsert=True)
