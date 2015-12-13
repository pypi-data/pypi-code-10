from bucket_filter.bucket import Bucket
from bucket_filter.condition import ConditionType, BooleanCondition
from bucket_filter.resolver import parse, evaluate

buckets = {}

def get_bucket(expression):
    key = BooleanCondition.build_key(expression)
    return buckets.get(key, None)


def register_bucket(expression, elements=None, condition_type=ConditionType.BOOLEAN):
    if condition_type == ConditionType.BOOLEAN:
        key = BooleanCondition.build_key(expression)
        if key not in buckets:
            condition = BooleanCondition(expression)
            bucket = Bucket(condition, elements)
            buckets[condition.key] = bucket


def solve(expression):
    expressions, inner = parse(expression)
    evaluated = {}
    if inner:
        for i in inner:
            evaluate(expressions["{}".format(i)], evaluated, buckets)
    bucket_final = evaluate(expressions["FINAL"], evaluated, buckets)
    return bucket_final.elements.values()
