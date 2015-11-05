class User(object):

    """Docstring for User. """

    def __init__(self, username, password):
        """@todo: to be defined1.

        :username: @todo
        :password: @todo

        """
        self.username = username
        self.password = password


class DictDiffer(object):

    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict = current_dict
        self.past_dict = past_dict
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added_keys(self):
        return self.set_current - self.intersect

    def added_objects(self):
        return [self.current_dict[k]
                for k in self.set_current - self.intersect]

    def removed_keys(self):
        return self.set_past - self.intersect

    def changed_keys(self, ignored_attributes=None):
        changed = []
        if ignored_attributes is None:
            ignored_attributes = []
        for o in self.intersect:
            past = self._remove_ignored_attributes(self.past_dict[o],
                                                   ignored_attributes)
            current = self._remove_ignored_attributes(self.current_dict[o],
                                                      ignored_attributes)
            if past != current:
                changed.append(o)
        return set(changed)

    def _remove_ignored_attributes(self, d, ignored):
        for ia in ignored:
            if ia in d:
                del d[ia]
        return d

    def changed_objects(self):
        changed = []
        for key in self.intersect:
            old = self.past_dict[key]
            new = self.current_dict[key]
            if old != new:
                changed.append((old, new))
        return changed

    def unchanged_keys(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])


def check_create_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(len(diff.removed_keys()), 0)
    check.assertEqual(len(diff.changed_keys()), 0)

    added = diff.added_objects()
    check.assertEqual(len(added), 1)
    check.check_dict_subset(data, added[0])


def check_read_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(len(diff.removed_keys()), 0)
    check.assertEqual(len(diff.added_keys()), 0)
    check.assertEqual(len(diff.changed_keys()), 0)


def check_update_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(len(diff.removed_keys()), 0)
    check.assertEqual(len(diff.added_keys()), 0)
    check.assertEqual(diff.changed_keys(), set([int(data["id"])]))

    [(old, new)] = diff.changed_objects()
    # the new value must have all the changes from data.
    check.check_dict_subset(data, new)
    # old and new values must be equal for all fields not in data
    unchanged = dict((k, old[k]) for k in old if k not in data)
    if "updated" in unchanged:
        # The field "updated" is changed automatically by the
        # underlying frameworks used in WASKIQ, so it will always
        # change.
        # FIXME: we should not hardwire names of such fields
        del unchanged["updated"]
    check.check_dict_subset(unchanged, new)


def check_delete_cb(check, data, diff, response):
    """Default callback to implement checks after the action has been called.

    :check: CRUD instance
    :data: Dict with submitted data
    :diff: DictDiffer instance
    :response: Response instance

    """
    check.assertEqual(diff.removed_keys(), set([int(data["id"])]))
    check.assertEqual(len(diff.added_keys()), 0)
    check.assertEqual(len(diff.changed_keys()), 0)


class CRUD(object):

    """Docstring for CRUD. """

    def __init__(self, model, unittest, relations=False):
        """@todo: to be defined1.

        :modul: @todo

        """
        self._model = model
        self._unittest = unittest
        self._relations = relations

    def _get_items(self):
        return self._unittest.session.query(self._model).all()

    def _get_url(self, action, id=None):
        url = [self._model.__tablename__, action]
        if id:
            url.append(id)
        return "/" + "/".join(url)

    def _convert(self, dict1):
        for key in dict1:
            # the serialize function returns an empty list, but we need
            # a unicode here, because [] has no effect in post.
            if isinstance(dict1[key], list) and not dict1[key]:
                dict1[key] = ''
        return dict1

    def _2dict(self, values):
        d = {}
        for item in values:
            # Use serialzed data to make comparison possible with the
            # values used to create the HTTP requests.
            d[item.id] = self._convert(
                item.get_values(serialized=True,
                                include_relations=self._relations))
        return d

    def _diff_pre_post(self, pre, post):
        return DictDiffer(post, pre)

    def run(self, data, user, status=200):
        pre_data = self._2dict(self._get_items())
        self._unittest.logout()
        if user:
            self._unittest.login(user.username, user.password)
        response = self.action(data, status)
        post_data = self._2dict(self._get_items())
        return response, self._diff_pre_post(pre_data, post_data)

    def action(self, data, status):
        assert(True)

    def assertTrue(self, first):
        self._unittest.assertTrue(first)

    def assertEqual(self, first, second):
        self._unittest.assertEqual(first, second)

    def check_dict_subset(self, expected, actual):
        """Check that the dictionary expected is a subset of actual.
        Here, 'subset' means: For all keys in the dictionary expected, the
        value in expected must be equal to the value for the same key in
        actual. It's OK for actual to have more keys.
        """
        self.assertEqual(expected,
                         dict((key, actual[key]) for key in expected))


class List(CRUD):

    def action(self, data, status):
        url = self._get_url("list")
        return self._unittest.app.get(url,
                                      params=data,
                                      status=status)

    def run(self, data, user, status=200, check_callback=check_read_cb):
        response, diff = super(List, self).run(data, user=user, status=status)
        if check_callback is None:
            check_callback = check_read_cb
        check_callback(self, data, diff, response)
        return response


class Create(CRUD):

    def action(self, data, status):
        url = self._get_url("create")
        return self._unittest.app.post(url,
                                       params=data,
                                       status=status)

    def run(self, data, user, status=302, check_callback=check_create_cb):
        response, diff = super(Create, self).run(data, user=user,
                                                 status=status)
        if check_callback is None:
            check_callback = check_create_cb
        check_callback(self, data, diff, response)
        return response


class Read(CRUD):

    def action(self, data, status):
        url = self._get_url("read", data["id"])
        return self._unittest.app.get(url, status=status)

    def run(self, data, user, status=200, check_callback=check_read_cb):
        response, diff = super(Read, self).run(data, user=user, status=status)
        if check_callback is None:
            check_callback = check_read_cb
        check_callback(self, data, diff, response)
        return response


class Update(CRUD):

    def action(self, data, status):
        url = self._get_url("update", data["id"])
        return self._unittest.app.post(url,
                                       params=data,
                                       status=status)

    def run(self, data, user, status=302, check_callback=check_update_cb):
        response, diff = super(Update, self).run(data, user=user,
                                                 status=status)
        if check_callback is None:
            check_callback = check_update_cb
        check_callback(self, data, diff, response)
        return response


class Delete(CRUD):

    def action(self, data, status):
        url = self._get_url("delete", data["id"])
        response = self._unittest.app.post(url,
                                           params=data,
                                           status=status)
        return response

    def run(self, data, user, status=302, check_callback=check_delete_cb):
        response, diff = super(Delete, self).run(data, user=user,
                                                 status=status)
        if check_callback is None:
            check_callback = check_delete_cb
        check_callback(self, data, diff, response)
        return response
