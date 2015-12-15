from uwosh.core.utils import *
from uwosh.default.config import DEPENDENCIES
from Products.GenericSetup import interfaces as gsinterfaces
from zope import component
from config import uwosh_cache_policies, cache_type_mappings

base_cache_rule_set = "with-caching-proxy"

def add_cache_policies(portal):
    plone_cache_tool = portal.portal_cache_settings

    for policy_id, policy_settings in uwosh_cache_policies.items():
            
        policy = plone_cache_tool[policy_id]
        
        def copy_attrs(obj, attrs):
            for key, value in attrs.items():
                if hasattr(obj, key):
                    if type(value) == dict:
                        copy_attrs(obj[key], value)
                    else:
                        setattr(obj, key, value)
                else:
                    if type(value) == dict and cache_type_mappings.has_key(obj.getId()):
                        #create obj and copy values...
                        obj.invokeFactory(id=key, type_name=cache_type_mappings[obj.getId()])
                        copy_attrs(obj[key], value)
                    else:
                        #skip this because it doesn't have a correct attribute
                        pass
                        
        copy_attrs(policy, policy_settings)

def import_all(context):
    
    if not context.readDataFile('uwosh.default.txt'):
        return
    
    #add view to ATDocument
    site = context.getSite()
    pt = getToolByName(site, "portal_types")
    
    # copy over cache setup settings
    if has.product('CacheSetup').installed():
        add_cache_policies(site)
