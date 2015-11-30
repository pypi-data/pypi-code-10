class PoogleError(Exception):
    pass


class PoogleRequestError(PoogleError):
    pass


class PoogleParserError(PoogleError):
    pass


class PoogleMaxQueriesError(PoogleError):
    pass


class PoogleNoResultsError(PoogleError):
    pass


class PoogleNoMoreResultsError(PoogleError):
    pass
