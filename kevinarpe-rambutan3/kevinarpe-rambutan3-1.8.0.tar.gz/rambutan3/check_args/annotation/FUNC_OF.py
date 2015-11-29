from rambutan3.check_args.func.RFunctionSignatureMatcherBuilder import RFunctionSignatureMatcherBuilder


# noinspection PyPep8Naming
def FUNC_OF(*matcher_tuple) -> RFunctionSignatureMatcherBuilder:
    x = RFunctionSignatureMatcherBuilder(*matcher_tuple)
    return x
