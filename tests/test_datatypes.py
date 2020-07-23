from abc import ABC
from collections import UserList
from unittest import TestCase

from datatypes import SemiMutableSequence


class TestDatatype(ABC, TestCase):
    class_ = None
    reference_class = None

    def setUp(self):
        if self.class_ is None:
            self.class_ = self.reference_class


class TestContainer(TestDatatype):
    reference_class = tuple

    def setUp(self):
        super(TestContainer, self).setUp()
        self.data = self.class_()

    def test_contains(self):
        self.assertFalse(object in self.data)


class TestHashable(TestDatatype):
    reference_class = object

    def test_hash(self):
        hash(self.reference_class())


class TestIterable(TestDatatype):
    reference_class = tuple

    def test_iter(self):
        iterator = iter(self.class_())
        self.assertTrue(hasattr(iterator, '__iter__'))
        self.assertTrue(hasattr(iterator, '__next__'))


class TestIterator(TestIterable):
    pass


class TestGenerator(TestIterator):
    pass


class TestSized(TestDatatype):
    reference_class = tuple

    def setUp(self):
        super(TestSized, self).setUp()
        self.data = self.class_()

    def test_len(self):
        length = len(self.data)
        self.assertTrue(isinstance(length, int))


class TestCallable(TestDatatype):
    reference_class = object

    def test_call(self):
        self.assertTrue(callable(self.reference_class))


class TestSequence(TestSized, TestIterable, TestContainer):
    reference_class = tuple

    def setUp(self):
        TestDatatype.setUp(self)
        self.items = 'ABCDE'
        self.data = self.class_(self.items)
        self.reference_data = self.reference_class(self.data)
        self.new_item = 'Z'
        assert self.new_item not in self.items

    def test_contains(self):
        for item in self.data:
            self.assertTrue(item in self.data)
        self.assertFalse(self.new_item in self.data)

    def test_hash(self):
        self.assertNotEqual(hash(self.data), self.class_([self.new_item]))

    def test_iter(self):
        i = 0
        for item in self.data:
            self.assertEqual(item, self.data[i])
            i += 1

    def test_iter_stops(self):
        iterator = iter(self.data)
        with self.assertRaises(StopIteration):
            for _ in range(len(self.data) + 1):
                next(iterator)

        for _ in range(3):
            with self.assertRaises(StopIteration):
                next(iterator)

    def test_repr(self):
        if self.class_ != self.reference_class:
            self.assertEqual(eval(repr(self.data)), self.data)

    def test_len(self):
        self.assertEqual(len(self.data), sum(1 for _ in self.data))
        self.assertEqual(len(self.class_([])), 0)

    def test_lt(self):
        self.assertTrue(self.data[:-1] < self.data)
        self.assertFalse(self.data < self.data[:-1])
        self.assertFalse(self.data < self.data)

    def test_le(self):
        self.assertTrue(self.data[:-1] <= self.data)
        self.assertFalse(self.data <= self.data[:-1])
        self.assertTrue(self.data <= self.data)

    def test_eq(self):
        self.assertTrue(self.data == self.data)
        self.assertFalse(self.data == self.data[:-1])
        self.assertFalse(self.data[:-1] == self.reference_data)

    def test_gt(self):
        self.assertTrue(self.data > self.data[:-1])
        self.assertFalse(self.data[:-1] > self.data)
        self.assertFalse(self.data > self.data)

    def test_ge(self):
        self.assertTrue(self.data >= self.data[:-1])
        self.assertFalse(self.data[:-1] >= self.data)
        self.assertTrue(self.data >= self.data)

    def test_get_item(self):
        for index, item in enumerate(self.data):
            self.assertEqual(self.data[index], self.reference_data[index])

    def test_get_item_missing(self):
        with self.assertRaises(IndexError):
            _ = self.data[len(self.data) + 1]

    def add(self, cls):
        self.reference_data = self.reference_data + self.reference_class([self.new_item])
        self.assertEqual(self.data + cls([self.new_item]), self.reference_data)

    def test_add(self):
        self.add(self.class_)

    def radd(self, cls):
        self.reference_data = self.reference_class([self.new_item]) + self.reference_data
        self.assertEqual(cls([self.new_item]) + self.data, self.reference_data)

    def test_radd(self):
        self.radd(self.class_)

    def test_mul(self):
        multiplier = 2
        self.assertEqual(self.data * multiplier, self.reference_data * multiplier)

    def test_rmul(self):
        multiplicand = 2
        self.assertEqual(multiplicand * self.data, multiplicand * self.reference_data)

    def test_count(self):
        self.assertEqual(self.data.count(self.data[0]), self.reference_data.count(self.reference_data[0]))
        self.assertEqual(self.data.count(self.new_item), 0)

    def test_index(self):
        for index, item in enumerate(self.data):
            self.assertEqual(self.data.index(item), index)

    def test_index_missing(self):
        with self.assertRaises(ValueError):
            self.data.index(self.new_item)


