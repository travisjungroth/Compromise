import math
from numbers import Rational


def number_decorate(func):
    def number_wrapper(*args, **kwargs):
        return Number(func(*args, **kwargs))
    return number_wrapper


def about(number):
    return Number(float(number.value))


def point(number):
    return Number(number.value / 10 ** (int(math.log10(number.value)) + 1))


class Number(Rational):
    names_list = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']
    names = {i: name for i, name in enumerate(names_list)}

    def __init__(self, value):
        if isinstance(value, Number):
            value = value.value
        self.value = value

    def __complex__(self):
        return compile(self.value)

    def __bool__(self):
        return bool(self.value)

    @number_decorate
    def __add__(self, other):
        return self.value + other

    @number_decorate
    def __radd__(self, other):
        return other + self.value

    @number_decorate
    def __neg__(self):
        return -self.value

    @number_decorate
    def __pos__(self):
        return +self.value

    @number_decorate
    def __mul__(self, other):
        return self.value * other

    @number_decorate
    def __rmul__(self, other):
        return other * self.value

    @number_decorate
    def __truediv__(self, other):
        return self.value / other

    @number_decorate
    def __rtruediv__(self, other):
        return other / self.value

    @number_decorate
    def __pow__(self, power):
        return self.value**power

    @number_decorate
    def __rpow__(self, base):
        return base ** self.value

    @number_decorate
    def __abs__(self):
        return abs(self.value)

    @number_decorate
    def conjugate(self):
        return self.value.conjugate()

    def __eq__(self, other):
        return self.value == other

    def __float__(self):
        return float(self.value)

    @number_decorate
    def __trunc__(self):
        return math.trunc(self.value)

    @number_decorate
    def __floor__(self):
        return math.floor(self.value)

    @number_decorate
    def __ceil__(self):
        return math.ceil(self.value)

    @number_decorate
    def __round__(self, n=None):
        return round(self.value, n)

    @number_decorate
    def __floordiv__(self, other):
        return self.value // other

    @number_decorate
    def __rfloordiv__(self, other):
        return other // self.value

    @number_decorate
    def __mod__(self, other):
        return other % self.value

    @number_decorate
    def __rmod__(self, other):
        return self.value % other

    @number_decorate
    def __lt__(self, other):
        return self.value < other

    @number_decorate
    def __le__(self, other):
        return self.value <= other

    @number_decorate
    def __gt__(self, other):
        return self.value > other

    @number_decorate
    def __ge__(self, other):
        return self.value >= other

    @number_decorate
    def numerator(self):
        return self.value.numerator

    @number_decorate
    def denominator(self):
        return self.value.denominator

    def __int__(self):
        return int(self.value)

    def __repr__(self):
        return repr(self.value)

    @number_decorate
    def __and__(self, other):
        if 0 < other < 1:
            return self.value + other
        else:
            return self.value * 10 + other


ZERO = Number(0)
ONE = Number(1)
TWO = Number(2)
THREE = Number(3)
FOUR = Number(4)
FIVE = Number(5)
SIX = Number(6)
SEVEN = Number(7)
EIGHT = Number(8)
NINE = Number(9)
