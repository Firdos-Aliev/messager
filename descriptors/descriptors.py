class Port:
    """Класс-дескриптор для порта"""
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if isinstance(value, int):
            if value < 0:
                raise ValueError('Должно быть число больше 0')
            if value > 65535:
                raise ValueError('Должно быть число меньше 65535')
            instance.__dict__[self.name] = value
        else:
            raise ValueError("Не числового типа")

    def __set_name__(self, owner, name):
        self.name = name
