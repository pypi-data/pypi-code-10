from pymongo import MongoClient
from bson.binary import Binary
import cPickle as pickle
import numpy as np


class DataManager(MongoClient):

    def __init__(self, url):
        super(DataManager, self).__init__(url)

    def fetch_data(self, dataset_name):
        db = self.pymks
        db_dict = db.db_metadata.find({"dataset_name": dataset_name})[0]
        n_datasets = int(db_dict['n_datasets'])
        X = []
        if db_dict['has_response_data']:
            y = []
            for ii in range(n_datasets):
                data_dict = db.data.find({"dataset_name":
                                          dataset_name + '_' + str(ii)})[0]
                X.append(pickle.loads(data_dict['structure_data']))
                y.append(pickle.loads(data_dict['response_data']))
            return np.concatenate(X), np.concatenate(y)
        else:
            for ii in range(n_datasets):
                data_dict = db.data.find({"dataset_name":
                                          dataset_name + '_' + str(ii)})[0]
                X.append(pickle.loads(data_dict['structure_data']))
            return np.concatenate(X)

    def fetch_metadata(self, dataset_name):
        db = self.pymks
        return db.metadata.find({"dataset_name": dataset_name})[0]

    def list_datasets(self):
        db = self.pymks
        collections = db.db_metadata.find()
        return [c['dataset_name'] for c in collections]

    def push_data(self, dataset_name, structure_data, data_source, parameters,
                  response_data=None, authors=None, description=None,
                  other_metadata=None):
        if dataset_name in self.list_datasets():
            raise RuntimeError('dataset_name already used')
        has_response_data = False
        if response_data is not None:
            has_response_data = True
            if len(response_data) != len(structure_data):
                raise RuntimeError(('number of samples for response_data ') +
                                   ('and structure_data must be the same'))
        db = self.pymks
        meta_data_dict = {'dataset_name': dataset_name,
                          'data_source': data_source,
                          'parameters': parameters,
                          'authors': authors,
                          'description': description,
                          'other_metadata': other_metadata}
        data_dicts = self._create_data_dicts(structure_data, response_data,
                                             dataset_name)
        n_datasets = len(data_dicts)
        db_dict = {'dataset_name': dataset_name,
                   'has_response_data': has_response_data,
                   'n_datasets': n_datasets}
        db.data.insert_many(data_dicts)
        db.db_metadata.insert_one(db_dict)
        db.metadata.insert_one(meta_data_dict)

    def _create_data_dicts(self, structure_data, response_data, dataset_name):
        slices = self._get_slices(structure_data)
        data_dicts = []
        if response_data is None:
            for ii, s in enumerate(slices):
                bi_s = Binary(pickle.dumps(structure_data[s], protocol=2))
                data_dicts.append({'dataset_name':
                                  dataset_name + '_' + str(ii),
                                   'structure_data': bi_s})
        else:
            for ii, s in enumerate(slices):
                bi_s = Binary(pickle.dumps(structure_data[s], protocol=2))
                bi_r = Binary(pickle.dumps(response_data[s], protocol=2))
                data_dicts.append({'dataset_name':
                                  dataset_name + '_' + str(ii),
                                   'structure_data': bi_s,
                                   'response_data': bi_r})
        return data_dicts

    def _get_slices(self, data):
        if data is None:
            return [None]
        n_slices = data.nbytes / 1.6e7 + 1
        if n_slices > len(data):
            raise RuntimeError('data is too large to load')
        indices = np.ceil(np.linspace(0, len(data), n_slices))
        if len(indices) <= 1:
            return [slice(None)]
        else:
            return [slice(s0, s1) for s0, s1 in zip(indices[:-1], indices[1:])]
