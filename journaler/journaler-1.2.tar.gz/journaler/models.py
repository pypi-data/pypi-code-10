from collections import namedtuple
import json
import datetime
from pytz import utc

DATETIME_FORMAT = "%m-%d-%YT%H:%M:%S.%fZ"

"""
Stores a line of the food log

:type date UTC datetime
:type mood_rating int from 1 to 5 about your general mood
    1 - Poor, 5 - Great
:type food_rating int from 1 to 5 about the food
    1 - Unhealthy/too much, 5 - Healthy, properly portioned
:type mood_tags list[str] labels for mood. Should be stored lowercase
:type food_tags list[str] labels for food. Should be stored lowercase
:type entry_tags list[str] metadata about entry that may be helpful for analysis
:type meal str (Breakfast, Lunch, Dinner, Snack) Multiple meal tags in a day are combined to be one meal
:type note str any other thoughts longform
"""
FoodLog = namedtuple(
    'FoodLog',
    [
        'date',
        'mood_rating',
        'food_rating',
        'mood_tags',
        'food_tags',
        'entry_tags',
        'meal',
        'note'
    ]
)
BREAKFAST = 'breakfast'
LUNCH = 'lunch'
DINNER = 'dinner'
SNACK = 'snack'
VALID_MEALS = [BREAKFAST, LUNCH, DINNER, SNACK]


def food_log_to_json(food_log):
    """
    Turns a FoodLog to json
    :param food_log: FoodLog object
    :return: json string
    """
    result = food_log.__dict__
    result['date'] = food_log.date.strftime(
        DATETIME_FORMAT
    )
    return json.dumps(result)


def json_to_food_log(json_string):
    """
    Turns a json string to a food_log
    :param json_string:
        A json formatted string that can
        be made to a json log
    :return: a FoodLog object
    """
    log_dict = json.loads(json_string)
    return FoodLog(
        date=utc.localize(
            datetime.datetime.strptime(
                log_dict['date'],
                DATETIME_FORMAT
            )
        ),
        mood_rating=log_dict['mood_rating'],
        food_rating=log_dict['food_rating'],
        mood_tags=log_dict['mood_tags'],
        food_tags=log_dict['food_tags'],
        entry_tags=log_dict['entry_tags'],
        meal=log_dict['meal'],
        note=log_dict['note']
    )
