class Rating:
    """
    Дескриптор, который принимает в качестве значения
    только числа в интервале [0; 10], с точностью не более
    одного знака после запятой. Примеры:
    - 3, 9.99999, 5.0, 7.8999 - подходит
    - False, 'abc', 11, -1 - не подходит
    """

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0.0)

    def __set__(self, instance, value):
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            raise TypeError("The value of rating should be a number")

        if not 0 <= value <= 10:
            raise ValueError("The value of rating must be in interval [0;10]")

        instance.__dict__[self.name] = round(float(value), 1)


class Director:
    """
    Дескриптор, который принимает в качестве значения только строки, состоящие
    из букв алфавита, пробелов и некоторых знаков пунктуации (,.'). При этом
    каждое слово в строке должно начинаться с заглавной буквы. Примеры:
    - Marta Smith, Robert Downey Jr., Mr's Somewhat - подходят
    - George lucas, 50 CENT, 2Pac - не подходят
    """

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Name of the director must be a string")

        allowed_chars = " '.,"
        if not (
            value.translate(str.maketrans("", "", allowed_chars)).isalpha()
            and value.istitle()
        ):
            raise ValueError(
                "Director's name must start with capital letter"
                "and consist of alphabetic characters "
            )
        instance.__dict__[self.name] = value


class Actors:
    """
    Дескриптор, который принимает в качестве значения только списки имён
    актёров, который валидируются по тому же принципу, что и имя режиссёра
    """

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, [])

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise TypeError("Actors must be a list")
        for name in value:
            if not isinstance(name, str):
                raise TypeError("All actors' names must be strings")
            allowed_chars = " '.,"
            if (
                not name.translate(str.maketrans("", "", allowed_chars)).isalpha()
                or not name.istitle()
            ):
                raise ValueError(
                    "All actors' names must consist of "
                    "alphabetic characters and start "
                    "with a capital letter"
                )
        instance.__dict__[self.name] = value
