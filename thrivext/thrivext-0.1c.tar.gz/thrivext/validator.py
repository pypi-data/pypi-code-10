class Validator(object):
    def __init__(self, mapperfile, schemafile, datafile):
        self.mapper = mapperfile
        self.schema = schemafile
        self.datafile = datafile

    def run(self):
        print "hello"