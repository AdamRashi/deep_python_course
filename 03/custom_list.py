from collections import UserList
from itertools import zip_longest


class CustomList(UserList):
    def __add__(self, other):
        if isinstance(other, CustomList):
            other = other.data
        elif not isinstance(other, list):
            raise TypeError(
                f"Can not add element of type {type(other)} with CustomList"
            )

        if not other:
            return CustomList(self.data.copy())
        result = []
        for elem_x, elem_y in zip_longest(self.data, other, fillvalue=0):
            result.append(elem_x + elem_y)
        return CustomList(result)

    def __radd__(self, other):
        try:
            return self + other
        except TypeError as err:
            raise TypeError(
                "Can not add element of "
                "CustomList with element of "
                f" {type(other)}"
            ) from err

    def __sub__(self, other):
        if isinstance(other, CustomList):
            other = other.data
        elif not isinstance(other, list):
            raise TypeError(
                f"Can not subtract element of type {type(other)} from CustomList"
            )

        if not other:
            return CustomList(self.data.copy())
        result = []
        for elem_x, elem_y in zip_longest(self.data, other, fillvalue=0):
            result.append(elem_x - elem_y)
        return CustomList(result)

    def __rsub__(self, other):
        if isinstance(other, CustomList):
            other = other.data
        elif not isinstance(other, list):
            raise TypeError(
                "Can not subtract element of "
                "CustomList from element of "
                f"type {type(other)}"
            )
        if not other:
            return CustomList([-elem_x for elem_x in self.data])
        result = []
        for elem_x, elem_y in zip_longest(other, self.data, fillvalue=0):
            result.append(elem_x - elem_y)
        return CustomList(result)

    def __lt__(self, other):
        if issubclass(type(other), CustomList):
            return sum(self.data) < sum(other.data)
        raise TypeError(
            "'<' not supported between instances of " f"{type(self)} and {type(other)}"
        )

    def __le__(self, other):
        if issubclass(type(other), CustomList):
            return sum(self.data) <= sum(other.data)
        raise TypeError(
            "'<=' not supported between instances of " f"{type(self)} and {type(other)}"
        )

    def __eq__(self, other):
        if issubclass(type(other), CustomList):
            return sum(self.data) == sum(other.data)
        raise TypeError(
            "'==' not supported between instances of "
            f"{self.__class__.__name__} and "
            f"{other.__class__.__name__}"
        )

    def __ne__(self, other):
        if issubclass(type(other), CustomList):
            return sum(self.data) != sum(other.data)
        raise TypeError(
            "'!=' not supported between instances of " f"{type(self)} and {type(other)}"
        )

    def __gt__(self, other):
        if issubclass(type(other), CustomList):
            return sum(self.data) > sum(other.data)
        raise TypeError(
            "'>' not supported between instances of " f"{type(self)} and {type(other)}"
        )

    def __ge__(self, other):
        if issubclass(type(other), CustomList):
            return sum(self.data) >= sum(other.data)
        raise TypeError(
            "'>=' not supported between instances of " f"{type(self)} and {type(other)}"
        )

    def __str__(self):
        return f"CustomList({self.data}, sum = {sum(self.data)})"

    def __repr__(self):
        return f"CustomList({self.data}, sum = {sum(self.data)})"
