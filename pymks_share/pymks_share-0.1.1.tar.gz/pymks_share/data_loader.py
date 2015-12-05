from pymongo import MongoClient
import cPickle as pickle
from bson.binary import Binary


class DataLoader(object):

    def __init__(self, url=None, port=None):
        self.port = port
        self.url = url
        print url
        print port
        if url is None and port is None:
            client = MongoClient()
        elif url is not None and port is not None:
            client = MongoClient(url + str(port))
        else:
            raise RuntimeError('url and port must both be specified')
        self.client = client

    def load_data(self, dataset_name, structure_data, data_source, parameters,
                  response_data=None, authors=None, description=None,
                  other_metadata=None):
        db = self.client.pymks
        bi_structure_data = Binary(pickle.dumps(structure_data, protocol=2))
        bi_response_data = Binary(pickle.dumps(response_data, protocol=2))
        data_dict = {'dataset_name': dataset_name,
                     'structure_data': bi_structure_data,
                     'data_source': data_source,
                     'parameters': parameters,
                     'response_data': bi_response_data,
                     'authors': authors,
                     'description': description,
                     'other_metadata': other_metadata}
        db.data.insert_one(data_dict)
