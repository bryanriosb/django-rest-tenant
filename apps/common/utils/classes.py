class CustomDict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value