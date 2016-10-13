from __future__ import absolute_import, print_function, unicode_literals

import copy
import warnings
from collections import OrderedDict

from django.utils import six

from django_compat_patcher.deprecation import *

class MergeDict(object):
    """
    A simple class for creating new "virtual" dictionaries that actually look
    up values in more than one dictionary, passed in the constructor.

    If a key appears in more than one of the given dictionaries, only the
    first occurrence will be used.
    """
    def __init__(self, *dicts):
        warnings.warn('`MergeDict` is deprecated, use `dict.update()` '
                      'instead.', RemovedInDjango19Warning, 2)
        self.dicts = dicts

    def __bool__(self):
        return any(self.dicts)

    def __nonzero__(self):
        return type(self).__bool__(self)

    def __getitem__(self, key):
        for dict_ in self.dicts:
            try:
                return dict_[key]
            except KeyError:
                pass
        raise KeyError(key)

    def __copy__(self):
        return self.__class__(*self.dicts)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    # This is used by MergeDicts of MultiValueDicts.
    def getlist(self, key):
        for dict_ in self.dicts:
            if key in dict_:
                return dict_.getlist(key)
        return []

    def _iteritems(self):
        seen = set()
        for dict_ in self.dicts:
            for item in six.iteritems(dict_):
                k = item[0]
                if k in seen:
                    continue
                seen.add(k)
                yield item

    def _iterkeys(self):
        for k, v in self._iteritems():
            yield k

    def _itervalues(self):
        for k, v in self._iteritems():
            yield v

    if six.PY3:
        items = _iteritems
        keys = _iterkeys
        values = _itervalues
    else:
        iteritems = _iteritems
        iterkeys = _iterkeys
        itervalues = _itervalues

        def items(self):
            return list(self.iteritems())

        def keys(self):
            return list(self.iterkeys())

        def values(self):
            return list(self.itervalues())

    def has_key(self, key):
        for dict_ in self.dicts:
            if key in dict_:
                return True
        return False

    __contains__ = has_key

    __iter__ = _iterkeys

    def copy(self):
        """Returns a copy of this object."""
        return self.__copy__()

    def __str__(self):
        '''
        Returns something like

            "{'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}"

        instead of the generic "<object meta-data>" inherited from object.
        '''
        return str(dict(self.items()))

    def __repr__(self):
        '''
        Returns something like

            MergeDict({'key1': 'val1', 'key2': 'val2'}, {'key3': 'val3'})

        instead of generic "<object meta-data>" inherited from object.
        '''
        dictreprs = ', '.join(repr(d) for d in self.dicts)
        return '%s(%s)' % (self.__class__.__name__, dictreprs)


class SortedDict(dict):
    """
    A dictionary that keeps its keys in the order in which they're inserted.
    """
    def __new__(cls, *args, **kwargs):
        instance = super(SortedDict, cls).__new__(cls, *args, **kwargs)
        instance.keyOrder = []
        return instance

    def __init__(self, data=None):
        warnings.warn(
            "SortedDict is deprecated and will be removed in Django 1.9.",
            RemovedInDjango19Warning, stacklevel=2
        )
        if data is None or isinstance(data, dict):
            data = data or []
            super(SortedDict, self).__init__(data)
            self.keyOrder = list(data) if data else []
        else:
            super(SortedDict, self).__init__()
            super_set = super(SortedDict, self).__setitem__
            for key, value in data:
                # Take the ordering from first key
                if key not in self:
                    self.keyOrder.append(key)
                # But override with last value in data (dict() does this)
                super_set(key, value)

    def __deepcopy__(self, memo):
        return self.__class__([(key, copy.deepcopy(value, memo))
                               for key, value in self.items()])

    def __copy__(self):
        # The Python's default copy implementation will alter the state
        # of self. The reason for this seems complex but is likely related to
        # subclassing dict.
        return self.copy()

    def __setitem__(self, key, value):
        if key not in self:
            self.keyOrder.append(key)
        super(SortedDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(SortedDict, self).__delitem__(key)
        self.keyOrder.remove(key)

    def __iter__(self):
        return iter(self.keyOrder)

    def __reversed__(self):
        return reversed(self.keyOrder)

    def pop(self, k, *args):
        result = super(SortedDict, self).pop(k, *args)
        try:
            self.keyOrder.remove(k)
        except ValueError:
            # Key wasn't in the dictionary in the first place. No problem.
            pass
        return result

    def popitem(self):
        result = super(SortedDict, self).popitem()
        self.keyOrder.remove(result[0])
        return result

    def _iteritems(self):
        for key in self.keyOrder:
            yield key, self[key]

    def _iterkeys(self):
        for key in self.keyOrder:
            yield key

    def _itervalues(self):
        for key in self.keyOrder:
            yield self[key]

    if six.PY3:
        items = _iteritems
        keys = _iterkeys
        values = _itervalues
    else:
        iteritems = _iteritems
        iterkeys = _iterkeys
        itervalues = _itervalues

        def items(self):
            return [(k, self[k]) for k in self.keyOrder]

        def keys(self):
            return self.keyOrder[:]

        def values(self):
            return [self[k] for k in self.keyOrder]

    def update(self, dict_):
        for k, v in six.iteritems(dict_):
            self[k] = v

    def setdefault(self, key, default):
        if key not in self:
            self.keyOrder.append(key)
        return super(SortedDict, self).setdefault(key, default)

    def copy(self):
        """Returns a copy of this object."""
        # This way of initializing the copy means it works for subclasses, too.
        return self.__class__(self)

    def __repr__(self):
        """
        Replaces the normal dict.__repr__ with a version that returns the keys
        in their sorted order.
        """
        return '{%s}' % ', '.join('%r: %r' % (k, v) for k, v in six.iteritems(self))

    def clear(self):
        super(SortedDict, self).clear()
        self.keyOrder = []