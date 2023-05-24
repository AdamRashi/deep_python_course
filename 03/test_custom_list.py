import random
from itertools import zip_longest
from unittest import TestCase

from custom_list import CustomList


class TestCustomList(TestCase):
    def setUp(self) -> None:
        self.int_lst_1 = CustomList([random.randint(0, 100) for _ in range(10)])
        self.int_lst_2 = CustomList([random.randint(0, 100) for _ in range(10)])

        self.float_lst_1 = CustomList([random.random() for _ in range(10)])
        self.float_lst_2 = CustomList([random.random() for _ in range(10)])

    def test_addition(self):
        # при проверке через assertEqual проверяем равенство внутренних списков,
        # иначе будет проверяться равенство сумм элементов

        # сложение двух списков заданного размера
        expected_result = [
            x_val + y_val
            for x_val, y_val in zip_longest(
                self.float_lst_1.data,
                self.float_lst_2.data,
            )
        ]
        self.assertEqual((self.float_lst_1 + self.float_lst_2).data, expected_result)

        expected_result = [
            x_val + y_val
            for x_val, y_val in zip_longest(
                self.int_lst_1.data,
                self.int_lst_2.data,
            )
        ]
        self.assertEqual((self.int_lst_1 + self.int_lst_2).data, expected_result)

        self.assertEqual((self.int_lst_1 + CustomList()).data, self.int_lst_1.data)

        self.assertEqual((CustomList([1]) + CustomList([2, 5])).data, [3, 5])
        self.assertEqual((CustomList([1]) + [2, 5]).data, [3, 5])
        self.assertEqual((CustomList([1]) + []).data, [1])

    def test_right_addition(self):
        # test __radd__
        self.assertEqual(([] + self.int_lst_1).data, self.int_lst_1.data)

        self.assertEqual(([2, 5] + CustomList([1, 3])).data, [3, 8])

        self.assertEqual(([2] + CustomList([1])).data, [3])

        self.assertEqual(([2, 3, 7] + CustomList([1])).data, [3, 3, 7])

    def test_basic_addition(self):
        with self.assertRaises(TypeError):
            _ = self.int_lst_1 + 1

        with self.assertRaises(TypeError):
            _ = None + self.int_lst_1

        with self.assertRaises(TypeError):
            _ = self.int_lst_1 + "string"

        # проверка того, что при сложении создается новый объект
        some_custom_list = CustomList()
        self.assertFalse(some_custom_list is (some_custom_list + self.int_lst_1))
        self.assertFalse(some_custom_list is (self.int_lst_1 + some_custom_list))
        self.assertFalse(some_custom_list is ([] + some_custom_list))
        self.assertFalse(some_custom_list is (some_custom_list + []))
        self.assertFalse(some_custom_list is ([1, 2, 4] + some_custom_list))
        self.assertFalse(some_custom_list is (some_custom_list + [3, 4, 5]))

    def test_subtraction(self):
        # вычитание с кастомными списками одинакового размера
        expected_result = [
            x_val - y_val
            for x_val, y_val in zip_longest(
                self.float_lst_1.data,
                self.float_lst_2.data,
            )
        ]
        self.assertEqual((self.float_lst_1 - self.float_lst_2).data, expected_result)

        expected_result = [
            x_val - y_val
            for x_val, y_val in zip_longest(
                self.int_lst_1.data,
                self.int_lst_2.data,
            )
        ]
        self.assertEqual((self.int_lst_1 - self.int_lst_2).data, expected_result)

        # вычитание списков другого размера
        some_custom_list = CustomList([1, 2, 3])
        self.assertEqual((some_custom_list - CustomList([2])).data, [-1, 2, 3])
        self.assertEqual(
            (some_custom_list - CustomList([2, 5, 4, 7])).data, [-1, -3, -1, -7]
        )
        self.assertEqual((some_custom_list - [2]).data, [-1, 2, 3])
        self.assertEqual((some_custom_list - [2, 5, 4, 7]).data, [-1, -3, -1, -7])

        # вычитание пустых списков
        self.assertEqual((self.int_lst_1 - []).data, self.int_lst_1.data)

        self.assertEqual((self.int_lst_1 - CustomList()).data, self.int_lst_1.data)

    def test_right_subtraction(self):
        lst = list(range(10))
        expected_result = [
            x_val - y_val
            for x_val, y_val in zip_longest(
                lst,
                self.int_lst_2.data,
            )
        ]

        # вычитание из списка того же размера
        self.assertEqual((lst - self.int_lst_2).data, expected_result)

        # вычитание из списка другого размера
        some_custom_list = CustomList([1, 2, 3])
        self.assertEqual(([1] - some_custom_list).data, [0, -2, -3])
        self.assertEqual(([3, 2] - some_custom_list).data, [2, 0, -3])
        self.assertEqual(([5, 3, 2, 7] - some_custom_list).data, [4, 1, -1, 7])

        # вычитание из пустых списков
        expected_result = [-x_val for x_val in self.int_lst_2.data]
        self.assertEqual(([] - self.int_lst_2).data, expected_result)
        self.assertEqual((CustomList() - self.int_lst_2).data, expected_result)

    def test_basic_subtraction(self):
        with self.assertRaises(TypeError):
            _ = self.int_lst_1 - 1

        with self.assertRaises(TypeError):
            _ = None - self.int_lst_1

        # проверка того, что при вычитании создается новый объект
        some_custom_list = CustomList()
        self.assertFalse(some_custom_list is (some_custom_list - self.int_lst_1))
        self.assertFalse(some_custom_list is (self.int_lst_1 - some_custom_list))
        self.assertFalse(some_custom_list is ([] - some_custom_list))
        self.assertFalse(some_custom_list is (some_custom_list - []))
        self.assertFalse(some_custom_list is ([1, 2, 4] - some_custom_list))
        self.assertFalse(some_custom_list is (some_custom_list - [3, 4, 5]))

    def test_equal(self):
        list1 = CustomList([1, 2, 3])  # 6
        list2 = CustomList([4, 5, 6])  # 15
        list3 = CustomList([7, -1])  # 6
        list4 = CustomList([4, 2, 0])  # 6
        self.assertEqual(list1, list3)
        self.assertEqual(list1, list4)
        self.assertNotEqual(list1, list2)

    def test_greater_than(self):
        list1 = CustomList([1, 2, 3])  # 6
        list2 = CustomList([4, 5, 6])  # 15
        list3 = CustomList([15])  # 15
        self.assertGreater(list2, list1)
        self.assertGreater(list3, list1)
        self.assertGreaterEqual(list2, list1)
        self.assertGreaterEqual(list2, list3)

    def test_less_than(self):
        list1 = CustomList([1, 2, 3])  # 6
        list2 = CustomList([4, 5, 6])  # 15
        list3 = CustomList([15])  # 15
        self.assertLess(list1, list2)
        self.assertLess(list1, list3)
        self.assertLessEqual(list1, list2)
        self.assertLessEqual(list2, list3)

    def test_invalid_operators(self):
        a_lst = CustomList([10])
        with self.assertRaises(TypeError):
            _ = a_lst == 10

        with self.assertRaises(TypeError):
            _ = a_lst != 10

        with self.assertRaises(TypeError):
            _ = a_lst <= 10

        with self.assertRaises(TypeError):
            _ = a_lst >= 10

        with self.assertRaises(TypeError):
            _ = a_lst > 10

        with self.assertRaises(TypeError):
            _ = a_lst < 10

    def test_print(self):
        custom_lst = CustomList([5, 1, 3, 7])
        self.assertTrue(
            f"{custom_lst = }" == "custom_lst = CustomList([5, 1, 3, 7], sum = 16)"
        )

    def test_str(self):
        self.assertEqual(
            str(CustomList([5, 1, 3, 7])), "CustomList([5, 1, 3, 7], sum = 16)"
        )

        self.assertEqual(str(CustomList([])), "CustomList([], sum = 0)")
