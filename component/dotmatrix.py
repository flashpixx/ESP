from typing import Any

import framebuf
from machine import SPI, Pin
from micropython import const

class DotMatrix:

    _instance = None

    def __new__(cls, *args, **kwargs):
        '''
        class instance

        :param args: ctor arguments
        :param kwargs: ctor arguments
        :return: instance
        '''
        if not cls._instance:
            cls._instance = super(DotMatrix, cls).__new__(cls)

        return cls._instance


    def __init__(self):
        self._matrix = dict()

    def create(self,
            name: str,
            width: int,
            height: int,
            cs: int,
            din: int = None,
            clk: int = None,
            rotate_180=False,
            spiid: int = 1,
            baudrate: int = 10000000,
            polarity: int = 0,
            phase: int = 0):
        self._matrix[name.replace(' ', '')] = self._Max7219(width, height, cs, din, clk, rotate_180, spiid, baudrate, polarity, phase)

    def fill(self, name: str, c: int):
        self._matrix[name].fill(c)

    def pixel(self, name: str, x: int, y: int, c: int):
        self._matrix[name].pixel(x, y, c)

    def hline(self, name: str, x: int, y: int, w: int, c: int):
        self._matrix[name].hline(x, y, w, c)

    def vline(self, name: str, x: int, y: int, h: int, c: int):
        self._matrix[name].vline(x, y, h, c)

    def line(self, name: str, x1: int, y1: int, x2: int, y2: int, c: int):
        self._matrix[name].line(x1, y1, x2, y2, c)

    def rect(self, name: str, x: int, y: int, w: int, h: int, c: int):
        pass

    def fill_rect(self, name: str, x: int, y: int, w: int, h: int, c: int):
        self._matrix[name].fill(x, y, w, h, c)

    def text(self, name: str, s: str, x: int, y: int, c: int = 1, encoding: str='latin1'):
        self._matrix[name].text(s.encode(encoding), x, y, c)


    class _Max7219(framebuf.FrameBuffer):
        # https://howtomechatronics.com/tutorials/arduino/8x8-led-matrix-max7219-tutorial-scrolling-text-android-control-via-bluetooth/
        # https://www.bastelgarage.ch/index.php?route=extension/d_blog_module/post&post_id=6
        # https://github.com/mcauser/micropython-max7219
        # https://github.com/adafruit/Adafruit_CircuitPython_MAX7219
        # https://github.com/vrialland/micropython-max7219

        _DIGIT_0 = const(0x1)

        _DECODE_MODE = const(0x9)
        _NO_DECODE = const(0x0)

        _INTENSITY = const(0xa)
        _INTENSITY_MIN = const(0x0)

        _SCAN_LIMIT = const(0xb)
        _DISPLAY_ALL_DIGITS = const(0x7)

        _SHUTDOWN = const(0xc)
        _SHUTDOWN_MODE = const(0x0)
        _NORMAL_OPERATION = const(0x1)

        _DISPLAY_TEST = const(0xf)
        _DISPLAY_TEST_NORMAL_OPERATION = const(0x0)

        _MATRIX_SIZE = const(8)

        def __init__(self,
                     width: int,
                     height: int,
                     cs: int,
                     din: int = None,
                     clk: int = None,
                     rotate_180=False,
                     spiid: int = 1,
                     baudrate: int = 10000000,
                     polarity: int = 0,
                     phase: int = 0):

            self._width = width
            self._height = height

            self._cols = width // _MATRIX_SIZE
            self._rows = height // _MATRIX_SIZE
            self._nb_matrices = self._cols * self._rows

            self._spi = SPI(spiid, mosi=None if din is None else Pin(din), sck=None if clk is None else Pin(clk), baudrate=baudrate, polarity=polarity,
                            phase=phase)
            self._cs = Pin(cs, Pin.OUT)
            self._rotate_180 = rotate_180

            # 1 bit per pixel (on / off) -> 8 bytes per matrix
            self.buffer = bytearray(width * height // 8)
            format = framebuf.MONO_HLSB if not self._rotate_180 else framebuf.MONO_HMSB
            super().__init__(self.buffer, width, height, format)

            self._initdisplay()

        def _initdisplay(self):
            '''
            initialize display
            '''
            for command, data in (
                    # Prevent flash during init
                    (_SHUTDOWN, _SHUTDOWN_MODE),
                    (_DECODE_MODE, _NO_DECODE),
                    (_DISPLAY_TEST, _DISPLAY_TEST_NORMAL_OPERATION),
                    (_INTENSITY, _INTENSITY_MIN),
                    (_SCAN_LIMIT, _DISPLAY_ALL_DIGITS),
                    (_SHUTDOWN, _NORMAL_OPERATION),
            ):
                self._push(command, data)

            self.reset()

        def _push(self, command, data):
            '''
            push command to the display

            :param command: command index
            :param data: command data
            '''
            cmd = bytearray([command, data])
            self._cs(0)
            for matrix in range(self._nb_matrices):
                self._spi.write(cmd)
            self._cs(1)

        def brightness(self, value):
            '''
            Set display brightness (0 to 15)
            :param value:
            :return:
            '''
            if not 0 <= value < 16:
                raise ValueError('Brightness must be between 0 and 15')
            self._push(_INTENSITY, value)

        def reset(self):
            '''
            resets the matrix
            :return:
            '''
            self.fill(0)
            self()

        def __call__(self):
            '''
            update
            '''

            # Write line per line on the matrices
            for line in range(8):
                self._cs(0)

                for matrix in range(self._nb_matrices):
                    # Guess where the matrix is placed
                    row, col = divmod(matrix, self._cols)
                    # Compute where the data starts
                    if not self._rotate_180:
                        offset = row * 8 * self._cols
                        index = col + line * self._cols + offset
                    else:
                        offset = 8 * self._cols - row * self._cols * 8 - 1
                        index = self._cols * (8 - line) - col + offset

                    self._spi.write(bytearray([_DIGIT_0 + line, self.buffer[index]]))

                self._cs(1)