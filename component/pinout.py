'''
module of pin access
'''

from machine import Pin

class PinOut:
    '''
    pin-out structure
    '''

    __instance = None

    def __new__(cls, pins: dict = None):
        if PinOut.__instance is None:
            PinOut.__instance = object.__new__(cls)

            PinOut.__instance._pinids = pins
            PinOut.__instance._pins = {}
            for name, pin in pins.items():
                p = Pin(pin, Pin.OUT)
                p.value(0)
                PinOut.__instance._pins[name] = p

        return PinOut.__instance

    def __str__(self):
        return str(self.__instance)

    def __contains__(self, item):
        return item in self.__instance._pins

    def pins(self):
        '''
        returns all key as tuple

        :return: tuple of keys
        '''
        return tuple(self.__instance._pins.keys())

    def allup(self):
        '''
        set all pins to high level
        '''

        for i in self.__instance._pins.values():
            i.value(1)

    def alldown(self):
        '''
        sets all pins to low level
        '''

        for i in self.__instance._pins.values():
            i.value(0)

    def up(self, item):
        '''
        set pin to high level

        :param item: item
        '''

        self.__instance._pins.get(item).value(1)

    def down(self, item):
        '''
        set pin to low level

        :param item: item
        '''
        self.__instance._pins.get(item).value(0)

    def isup(self, item):
        '''
        returns the flag if the pin is up

        :param item: item
        :return: up level
        '''
        return self.__instance._pins.get(item).value() == 1

    def isdown(self, item):
        '''
        returns the flag if the pin is down

        :param item: item
        :return: down level
        '''
        return self.__instance._pins.get(item).value() == 0

    def toggle(self, item):
        '''
        toggle pin level

        :param item: item
        '''
        i = self.__instance._pins.get(item)
        i.value(int(not i.value()))

    def pindis(self):
        '''
        returns the dict of keys and pin ids

        :return: dict
        '''
        return self.__instance._pinids
