# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "kyper_census"


def list_surveys():
    ''' List surveys
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_surveys")
    return _pd.read_json(ret, orient="split", dtype=False)

def list_years():
    ''' List servey year
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_years")
    return _pd.read_json(ret, orient="split", dtype=False)

def list_geo_levels(surveys=['sf1', 'sf3'], years=[2010, 2000, 1990]):
    ''' List geography levels
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_geo_levels", surveys=surveys, years=years)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_sf1_tables(title=None, years=[2010, 2000, 1990]):
    ''' Search census SF1 variable tables
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_sf1_tables", title=title, years=years)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_sf1_labels(label=None, concept=".*", years=[2010, 2000, 1990]):
    ''' Search census SF1 variable labels
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_sf1_labels", label=label, concept=concept, years=years)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_sf1_variables(variable=None, label=None, concept=".*", years=[2010, 2000, 1990]):
    ''' Search census SF1 variable
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_sf1_variables", variable=variable, label=label, concept=concept, years=years)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_states(states=['*']):
    ''' List SF1 states
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_states", states=states)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_counties(states=['*'], counties=['*']):
    ''' List SF1 countries
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_counties", states=states, counties=counties)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_SLD(states=['*']):
    ''' List SF1 state legislative districts
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_SLD", states=states)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_CD(states=['*'], cds=['*']):
    ''' List SF1 congressional districts
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_CD", states=states, cds=cds)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_county_subdivisions(state=None, counties=['*'], county_subdivisions=['*']):
    ''' List SF1 county subdivisions
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_county_subdivisions", state=state, counties=counties, county_subdivisions=county_subdivisions)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_tracts(state=None, counties=['*'], tracts=['*']):
    ''' List SF1 tracts
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_tracts", state=state, counties=counties, tracts=tracts)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_places(state=None, counties=['*'], places=['*']):
    ''' List SF1 place
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_places", state=state, counties=counties, places=places)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_zip_codes(state=None, zips=['*']):
    ''' List SF1 zip codes
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_zip_codes", state=state, zips=zips)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_block_groups(state=None, county=None, block_groups=['*']):
    ''' List SF1 block groups
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_block_groups", state=state, county=county, block_groups=block_groups)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf1_blocks(state=None, county=None, blocks=['*']):
    ''' List SF1 blocks
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf1_blocks", state=state, county=county, blocks=blocks)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_states(variables=None, states=['*'], year=2010):
    ''' get census of SF1 states
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_states", variables=variables, states=states, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_counties(variables=None, states=['*'], counties=['*'], year=2010):
    ''' get census of SF1 counties
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_counties", variables=variables, states=states, counties=counties, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_SLD(variables=None, states=['*'], year=2010):
    ''' get census of SF1 state legislative district
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_SLD", variables=variables, states=states, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_CD(variables=None, states=['*'], cds=['*'], year=2010):
    ''' get census of SF1 congressional district
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_CD", variables=variables, states=states, cds=cds, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_county_subdivision(variables=None, state=None, counties=['*'], county_subdivisions=['*'], year=2010):
    ''' get census of SF1 county subdivision
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_county_subdivision", variables=variables, state=state, counties=counties, county_subdivisions=county_subdivisions, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_tract(variables=None, state=None, counties=['*'], tracts=['*'], year=2010):
    ''' get census of SF1 tract
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_tract", variables=variables, state=state, counties=counties, tracts=tracts, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_place(variables=None, state=None, counties=['*'], places=['*'], year=2010):
    ''' get census of SF1 place
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_place", variables=variables, state=state, counties=counties, places=places, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_zip_code(variables=None, state=None, zips=['*'], year=2010):
    ''' get census of SF1 zip code
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_zip_code", variables=variables, state=state, zips=zips, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_block_group(variables=None, state=None, county=None, block_groups=['*'], year=2010):
    ''' get census of SF1 block group
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_block_group", variables=variables, state=state, county=county, block_groups=block_groups, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf1_block(variables=None, state=None, county=None, blocks=['*'], year=2010):
    ''' get census of SF1 block
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf1_block", variables=variables, state=state, county=county, blocks=blocks, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_sf3_tables(title=None, years=[2000, 1990]):
    ''' Search census SF3 variable tables
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_sf3_tables", title=title, years=years)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_sf3_labels(label=None, concept=".*", years=[2000, 1990]):
    ''' Search census SF3 variable labels
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_sf3_labels", label=label, concept=concept, years=years)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_sf3_variables(variable=None, label=None, concept=".*", years=[2000, 1990]):
    ''' Search census SF3 variable
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_sf3_variables", variable=variable, label=label, concept=concept, years=years)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_states(states=['*']):
    ''' List SF3 states
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_states", states=states)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_counties(states=['*'], counties=['*']):
    ''' List SF3 countries
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_counties", states=states, counties=counties)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_CD(states=['*'], cds=['*']):
    ''' List SF3 congressional districts
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_CD", states=states, cds=cds)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_county_subdivisions(state=None, counties=['*'], county_subdivisions=['*']):
    ''' List SF3 county subdivisions
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_county_subdivisions", state=state, counties=counties, county_subdivisions=county_subdivisions)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_tracts(state=None, counties=['*'], tracts=['*']):
    ''' List SF3 tracts
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_tracts", state=state, counties=counties, tracts=tracts)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_places(state=None, counties=['*'], places=['*']):
    ''' List SF3 place
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_places", state=state, counties=counties, places=places)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_zip_codes(state=None, zips=['*']):
    ''' List SF3 zip codes
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_zip_codes", state=state, zips=zips)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_sf3_block_groups(state=None, county=None, block_groups=['*']):
    ''' List SF3 block groups
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_sf3_block_groups", state=state, county=county, block_groups=block_groups)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_states(variables=None, states=['*'], year=2000):
    ''' get census of SF3 states
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_states", variables=variables, states=states, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_counties(variables=None, states=['*'], counties=['*'], year=2000):
    ''' get census of SF3 counties
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_counties", variables=variables, states=states, counties=counties, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_CD(variables=None, states=['*'], cds=['*'], year=2000):
    ''' get census of SF3 congressional district
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_CD", variables=variables, states=states, cds=cds, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_county_subdivision(variables=None, state=None, counties=['*'], county_subdivisions=['*'], year=2000):
    ''' get census of SF3 county subdivision
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_county_subdivision", variables=variables, state=state, counties=counties, county_subdivisions=county_subdivisions, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_tract(variables=None, state=None, counties=['*'], tracts=['*'], year=2000):
    ''' get census of SF3 tract
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_tract", variables=variables, state=state, counties=counties, tracts=tracts, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_place(variables=None, state=None, counties=['*'], places=['*'], year=2000):
    ''' get census of SF3 place
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_place", variables=variables, state=state, counties=counties, places=places, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_zip_code(variables=None, state=None, zips=['*'], year=2000):
    ''' get census of SF3 zip code
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_zip_code", variables=variables, state=state, zips=zips, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sf3_block_group(variables=None, state=None, county=None, block_groups=['*'], year=2000):
    ''' get census of SF3 block group
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sf3_block_group", variables=variables, state=state, county=county, block_groups=block_groups, year=year)
    return _pd.read_json(ret, orient="split", dtype=False)
