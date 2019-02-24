'''
module of pin access
'''
from machine import Pin


class PinOut:
    '''
    pin-out structure
    '''

    _instance = None

    def __new__(cls, *args, **kwargs):
        '''
        class instance

        :param args: ctor arguments
        :param kwargs: ctor arguments
        :return: instance
        '''
        if not cls._instance:
            cls._instance = super(PinOut, cls).__new__(cls)

        return cls._instance

    def __init__(self, pins: dict = None):
        '''
        ctor

        :param pins: dict with bin names and pin ids
        '''
        if pins is None:
            return

        self._pins = {}
        self._pinids = pins
        for name, pin in pins.items():
            pin = Pin(pin, Pin.OUT)
            pin.value(0)
            self._pins[name] = pin

    def __str__(self):
        return str(self._pins)

    def __contains__(self, item):
        return item in self._pins

    def pins(self):
        '''
        returns all key as tuple

        :return: tuple of keys
        '''
        return tuple(self._pins.keys())

    def allup(self):
        '''
        set all pins to high level
        '''

        for i in self._pins.values():
            i.value(1)

    def alldown(self):
        '''
        sets all pins to low level
        '''

        for i in self._pins.values():
            i.value(0)

    def up(self, item):
        '''
        set pin to high level

        :param item: item
        '''

        self._pins.get(item).value(1)

    def down(self, item):
        '''
        set pin to low level

        :param item: item
        '''
        self._pins.get(item).value(0)

    def isup(self, item):
        '''
        returns the flag if the pin is up

        :param item: item
        :return: up level
        '''
        return self._pins.get(item).value() == 1

    def isdown(self, item):
        '''
        returns the flag if the pin is down

        :param item: item
        :return: down level
        '''
        return self._pins.get(item).value() == 0

    def toggle(self, item):
        '''
        toggle pin level

        :param item: item
        '''
        i = self._pins.get(item)
        i.value(int(not i.value()))

    def pindis(self):
        '''
        returns the dict of keys and pin ids

        :return: dict
        '''
        return self._pinids
