from datetime import datetime

from bingads.internal.bulk.string_table import _StringTable
from six import PY2
import re
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY, _CAMPAIGN_OBJECT_FACTORY_V10


DELETE_VALUE = "delete_value"
_BULK_DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'
_BULK_DATETIME_FORMAT_2 = '%m/%d/%Y %H:%M:%S.%f'
_BULK_DATE_FORMAT = "%m/%d/%Y"

url_splitter = ";\\s*(?=https?://)"
custom_param_splitter = "(?<!\\\\);\\s*"
custom_param_pattern = "^\\{_(.*?)\\}=(.*$)"


def bulk_str(value):
    if value is None or (hasattr(value, 'value') and value.value is None):
        return None
    if isinstance(value, str):
        return value
    if PY2:
        if isinstance(value, unicode):
            return value
    return str(value)


def bulk_upper_str(value):
    s = bulk_str(value)
    if s is None:
        return None
    return s.upper()


def bulk_date_str(value):
    if value is None:
        return None
    return '{0!s}/{1!s}/{2!s}'.format(value.Month, value.Day, value.Year)


def bulk_datetime_str(value):
    if value is None:
        return None
    return value.strftime(_BULK_DATETIME_FORMAT)


def _is_daily_budget(budget_type):
    if budget_type.lower() == 'DailyBudgetAccelerated'.lower() \
            or budget_type.lower() == 'DailyBudgetStandard'.lower():
        return True
    else:
        return False


def csv_to_budget(row_values, bulk_campaign):
    success, budget_type = row_values.try_get_value(_StringTable.BudgetType)
    if not success or not budget_type:
        return

    success, budget_row_value = row_values.try_get_value(_StringTable.Budget)
    if not success:
        return
    budget_value = float(budget_row_value) if budget_row_value else None

    bulk_campaign.campaign.BudgetType = budget_type
    if _is_daily_budget(budget_type):
        bulk_campaign.campaign.DailyBudget = budget_value
    else:
        bulk_campaign.campaign.MonthlyBudget = budget_value


def budget_to_csv(bulk_campaign, row_values):
    budget_type = bulk_campaign.campaign.BudgetType
    if not budget_type:
        return

    if _is_daily_budget(str(budget_type)):
        row_values[_StringTable.Budget] = bulk_str(bulk_campaign.campaign.DailyBudget)
    else:
        row_values[_StringTable.Budget] = bulk_str(bulk_campaign.campaign.MonthlyBudget)


def bulk_optional_str(value):
    if value is None:
        return None
    if not value:
        return DELETE_VALUE
    return value


def csv_to_status(c, v):
    if v == 'Expired':
        c.ad_group.Status = 'Expired'
        c._is_expired = True
    else:
        c.ad_group.Status = v if v else None


def bulk_device_preference_str(value):
    if value is None:
        return None
    elif value == 0:
        return "All"
    elif value == 30001:
        return "Mobile"
    else:
        raise ValueError("Unknown device preference")


def parse_datetime(dt_str):
    """ Convert the datetime str to datetime object.

    :param dt_str: The string representing a datetime object.
    :type dt_str: str
    :return: The datetime object parsed from the string.
    :rtype: datetime | None
    """

    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, _BULK_DATETIME_FORMAT)
    except Exception:
        return datetime.strptime(dt_str, _BULK_DATETIME_FORMAT_2)


def parse_date(d_str):
    if not d_str:
        return None
    parsed_date = datetime.strptime(d_str, _BULK_DATE_FORMAT)
    bing_ads_date = _CAMPAIGN_OBJECT_FACTORY.create('Date')
    bing_ads_date.Day = parsed_date.day
    bing_ads_date.Month = parsed_date.month
    bing_ads_date.Year = parsed_date.year

    return bing_ads_date


def parse_device_preference(value):
    if not value:
        return None

    if value.lower() == 'all':
        return 0
    elif value.lower() == "mobile":
        return 30001
    else:
        raise ValueError("Unknown device preference")

def field_to_csv_MediaIds(entity):
    """
    MediaIds field to csv content
    :param entity: entity which has MediaIds attribute
    :return:
    """
    # media_ids? "ns4:ArrayOflong"
    media_ids = entity.ImageMediaIds
    if media_ids is None or len(media_ids) == 0:
        return None
    return ';'.join(str(media_id) for media_id in media_ids)


def csv_to_field_MediaIds(entity, value):
    """
    MediaIds csv to entity
    :param entity:
    :return:
    """
    # media_ids? "ns4:ArrayOflong"
    entity.ImageMediaIds = [None if i == 'None' else int(i) for i in value.split(';')]


