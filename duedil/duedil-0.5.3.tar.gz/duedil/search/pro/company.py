

# from ...resources import Resource
from .. import SearchResource


class CompanySearchResult(SearchResource):
    attribute_names = [
        'locale',
        'name',
        'company_url'
    ]
    result_obj = {
        'company': 'duedil.resources.pro.company.Company'
    }
