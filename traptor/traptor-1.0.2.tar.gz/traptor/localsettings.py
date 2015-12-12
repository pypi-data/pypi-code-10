'''
Settings for traptor
====================
'''
LOG_LEVEL = 'INFO'

KAFKA_HOSTS = "localhost:9092"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Kafka topic to write all twitter data
KAFKA_TOPIC = "traptor"

# Your API information.  Fill this out in localsettings.py!
APIKEYS = {
    'CONSUMER_KEY': "5IwgjDRUlEMI8Tld5mj6JXvjE",
    'CONSUMER_SECRET': "qk9xE1sM6ZAPtOJ1mXRT0qJCiVCvnjuFbHlvmSzzVdYvgHrftg",
    'ACCESS_TOKEN': "3515187809-v2K8RL7I1vTt47KJ7vkOfF5H4GGl0Ljf5aEvzUg",
    'ACCESS_TOKEN_SECRET': "7w5PGAAk3YDLTISQaBfJ8TnrmWKIqmcRBdnf2yADAkBtz"
}

'''
Each 'traptor_type' has a unqiue 'traptor_id'.  This ID is how traptor knows
where to look for a ruleset in Redis.  For example, traptor-follow:0
'''

# Options for TRAPTOR_TYPE:  follow, track
TRAPTOR_TYPE = 'follow'
TRAPTOR_ID = 0