from Products.CMFCore.Expression import Expression

DEPENDENCIES = []

#type mappings for generating the cache type policies
cache_type_mappings = {
    'headersets' : 'HeaderSet',
    'rules' : 'ContentCacheRule'
}

uwosh_cache_policies = {
    'with-caching-proxy' : {
        'headersets' : {
            'cache-for-5-min' : {
                'title': 'Cache For 5 Minutes',
                'lastModified' : 'delete',
                'etag' : False,
                'enable304s' : False,
                'vary' : True,
                'maxAge': 300,
                'sMaxAge' : 300,
                'mustRevalidate' : True,
                'proxyRevalidate' : False,
                'noCache' : False,
                'noStore' : False,
                'public' : False,
                'private' : False,
                'noTransform' : False,
                'preCheck' : None,
                'postCheck' : None,
                'staleWhileRevalidate' : None,
                'staleIfError' : None
            }
        },
        'rules' : {
            'plone-content-types' : {
                'headerSetIdAnon' : 'cache-for-5-min'
            }
        }
    }
}