# None and empty string will set to empty string
def escape_parameter_text(s):
    return '' if not s else s.replace('\\', '\\\\').replace(';', '\\;')


def unescape_parameter_text(s):
    return '' if not s else s.replace('\\\\', '\\').replace('\\;', ';')


def field_to_csv_UrlCustomParameters(entity):
    """
    transfer the CustomParameters of a entity to csv content (string)
    :param entity: the entity which contains UrlCustomparameters attribute
    :return: csv string content
    """
    if entity is None or entity.UrlCustomParameters is None:
        return None
    if entity.UrlCustomParameters.Parameters is None or entity.UrlCustomParameters.Parameters.CustomParameter is None:
        return DELETE_VALUE
    # The default case when entity created
    if len(entity.UrlCustomParameters.Parameters.CustomParameter) == 0:
        return None
    params = []
    for parameter in entity.UrlCustomParameters.Parameters.CustomParameter:
        params.append('{{_{0}}}={1}'.format(parameter.Key, escape_parameter_text(parameter.Value)))
    return '; '.join(params)


def csv_to_field_UrlCustomParameters(entity, value):
    if value is None or value.strip() == '':
        return
    splitter = re.compile(custom_param_splitter)
    pattern = re.compile(custom_param_pattern)
    #params = _CAMPAIGN_OBJECT_FACTORY_V10.create("ns0:ArrayOfCustomParameter")
    params = []
    param_strs = splitter.split(value)
    for param_str in param_strs:
        match = pattern.match(param_str)
        if match:
            custom_parameter = _CAMPAIGN_OBJECT_FACTORY_V10.create("ns0:CustomParameter")
            custom_parameter.Key = match.group(1)
            custom_parameter.Value = unescape_parameter_text(match.group(2))
            params.append(custom_parameter)
    if len(params) > 0:
        entity.UrlCustomParameters.Parameters.CustomParameter = params


def csv_to_field_Urls(entity, value):
    """
    set FinalUrls / FinalMobileUrls string field
    :param entity: FinalUrls / FinalMobileUrls
    :param value: the content in csv
    :return:set field values
    """
    if value is None or value == '':
        return
    splitter = re.compile(url_splitter)
    entity.string = splitter.split(value)


def field_to_csv_Urls(entity):
    """
    parse entity to csv content
    :param entity: FinalUrls / FinalMobileUrls
    :return: csv content
    """
    if entity is None:
        return None
    if entity.string is None:
        return DELETE_VALUE
    if len(entity.string) == 0:
        return None
    return '; '.join(entity.string)


def ad_rotation_bulk_str(value):
    if value is None:
        return None
    elif value.Type is None:
        return DELETE_VALUE
    else:
        return bulk_str(value.Type)


def parse_ad_rotation(value):
    if not value:
        return None
    ad_rotation = _CAMPAIGN_OBJECT_FACTORY.create('AdRotation')
    ad_rotation.Type = None if value == DELETE_VALUE else value
    return ad_rotation


def parse_ad_group_bid(value):
    if not value:
        return None
    bid = _CAMPAIGN_OBJECT_FACTORY.create('Bid')
    bid.Amount = float(value)
    return bid


def ad_group_bid_bulk_str(value):
    if value is None or value.Amount is None:
        return None
    return bulk_str(value.Amount)


def keyword_bid_bulk_str(value):
    if value is None:
        return None
    if value.Amount is None:
        return DELETE_VALUE
    return bulk_str(value.Amount)


def parse_keyword_bid(value):
    bid = _CAMPAIGN_OBJECT_FACTORY.create('Bid')
    if not value:
        bid.Amount = None
    else:
        bid.Amount = float(value)
    return bid


def minute_bulk_str(value):
    if value == 'Zero':
        return '0'
    elif value == 'Fifteen':
        return '15'
    elif value == 'Thirty':
        return '30'
    elif value == 'FortyFive':
        return '45'
    else:
        raise ValueError('Unknown minute')


def parse_minute(value):
    minute_number = int(value)
    if minute_number == 0:
        return 'Zero'
    elif minute_number == 15:
        return 'Fifteen'
    elif minute_number == 30:
        return 'Thirty'
    elif minute_number == 45:
        return 'FortyFive'
    raise ValueError('Unknown minute')


def parse_location_target_type(value):
    if value == 'Metro Area':
        return 'MetroArea'
    elif value == 'Postal Code':
        return 'PostalCode'
    else:
        return value


def location_target_type_bulk_str(value):
    if value == 'MetroArea':
        return 'Metro Area'
    elif value == 'PostalCode':
        return 'Postal Code'
    else:
        return value
