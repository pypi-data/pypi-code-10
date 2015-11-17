from .tilelogs import buildTileRequestDocument

#=================#
# Clear Tile Logs
def clearLogs(host='localhost', port='27017', dbname='tilejet', collection_logs='logs', GEVENT_MONKEY_PATCH=False):
    # Import Gevent and monkey patch
    if GEVENT_MONKEY_PATCH:
        from gevent import monkey
        monkey.patch_all()
    # Init Mongo Client
    from pymongo import MongoClient
    client = MongoClient(host, port)
    db = client[dbname]
    # Clear Logs
    db.drop_collection(collection_logs)


#=================#
# Build Tile Logs
def reloadLogs(directory_logs, host='localhost', port='27017', dbname='tilejet', collection_logs='logs', GEVENT_MONKEY_PATCH=False):
    import os
    import glob
    #=========================#
    # Import Gevent and monkey patch
    if GEVENT_MONKEY_PATCH:
        from gevent import monkey
        monkey.patch_all()
    # Init Mongo Client
    from pymongo import MongoClient
    client = MongoClient(host, port)
    db = client[dbname]
    # Clear Logs
    db.drop_collection(collection_logs)
    # Reload Logs
    log_root = directory_logs
    if log_root:
        log_files = glob.glob(log_root+os.sep+"requests_tiles_*.tsv")
        if log_files:
            collection = db[collection_logs]
            for log_file in log_files:
                reloadLog(log_file, collection)


def reloadLog(path_file, collection):
    import os
    import iso8601
    #=========================#
    if path_file:
        if os.path.exists(path_file):
            lines = None
            with open(path_file,'r') as f:
                lines =  f.readlines()

            if lines:
                documents = []
                for line in lines:
                    values = line.rstrip('\n').split("\t")
                    status = values[0]
                    tileorigin = values[1]
                    tilesource = values[2]
                    z = values[3]
                    x = values[4]
                    y = values[5]
                    ip = values[6]
                    #dt = datetime.datetime.strptime(values[6],'YYYY-MM-DDTHH:MM:SS.mmmmmm')
                    dt = iso8601.parse_date(values[7])
                    location = z+"/"+x+"/"+y
                    r = buildTileRequestDocument(tileorigin, tilesource, x, y, z, status, dt, ip)
                    documents.append(r)
                    #collection.insert_one(r)
                #insert_many available in 3.0, which is still in Beta
                #collection.insert_many(documents, ordered=False)
                collection.insert(documents, continue_on_error=True)
