import json
import os

def _get_meta(fpath, reload_job=False):
    def get_files(o):
        if isinstance(o, dict) and o.get('class') == 'File':
            return [o]
        if isinstance(o, dict):
            return sum(map(get_files, o.itervalues()), [])
        if isinstance(o, list):
            return sum(map(get_files, o), [])
        return []

    files = getattr(_get_meta, '_files', None)
    if reload_job or files is None:
        with open('job.json') as fp:
            job = json.load(fp)
        files = {f['path']: f for f in get_files(job['inputs'])}
    return files[fpath].get('metadata', {})


class _DotDict(dict):
    def _map(self, attr):
        key_map = {
            "file_type": "file_extension",
            "seq_tech": "platform",
            "sample": "sample_id",
            "library": "library_id",
            "platform_unit": "platform_unit_id",
            "chunk": "file_segment_number",
            "qual_scale": "quality_scale"
        }
        if attr in key_map:
            attr = key_map[attr]
        return attr

    def __init__(self, *args, **kwargs):
        super(_DotDict, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict) or isinstance(arg, _DotDict):
                for k, v in arg.iteritems():
                    nk = self._map(k)
                    if k != nk and k in self:
                        self.pop(k)
                    self[nk] = v
        if kwargs:
            for k, v in kwargs.iteritems():
                self[self._map(k)] = v

    def __getattr__(self, attr):
        return self.get(self._map(attr))

    def __setattr__(self, key, value):
        self.__setitem__(self._map(key), value)

    def __setitem__(self, key, value):
        super(_DotDict, self).__setitem__(self._map(key), value)
        self.__dict__.update({self._map(key): value})

    def __delattr__(self, item):
        self.__delitem__(self._map(item))

    def __delitem__(self, key):
        super(_DotDict, self).__delitem__(self._map(key))
        del self.__dict__[self._map(key)]

class _OldInput(str):

    _meta = None

    @property
    def meta(self):
        if self._meta is None:
            self._meta = _DotDict(_get_meta(self))
        return self._meta
    
    def make_metadata(self, **kwargs):
        new_meta = _DotDict(self.meta)
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                new_meta[key] = value
        return new_meta


class _OldOutputBucket(_DotDict):
    
    def __setitem__(self, key, value):
        if isinstance(value, list):
            super(_OldOutputBucket, self).__setitem__(key, _OldOutputList(value))
        else:
            super(_DotDict, self).__setitem__(key, _OldOutput(value))
            

class _OldOutput(str):

    _meta = None

    @property
    def meta(self):
        if self._meta is None:
            self._meta = _DotDict()
        return self._meta

    @meta.setter
    def meta(self, value):
        self._meta = _DotDict(value)


class _OldOutputList(list):

    def add_file(self, name):
        new_file = _OldOutput(name)
        self.append(new_file)
        return new_file

def cwl_input(_args, _new, _old, list=False):
    _new = _args[_new]
    if isinstance(_new, str):
        _new = [_new]
    if list==False and len(_new) > 1:
        raise Exception('Number of items provided to a non-list type input.')
    if len(_new) == 1 and list == False:
        self.inputs[_old] =  _OldInput(_new[0])
    else:
        self.inputs[_old] = map(_OldInput, _new)

def cwl_param(_args, _new, _old):
    self.params[_old] = _args[_new]

def cwl_output(_old, list=False):
    if list is False:
        self.outputs[_old] = _OldOutput()
    else:
        self.outputs[_old] = _OldOutputList()


def cwl_finish():
    if not self['outputs']:
        return
    if 'cwl_secondary' not in self:
        self['cwl_secondary'] = {}
    data = {}
    for output in self['outputs']:
        o = self['outputs'][output]
        sf = self['cwl_secondary'].get(output, None)
        if isinstance(o, _OldOutputList):
            file_data = []
            for f in o:
                f_dict = {'name': os.path.split(f)[1], \
                          'class': 'File', \
                          'metadata': f.meta, \
                          'path': os.path.join(os.getcwd(), f)}
                if sf:
                    f_dict['secondaryFiles'] = [{'path': os.path.join(os.getcwd(), x), "class": "File"} for x in sf]
                file_data.append(f_dict)
        else:
            file_data = {
                'name': os.path.split(o)[1],
                'class': 'File',
                'metadata': o.meta,
                'path': os.path.join(os.getcwd(), o)
            }
            if sf:
                file_data['secondaryFiles'] = [{'path': os.path.join(os.getcwd(), x), "class": "File"} for x in sf]
        data[output] = file_data
    with open('cwl.output.json', 'w') as w:
        json.dump(data, w)

def cwl_set_secondary(output, secondary_files):
    if 'cwl_secondary' not in self:
        self['cwl_secondary'] = {}
    if not isinstance(secondary_files, list):
        secondary_files = [secondary_files]
    self['cwl_secondary'][output] = secondary_files

################################################################################

global self
self = _DotDict(globals())
if 'inputs' not in self:
    self['inputs'] = _DotDict()
if 'outputs' not in self:
    self['outputs'] =  _OldOutputBucket()
if 'params' not in self:
    self['params'] = _DotDict()