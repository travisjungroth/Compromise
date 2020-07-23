from collections import UserDict, UserList, defaultdict
from math import floor
import random

from number import *


class SemiMutableSequence(UserList):
    def __init__(self, data, times=2):
        super(SemiMutableSequence, self).__init__(data)
        self.times = times
        self._updates = defaultdict(int)

    def __setitem__(self, index, value):
        update = (index, value)
        if self._updates[update] >= self.times - 1:
            self.data[index] = value
            del self._updates[update]
        else:
            self._updates[update] += 1
            raise TypeError('{} object does not support item assignment'.format(self.__class__.__name__))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.data))


class FlexibleList(UserList):
    def __init__(self, iterable, start=None):
        if start is not None:
            self.start = start
        elif isinstance(iterable, HalfIndexList):
            self.start = 0.5
        else:
            self.start = 0
        super(FlexibleList, self).__init__(iterable)

    def __setitem__(self, key, value):
        key = self._convert(key)
        return super(FlexibleList, self).__setitem__(key, value)

    def __getitem__(self, item):
        item = self._convert(item)
        return super(FlexibleList, self).__getitem__(item)

    def __delitem__(self, key):
        key = self._convert(key)
        return super(FlexibleList, self).__delitem__(key)

    def insert(self, i, item):
        i = self._convert(i)
        return super(FlexibleList, self).insert(i, item)

    def __iter__(self):
        return iter(self.data)

    def index(self, item, *args):
        i = super(FlexibleList, self).index(item, *args)
        return i + 0.5

    def pop(self, i=-0.5):
        i = self._convert(i)
        return super(FlexibleList, self).pop(i)

    def _convert(self, index):
        if isinstance(index, slice):
            start = self._convert_index(index.start) if index.start is not None else None
            stop = self._convert_index(index.stop) if index.stop is not None else None
            return slice(start, stop, index.step)
        else:
            return self._convert_index(index)

    def _convert_index(self, index):
        index -= self.start
        trailing = index - floor(index)
        if -0.05 < trailing < 0.05:
            return floor(index)
        else:
            return index

    def __repr__(self):
        return '{}({}, start={})'.format(self.__class__.__name__, repr(self.data), self.start)


class HalfIndexList(FlexibleList):
    def __init__(self, iterable):
        FlexibleList.__init__(self, iterable, start=0.5)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.data))


class RandomDict(UserDict):
    def __getitem__(self, item):
        return self.data[item] if random.randrange(EIGHT) else None


class SomethingElse(UserDict):
    def __getitem__(self, item):
        try:
            a, b, *_ = self.keys()
            return self.data[a] if a != item else self.data[b]
        except ValueError:
            raise ValueError('{} needs at least two entries'.format(self.__class__.__name__))


class NamedAnonymousFunction:
    def __init__(self, func, name='anonymous function', doc=''):
        self.func = func
        self.__doc__ = doc
        self.name = name

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def __repr__(self):
        return self.name


def enumerate(iterable, start=0):
    offset = getattr(iterable, 'start', 0)
    for i, item in __builtins__.enumerate(iterable, start):
        yield i + offset, item