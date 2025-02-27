class Token:
    def __init__(self, type, value, subtype = None):
        self.type = type
        self.value = value
        self.subtype = subtype

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)}, {repr(self.subtype)})'

    def __repr__(self):
        return self.__str__()