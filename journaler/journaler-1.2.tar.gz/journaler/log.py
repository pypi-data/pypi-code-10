#!/usr/bin/env python
import datetime
from journaler.models import food_log_to_json, VALID_MEALS, FoodLog
from journaler.validate import validate_rating, validate_meal
import os

LOG_LOC_ENV = "JOURNAL_LOG_LOC"

TAG_PROMPT_FORMAT = "How would you describe your {}? (Use key phrases separated by commas)\n"
RATING_PROMPT_FORMAT = "{} Rating?\n"


def add_log_to_file(loc, log):
    """
    :param loc: path to file we are adding to
    :param log: FoodLog object
    :return:
    """
    with open(loc, "a") as log_file:
        log_file.write(food_log_to_json(log))
        log_file.write("\n")


def format_tags(tag_string):
    """
    :param tag_string: String of tags comma separated
    :return: list of strings
    """
    if not tag_string.strip().replace(',', ''):
        return []
    return filter(None, map(lambda x: x.strip(), tag_string.lower().split(',')))


def _get_value(prompt, validation_function):
    value = None
    while not value:
        value = raw_input(prompt).lower()
        try:
            validation_function(value)
        except ValueError as e:
            print str(e)
            value = None
    return value


def main():
    location = os.getenv(LOG_LOC_ENV)
    while not location:
        location = raw_input("Where is the log?\n")
        if not os.path.isdir(os.path.dirname(location)):
            print "Invalid path!"
    if not os.path.isfile(location):
        result = raw_input("File {} does not exist. Create new log?\n".format(location))
        if result.lower() not in ['y', 'yes', 'ye']:
            print("Assuming wrong path provided then. Quitting")
            exit(1)

    mood_rating = _get_value(RATING_PROMPT_FORMAT.format("Mood"), validate_rating)
    food_rating = _get_value(RATING_PROMPT_FORMAT.format("Food"), validate_rating)
    mood_tags = format_tags(raw_input(TAG_PROMPT_FORMAT.format("mood")).lower())
    food_tags = format_tags(raw_input(TAG_PROMPT_FORMAT.format("food")).lower())
    entry_tags = format_tags(raw_input(TAG_PROMPT_FORMAT.format("entry")).lower())
    meal = _get_value(
        "What meal is this? Must be one of: {}\n".format(VALID_MEALS), validate_meal
    )
    note = raw_input("Any other thoughts?\n")
    log = FoodLog(
        date=datetime.datetime.utcnow(),
        mood_rating=mood_rating,
        food_rating=food_rating,
        mood_tags=mood_tags,
        food_tags=food_tags,
        entry_tags=entry_tags,
        meal=meal,
        note=note
    )
    add_log_to_file(location, log)
    print "Entry Added"

if __name__ == '__main__':
    main()
