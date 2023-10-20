import collections.abc

from elasticsearch_dsl import Field, Range


class RangeField(Field):
    _coerce = True

    def _deserialize(self, data):
        if isinstance(data, Range):
            return data
        return Range(data)

    def _serialize(self, data):
        if data is None:
            return None
        if not isinstance(data, collections.abc.Mapping):
            data = data.to_dict()
        return data
