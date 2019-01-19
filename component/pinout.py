class PinOut:
    '''
    pin out structure
    '''

    __instance = None

    def __new__(cls, **args):
        from machine import Pin

        if PinOut.__instance is None:
            PinOut.__instance = object.__new__(cls)

        PinOut.__instance._pins = {}
        for name, pin in args:
            PinOut.__instance.__pins[name] = Pin(pin, Pin.OUT)

        return PinOut.__instance

    def __str__(self):
        return str(self.__instance)

    def __contains__(self, item):
        return item in self.__instance._pins

    def up(self, item):
        self.__instance._pins.get(item).value(1)

    def down(self, item):
        self.__instance._pins.get(item).value(0)
