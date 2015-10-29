from django.core.exceptions import ImproperlyConfigured


class DynamicFieldsMixin(object):
    """
    A serializer mixin that takes an additional `fields` argument that controls
    which fields should be displayed.
    Usage::
        class MySerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
            class Meta:
                model = MyModel

    Modified version of a gist originally created by Danilo Bargen at https://gist.github.com/dbrgn/4e6fc1fe5922598592d6
    """
    removed_fields = {}
    removed_declared_fields = {}
    saved_fields = ()

    def shelve_fields(self):
        # Ensure fields are set in the serializers Meta class.
        try:
            self.saved_fields = self.Meta.fields
        except AttributeError as e:
            raise ImproperlyConfigured("To use a DynamicFieldsMixin, you must specify fields in your DRF Serializer's "
                                       "Meta class. Original Error: {}".format(e))

        # Ensure a context is present, a request object is inside that context, and it has query_params
        try:
            params = self.context['request'].query_params
        except (KeyError, AttributeError):
                raise ImproperlyConfigured("To use a DynamicFieldsMixin, you must initialize the serializer with a"
                                           " context containing the request object.")
        # Detect available field sets as specified in the serializers Meta.fields
        try:
            available_field_sets = self.Meta.field_sets
        except AttributeError as e:
            # No field sets are set. Default field set will be all fields in Meta.fields.
            available_field_sets = {}

        # Figure out which field set to start from. If no field set is passed in,
        # the field set will either be the given default or the current value of Meta.fields
        if 'field_set' in params and params.get('field_set') in available_field_sets:
            field_set = set(available_field_sets[params.get('field_set')])
            self._shelve_fields(allowed_fields=field_set)
        else:
            if 'default' in available_field_sets:
                default_field_set = set(available_field_sets['default'])
            else:
                default_field_set = self.Meta.fields
            self._shelve_fields(allowed_fields=default_field_set)

        if 'exclude_fields' in params:
            excluded_fields = set(params.getlist('exclude_fields'))
            self._shelve_fields(excluded_fields=excluded_fields)

        if 'include_fields' in params:
            field_set = set(params.getlist('include_fields'))
            self._shelve_fields(allowed_fields=field_set)

    def _shelve_fields(self, allowed_fields=None, excluded_fields=None):
        if allowed_fields:
            existing = set(self.fields)
            for field_name in (field_name for field_name in existing if field_name not in set(allowed_fields)):
                self.removed_fields[field_name] = self.fields.pop(field_name)
                if field_name in self._declared_fields:
                    self.removed_declared_fields[field_name] = self._declared_fields.pop(field_name)
            self.Meta.fields = tuple([field_name for field_name in existing if field_name in set(allowed_fields)])

        elif excluded_fields:
            existing = set(self.fields)
            for field_name in (field_name for field_name in existing if field_name in set(excluded_fields)):
                self.removed_fields[field_name] = self.fields.pop(field_name)
                if field_name in self._declared_fields:
                    self.removed_declared_fields[field_name] = self._declared_fields.pop(field_name)
            self.Meta.fields = tuple([field_name for field_name in existing if field_name not in set(excluded_fields)])

    def unshelve_fields(self):
        for field in set(self.removed_fields.keys()):
            try:
                self.fields[field] = self.removed_fields[field]
            except AssertionError:
                # This occurs because we are re-binding fields to their serializer dynamically. Not an actual issue.
                pass
        for field in self.removed_declared_fields:
            self._declared_fields[field] = self.removed_declared_fields[field]

        self.Meta.fields = self.saved_fields
        self.removed_fields = {}
        self.removed_declared_fields = {}
        self.saved_fields = ()

    def to_representation(self, instance):
        """
        Override DRF's to_representation to dynamically remove fields from the model before it is serialized.
        This process mutates the Serializer object, so after we are done serializing, we have to undo our actions
        or the next time the serializer is used, the fields won't be present.
        :param instance: The instance to translate into outgoing representation.
        :return: The outgoing representation.
        """
        self.shelve_fields()
        ret = super(DynamicFieldsMixin, self).to_representation(instance=instance)
        self.unshelve_fields()
        return ret
