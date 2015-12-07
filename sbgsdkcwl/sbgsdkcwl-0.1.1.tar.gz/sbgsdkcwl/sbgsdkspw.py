import functools
import itertools

S = '__!__'

def make_rg_id(metadata_key, io_obj):
    rg = [
        io_obj.meta.sample_group or '',
        io_obj.meta.sample or '',
        io_obj.meta.library or '',
        io_obj.meta.platform_unit or '',
        str(io_obj.meta.chunk) if io_obj.meta.chunk is not None else '',
    ]
    rg_map = {
        'sample': rg[:2],
        'library': rg[:3],
        'platform_unit': rg[:4],
        'chunk': rg[:5],
    }
    return S.join(rg_map[metadata_key]) if metadata_key in rg_map else getattr(io_obj.meta, metadata_key)

def group_for_each(inp, metadata_key):
    if str(metadata_key) == 'None':
        return {'': [f for f in inp]}
    if metadata_key == 'file':
        return {f: [f] for f in inp}
    key_getter = functools.partial(make_rg_id, metadata_key)
    files = sorted(inp, key=key_getter)
    return {key: [f for f in val] for key, val in itertools.groupby(files, key_getter)}
