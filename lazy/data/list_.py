from abc import ABCMeta, abstractmethod

from lazy._thunk import strict
from lazy.utils import singleton


class LazyList(metaclass=ABCMeta):
    def __repr__(self):
        return repr(strict(self))

    def __str__(self):
        return str(strict(self))

    @abstractmethod
    def __strict__(self):
        raise NotImplementedError('__strict__')

    @abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError('__getitem__')

    @abstractmethod
    def __len__(self, key):
        raise NotImplementedError('__len__')

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError('__iter__')


@singleton
class NilType(LazyList):
    def __init__(self):
        pass

    @property
    def __strict__(self):
        return ()

    def __getitem__(self, key):
        raise IndexError('LazyList index out of range')

    def __len__(self):
        return 0

    def __iter__(self):
        return iter(())

nil = NilType()


class Cons(LazyList):
    def __init__(self, car, cdr):
        self._car = car
        self._cdr = cdr

    @property
    def __strict__(self):
        return self._normal_form()

    def _normal_form(self):
        ns = (self._car,) + strict(self._cdr)
        self._normal_form = lambda: ns
        return ns

    def __getitem__(self, key):
        key = strict(key.__index__())
        if key < 0:
            key = len(self) + key

        if key == 0:
            return self._car
        else:
            return self._cdr[key - 1]

    def __len__(self):
        return len(strict(self))

    def __iter__(self):
        a = self
        while not isinstance(a, NilType):
            yield a._car
            a = a._cdr
