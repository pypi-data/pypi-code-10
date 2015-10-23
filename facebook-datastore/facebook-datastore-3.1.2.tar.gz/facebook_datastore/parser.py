import datetime
import logging


logger = logging.getLogger(__name__)


class FacebookDataParserError(Exception):
    pass


class FacebookDataParserCriticalError(FacebookDataParserError):
    pass


class FacebookDataBaseParser(object):
    parse_prefix = 'parse_'

    def __init__(self, data, ignore_errors=False, log_errors=False):
        self.data = data
        self.ignore_errors = ignore_errors
        self.log_errors = log_errors

    def run(self):
        params = {}
        for method in self.get_parsing_methods():
            try:
                params[method.replace(self.parse_prefix, '', 1)] = getattr(
                    self, method)()
            except FacebookDataParserCriticalError as e:
                if self.log_errors:
                    logger.error(e, exc_info=True)
                raise
            except FacebookDataParserError as e:
                if self.log_errors:
                    logger.error(e, exc_info=True)
                if not self.ignore_errors:
                    raise

        return params

    def get_parsing_methods(self):
        return [
            name for name in dir(self)
            if (name.startswith(self.parse_prefix)
                and callable(getattr(self, name)))
        ]


class FacebookDataParser(FacebookDataBaseParser):
    def parse_facebook_id(self):
        try:
            return int(self.data['id'])
        except KeyError:
            raise FacebookDataParserCriticalError("No ID in data")
        except ValueError:
            raise FacebookDataParserCriticalError("ID is not number")

    def parse_first_name(self):
        return self.data.get('first_name', None)

    def parse_last_name(self):
        return self.data.get('last_name', None)

    def parse_locale(self):
        return self.data.get('locale', None)

    def parse_username(self):
        return self.data.get('username', None)

    def parse_location_name(self):
        location = self.data.get('location', None)
        if location:
            return location.get('name', None)

    def parse_location_id(self):
        location = self.data.get('location', None)
        if location:
            return location.get('id', None)

    def parse_name(self):
        return self.data.get('name', None)

    def parse_birthday(self):
        datestr = self.data.get('birthday', None)
        if not datestr:
            return None
        try:
            return datetime.datetime.strptime(datestr, "%m/%d/%Y").date()
        except ValueError as e:
            raise FacebookDataParserError("Birthday date: %s" % e)

    def parse_raw_data(self):
        return self.data.raw_data

    def parse_gender(self):
        gender_name = self.data.get('gender', None)
        if gender_name is None:
            return None
        if gender_name in ["male", "male (hidden)"]:
            return "m"
        if gender_name in ["female", "female (hidden)"]:
            return "f"
        raise FacebookDataParserError("'%s' is not valid gender."
                                      % gender_name)

    def parse_email(self):
        return self.data.get('email', None)

    def parse_age_range_min(self):
        age_range = self.data.get('age_range', {})
        return age_range.get('min', None)

    def parse_age_range_max(self):
        age_range = self.data.get('age_range', {})
        return age_range.get('max', None)

    def parse_uses_ios(self):
        return self._parse_mobile_os('iOS')

    def parse_uses_android(self):
        return self._parse_mobile_os('Android')

    def _parse_mobile_os(self, os):
        devices = self.data.get('devices', [])
        for device in devices:
            if device['os'] == os:
                return True
        return False