class TestMutableSequence(TestSequence):
    reference_class = list

    def test_hash(self):
        with self.assertRaises(TypeError):
            hash(self.data)

    def test_set_item(self):
        self.data[0] = self.new_item
        self.assertEqual(self.data[0], self.new_item)

    def test_imul(self):
        multiplier = 2
        self.data *= multiplier
        self.reference_data *= multiplier
        self.assertEqual(self.data, self.reference_data)

    def test_insert(self):
        i = 0
        self.data.insert(i, self.new_item)
        self.reference_data.insert(i, self.new_item)
        self.assertEqual(self.data, self.reference_data)

    def test_pop(self):
        last_item = self.data[-1]
        self.assertEqual(self.data.pop(), last_item)
        self.reference_data.pop()
        self.assertEqual(self.data, self.reference_data)

        i = 0
        item = self.data[i]
        self.assertEqual(self.data.pop(i), item)
        self.reference_data.pop(i)
        self.assertEqual(self.data, self.reference_data)

    def test_remove(self):
        item = self.data[0]
        self.data.remove(item)
        self.assertNotEqual(self.data[0], item)

    def test_remove_missing(self):
        with self.assertRaises(ValueError):
            self.data.remove(self.new_item)

    def i_add(self, addition_class):
        self.reference_data += self.reference_class([self.new_item])
        self.data += addition_class([self.new_item])
        self.assertEqual(self.data, self.reference_data)

    def test_iadd(self):
        self.i_add(self.class_)

    def test_del(self):
        short = self.data[:-1]
        del self.data[-1]
        self.assertEqual(self.data, short)

    def test_reverse(self):
        self.data.reverse()
        self.reference_data.reverse()
        self.assertEqual(self.data, self.reference_data)

    def test_sort(self):
        self.data.sort()
        self.reference_data.sort()
        self.assertEqual(self.data, self.reference_data)

    def test_append(self):
        self.data.append(self.new_item)
        self.assertEqual(self.data[-1], self.new_item)

    def test_clear(self):
        self.data.clear()
        self.assertFalse(any(True for _ in self.data))

    def test_copy(self):
        self.assertEqual(self.data.copy(), self.data)
        self.assertIsNot(self.data.copy(), self.data)

    def test_extend(self):
        self.data.extend(self.class_(self.reference_data))
        self.assertEqual(self.data, self.class_(self.items * 2))


class TestUserList(TestMutableSequence):
    reference_class = UserList

    def test_radd(self):
        for cls in [self.class_, list]:
            self.setUp()
            self.radd(cls)

    def test_iadd(self):
        self.i_add(self.class_)
        self.i_add(list)
        self.i_add(tuple)
        self.i_add(type(self.data))

    def test_add(self):
        pass

    def test_delitem(self):
        pass


class TestSemiMutableSequence(TestUserList):
    class_ = SemiMutableSequence

    def test_set_item(self):
        index = 0
        with self.assertRaises(TypeError):
            self.data[index] = self.new_item
        self.data[index] = self.new_item
        self.assertEqual(self.data[index], self.new_item)

    def test_set_item_n(self):
        index = 0
        self.data.times = 3
        for _ in range(self.data.times - 1):
            with self.assertRaises(TypeError):
                self.data[index] = self.new_item
        # nth time's a charm
        self.data[index] = self.new_item
        self.assertEqual(self.data[index], self.new_item)
