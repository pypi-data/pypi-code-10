from pymongo import MongoClient
from bson.binary import Binary
import cPickle as pickle


class DataManager(object):

    def __init__(self, url=None, port=None):
        self.port = port
        self.url = url
        if url is None and port is None:
            client = MongoClient()
        elif url is not None and port is not None:
            client = MongoClient(url + str(port))
        else:
            raise RuntimeError('url and port must both be specified')
        self.client = client

    def fetch_data(self, dataset_name):
        db = self.client.pymks
        self.data_dict = db.data.find({"dataset_name": dataset_name})[0]
        X = pickle.loads(self.data_dict['structure_data'])
        y = pickle.loads(self.data_dict['response_data'])
        return X, y

    def list_dataset_names(self):
        db = self.client.pymks
        collections = db.metadata.find()
        return [c['dataset_name'] for c in collections]

    def push_data(self, dataset_name, structure_data, data_source, parameters,
                  response_data=None, authors=None, description=None,
                  other_metadata=None):
        db = self.client.pymks
        bi_structure_data = Binary(pickle.dumps(structure_data, protocol=2))
        bi_response_data = Binary(pickle.dumps(response_data, protocol=2))
        data_dict = {'dataset_name': dataset_name,
                     'structure_data': bi_structure_data,
                     'response_data': bi_response_data}
        db.data.insert_one(data_dict)
        meta_data_dict = {'dataset_name': dataset_name,
                          'data_source': data_source,
                          'parameters': parameters,
                          'authors': authors,
                          'description': description,
                          'other_metadata': other_metadata}
        db.metadata.insert_one(meta_data_dict)
