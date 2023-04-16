class CustomMeta(type):
    """
    Этот метакласс переопределяет имена атрибутов создаваемого класса
    и его экземпляров. В начале названий всех атрибутов и методов,
    кроме магических, добавляется префикс "custom_". При этом, в данной
    реализации при добавлении атрибутов через
    >> <obj>.__dict__[<'new_attr'>] = <val>
    имя создаваемого атрибута изменяться не будет.
    """

    # переопределение метода __setattr__() для экземпляров
    # создаваемого класса
    def _new_setattr(instance, key, value):
        if not key.startswith("__") and not key.endswith("__"):
            key = "custom_" + key
        instance.__class__.__base__.__setattr__(instance, key, value)

    def __new__(mcs, name, bases, dct, **kwargs):
        new_dct = {}

        # для каждого атрибута создаваeмого класса, который не является
        # магическим методом, подменим имя на 'custom_<старое имя атрибута>'

        for key in dct:
            if not key.startswith("__") and not key.endswith("__"):
                new_dct["custom_" + key] = dct[key]
            else:
                new_dct[key] = dct[key]

        # подменим метод __setattr__ создаваемого класса для переопределения
        # имен атрибутов у экземпляра создаваемого класса

        new_dct["__setattr__"] = mcs._new_setattr

        return super().__new__(mcs, name, bases, new_dct)

    # подменяем имена для динамически добавляемых атрибутов
    # создаваемого класса
    def __setattr__(cls, key, value):
        # обрабатываем случай, когда переопределяется магический метод
        if not key.startswith("__") and not key.endswith("__"):
            key = "custom_" + key
        super().__setattr__(key, value)
