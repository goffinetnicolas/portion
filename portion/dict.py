from collections.abc import MutableMapping, Mapping
from .const import Bound
from .interval import Interval
from .intervaltree import IntervalTree


class IntervalDict(MutableMapping):
    """
    An IntervalDict is a dict-like data structure that maps from intervals to data,
    where keys can be single values or Interval instances.

    When keys are Interval instances, its behaviour merely corresponds to
    range queries and it returns IntervalDict instances corresponding to the
    subset of values covered by the given interval. If no matching value is
    found, an empty IntervalDict is returned.
    When keys are "single values", its behaviour corresponds to the one of Python
    built-in dict. When no matching value is found, a KeyError is raised.

    Note that this class does not aim to have the best performance, but is
    provided mainly for convenience. Its performance mainly depends on the
    number of distinct values (not keys) that are stored.
    """

    __slots__ = ("_storage",)

    # Class to use when creating Interval instances
    _klass = Interval

    def __init__(self, mapping_or_iterable=None):
        """
        Return a new IntervalDict.

        If no argument is given, an empty IntervalDict is created. If an argument
        is given, and is a mapping object (e.g., another IntervalDict), an
        new IntervalDict with the same key-value pairs is created. If an
        iterable is provided, it has to be a list of (key, value) pairs.

        :param mapping_or_iterable: optional mapping or iterable.
        """
        self._storage = IntervalTree()

        if mapping_or_iterable is not None:
            self.update(mapping_or_iterable)

    @classmethod
    def _from_items(cls, items):
        """
        Fast creation of an IntervalDict with the provided items.

        The items have to satisfy the two following properties: (1) all keys
        must be disjoint intervals and (2) all values must be distinct.

        :param items: list of (key, value) pairs.
        :return: an IntervalDict
        """
        d = cls()
        for key, value in items:
            d[key] = value

        return d

    @classmethod
    def _from_interval_tree(cls, interval_tree):
        d = cls()
        x = interval_tree.root.minimum
        while not x.is_nil:
            d[x.interval] = x.value
            x = interval_tree.successor(x)
        return d

    def clear(self):
        """
        Remove all items from the IntervalDict.
        """
        self._storage.__init__()

    def copy(self):
        """
        Return a shallow copy.

        :return: a shallow copy.
        """
        #return self.__class__._from_items(self.items())
        return self.__class__._from_interval_tree(self._storage)


    def get(self, key, default=None):
        """
        Return the values associated to given key.

        If the key is a single value, it returns a single value (if it exists) or
        the default value. If the key is an Interval, it returns a new IntervalDict
        restricted to given interval. In that case, the default value is used to
        "fill the gaps" (if any) w.r.t. given key.

        :param key: a single value or an Interval instance.
        :param default: default value (default to None).
        :return: an IntervalDict, or a single value if key is not an Interval.
        """
        if isinstance(key, Interval):
            d = self[key]
            d[key - d.domain()] = default
            return d
        else:
            try:
                return self[key]
            except KeyError:
                return default

    def find(self, value):
        """
        Return a (possibly empty) Interval i such that self[i] = value, and
        self[~i] != value.

        :param value: value to look for.
        :return: an Interval instance.
        """
        return self._storage.find(value)


    def items(self):
        """
        Return a list of key values tuples sorted by key
        (see https://docs.python.org/3/library/stdtypes.html#dict-views).

        :return: a list of key values tuples.
        """
        return self._storage.items()

    def keys(self):
        """
        Return a view object on the contained keys (sorted)
        (see https://docs.python.org/3/library/stdtypes.html#dict-views).

        :return: list of keys.
        """
        return self._storage.keys()

    def values(self):
        """
        Return a view object on the contained values sorted by key
        (see https://docs.python.org/3/library/stdtypes.html#dict-views).

        :return: a list of values.
        """
        return self._storage.values()

    def domain(self):
        """
        Return an Interval corresponding to the domain of this IntervalDict.

        :return: an Interval.
        """
        return self._klass(self._storage.domain())

    def pop(self, key, default=None):
        """
        Remove key and return the corresponding value if key is not an Interval.
        If key is an interval, it returns an IntervalDict instance.

        This method combines self[key] and del self[key]. If a default value
        is provided and is not None, it uses self.get(key, default) instead of
        self[key].

        :param key: a single value or an Interval instance.
        :param default: optional default value.
        :return: an IntervalDict, or a single value if key is not an Interval.
        """
        if default is None:
            value = self[key]
            del self[key]
            return value
        else:
            value = self.get(key, default)
            try:
                del self[key]
            except KeyError:
                pass
            return value

    def popitem(self):
        """
        Remove and return some (key, value) pair as a 2-tuple.
        Raise KeyError if D is empty.

        :return: a (key, value) pair.
        """
        delete = self._storage.root.maximum
        if delete.is_nil:
            raise KeyError
        else:
            self._storage.delete(delete)
            return delete.interval, delete.value

    def setdefault(self, key, default=None):
        """
        Return given key. If it does not exist, set its value to default and
        return it.

        :param key: a single value or an Interval instance.
        :param default: default value (default to None).
        :return: an IntervalDict, or a single value if key is not an Interval.
        """
        if isinstance(key, Interval):
            value = self.get(key, default)
            self.update(value)
            return value
        else:
            try:
                return self[key]
            except KeyError:
                self[key] = default
                return default

    def update(self, mapping_or_iterable):
        """
        Update current IntervalDict with provided values.

        If a mapping is provided, it must map Interval instances to values (e.g.,
        another IntervalDict). If an iterable is provided, it must consist of a
        list of (key, value) pairs.

        :param mapping_or_iterable: mapping or iterable.
        """
        if isinstance(mapping_or_iterable, Mapping):
            data = mapping_or_iterable.items()
        else:
            data = mapping_or_iterable

        for i, v in data:
            self[i] = v

    def combine(self, other, how):
        """
        Return a new IntervalDict that combines the values from current and
        provided ones.

        If d = d1.combine(d2, f), then d contains (1) all values from d1 whose
        keys do not intersect the ones of d2, (2) all values from d2 whose keys
        do not intersect the ones of d1, and (3) f(x, y) for x in d1, y in d2 for
        intersecting keys.

        :param other: another IntervalDict instance.
        :param how: a function of two parameters that combines values.
        :return: a new IntervalDict instance.
        """
        new_items = []

        dom1, dom2 = self.domain(), other.domain()

        new_items.extend(self[dom1 - dom2].items())
        new_items.extend(other[dom2 - dom1].items())

        intersection = dom1 & dom2
        d1, d2 = self[intersection], other[intersection]

        for i1, v1 in d1.items():
            for i2, v2 in d2.items():
                if i1.overlaps(i2):
                    i = i1 & i2
                    v = how(v1, v2)
                    new_items.append((i, v))

        return self.__class__(new_items)

    def as_dict(self, atomic=False):
        """
        Return the content as a classical Python dict.

        :param atomic: whether keys are atomic intervals.
        :return: a Python dict.
        """
        if atomic:
            d = dict()
            for interval, v in self.items():
                for i in interval:
                    d[i] = v
            return d
        else:
            return dict(self.items())

    def __getitem__(self, key):
        x = self._storage.root
        if isinstance(key, Interval):
            items = []
            for i in key:
                if not (i < x.minimum.interval or i > x.maximum.interval):
                    items.extend(self._storage.search(i))
            return self.__class__._from_items(items)
        else:
            if key < x.minimum.interval or key > x.maximum.interval:
                raise KeyError(key)
            while not x.is_nil:
                if key in x.interval:
                    return x.value
                if x.interval > key:
                    x = x.left
                else:
                    x = x.right
            raise KeyError(key)

    def __setitem__(self, key, value):
        if isinstance(key, Interval):
            interval = key
        else:
            interval = self._klass.from_atomic(Bound.CLOSED, key, key, Bound.CLOSED)
        if interval.empty:
            return
        for i in interval:
            self._storage.insert_interval_value(i, value)

    def __delitem__(self, key):
        if isinstance(key, Interval):
            interval = key
        else:
            interval = self._klass.from_atomic(Bound.CLOSED, key, key, Bound.CLOSED)

        if interval.empty:
            return

        for i in interval:
            if i < self._storage.root.minimum.interval or i > self._storage.root.maximum.interval:
                if not isinstance(key, Interval):
                    raise KeyError(key)
            else:
                self._storage.delete_interval(i)

    def __or__(self, other):
        d = self.copy()
        d.update(other)
        return d

    def __ior__(self, other):
        self.update(other)
        return self

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return self._storage.root.size

    def __contains__(self, key):
        return key in self.domain()

    def __repr__(self):
        return "{}{}{}".format(
            "{",
            ", ".join("{!r}: {!r}".format(i, v) for i, v in self.items()),
            "}",
        )

    def __eq__(self, other):
        if isinstance(other, IntervalDict):
            return self.as_dict() == other.as_dict()
        else:
            return NotImplemented
