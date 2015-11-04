from ConfigParser import RawConfigParser, NoSectionError, NoOptionError, Error


class Config(RawConfigParser, object):
    def __init__(self, config_file):
        super(Config, self).__init__()
        self.file = config_file
        self.read(self.file)

    def __repr__(self):
        return '\n'.join(map(str, self.sections()))

    def _check_section_exists(func):
        def wrapped(self, section, *args, **kwargs):
            if self.has_section(section):
                return func(self, section, *args, **kwargs)
            else:
                raise NoSectionError(section)
        return wrapped

    def keys(self):
        return self.sections()

    @_check_section_exists
    def __getitem__(self, section):
        return Section(self, section)

    @_check_section_exists
    def __delitem__(self, section):
        self.remove_section(section)
        return True

    def __setitem__(self, section, section_obj):
        try:
            [section_obj[key] for key in section_obj]
            if self.has_section(section):
                del self[section]
            self.add_section(section)
            for key in section_obj:
                self[section][key] = section_obj[key]
        except (IndexError, KeyError, TypeError) as e:
            raise ReadSectionError(msg='Unable to read section.\
            Make sure it is a valid dict-like.\n%s' % section_obj)

    def save(self, filename=None, append=False):
        filename = self.file if filename is None else filename
        mode = 'a' if append else 'w'
        with open(filename, mode) as fp:
            self.write(fp)


class Section(object):
    def __init__(self, config_obj, section):
        self.config_obj = config_obj
        self.name = section

    def __repr__(self):
        s = '[%s]\n' % self.name
        items = self.config_obj.items(self.name)
        s += '\n'.join(['%s = %s' % (k, v) for k, v in items])
        return s

    def _check_option_exists(func):
        def wrapped(self, option, *args, **kwargs):
            if self.config_obj.has_option(self.name, option):
                return func(self, option, *args, **kwargs)
            else:
                raise NoOptionError(option, self.name)
        return wrapped

    def keys(self):
        return self.config_obj.options(self.name)

    @_check_option_exists
    def __getitem__(self, option):
        return self.config_obj.get(self.name, option)

    @_check_option_exists
    def __delitem__(self, option):
        self.config_obj.remove_option(self.name, option)
        return True

    def __setitem__(self, option, value):
        self.config_obj.set(self.name, option, value)


class ReadSectionError(Error):
    pass
