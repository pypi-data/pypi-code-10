from fanstatic import Library, Resource

library = Library('lodash', 'resources')

lodash = Resource(
    library, 'js/lodash.js',
    minified='js/lodash.min.js'
)

lodash_compatible = Resource(
    library, 'js/lodash.compat.js',
    minified='js/lodash.compat.min.js'
)
