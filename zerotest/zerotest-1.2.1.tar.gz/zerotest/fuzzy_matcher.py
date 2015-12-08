from __future__ import unicode_literals

import warnings


class FuzzyMatchWarning(Warning):
    pass


class FuzzyMatcher(object):
    def __init__(self, allow_blank=False, allow_none=False):
        self.content1 = None
        self.content2 = None
        self._allow_blank = allow_blank
        self._allow_none = allow_none

    def set_items(self, content1, content2):
        assert isinstance(content1, dict)
        assert isinstance(content2, dict)
        self.content1 = content1
        self.content2 = content2

    def _find_value_rule(self, value):
        value_type = type(value)
        rule = {"type": value_type}
        if not value:
            rule["empty_value"] = value
        if value_type is dict:
            sub_rules = self._find_key_value_rule(value)
            rule["sub_rules"] = sub_rules
        elif rule["type"] is list:
            sub_rules = self._find_list_rule(value)
            rule["sub_rules"] = sub_rules
        return rule

    def _find_list_rule(self, value):
        assert isinstance(value, list)
        rules = []
        for v in value:
            rules.append(self._find_value_rule(v))
        return rules

    def _find_key_value_rule(self, value):
        """
        get schema rule from k-v pairs
        :param value:
        :return:
        """
        rules = []
        assert isinstance(value, dict)
        for k, v in value.items():
            rule = self._find_value_rule(v)
            rule["key"] = k
            rules.append(rule)

        return rules

    def generate_schema(self, content):
        rule = self._find_value_rule(content)
        return rule

    def _match_list(self, schema, values):
        rules = schema['sub_rules']
        sub_rules = rules[0:min(len(rules), len(values))]
        for i, rule in enumerate(sub_rules):
            value = values[i]
            self._match_rule(rule, value)

    def _match_rule(self, rule, value):
        rule_type = rule['type']
        if rule_type == list:
            self._match_list(rule, value)
        elif rule_type == dict:
            self.match_schema(rule, value)
        else:
            assert rule['type'] == type(value)

    def match_schema(self, schema, content):
        for rule in schema['sub_rules']:
            key = rule.get('key')
            if key:
                if not content:
                    if self._allow_none and content is None:
                        warnings.warn("fields '{}' is None".format(key), FuzzyMatchWarning)
                        continue
                    elif self._allow_blank and content is not None:
                        warnings.warn("fields '{}' = {}".format(key, repr(content)), FuzzyMatchWarning)
                        continue
                    else:
                        value = content
                else:
                    value = content.get(key, None)
            else:
                value = content
            self._match_rule(rule, value)

    def compare(self):
        assert self.content1.keys() == self.content2.keys()
        schema = self.generate_schema(self.content1)
        self.match_schema(schema, self.content2)
