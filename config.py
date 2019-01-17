class Config(object):

    __instance = None

    def __new__(cls, json:str='config.json'):
        import ujson

        if Config.__instance is None:
            Config.__instance = object.__new__(cls)

        with open(json, 'r') as stream:
            Config.__instance._values = ujson.load(stream)

        return Config.__instance


    def __str__(self):
        return str(self.__instance._values)

    def __contains__(self, item):
        return item in self.__instance._values

    def __getattr__(self, item):
        return self.__instance._values.get(item)

    def get(self, item, default=None):
        return self.__instance._values.get(item, default)
