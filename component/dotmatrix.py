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
        self._matrix = {}
        self._spi = 1

    def bind(self,
             name: str,
             width: int,
             height: int,
             cs: int,
             din: int = None,
             clk: int = None,
             rotate_180=False,
             baudrate: int = 10000000,
             polarity: int = 0,
             phase: int = 0):
        self._matrix[name] = self._Max7219(width, height, cs, din, clk, rotate_180, self._spi, baudrate, polarity, phase)
        self._spi += 1

    def unbind(self, name: str):
        del self._matrix[name]

    def fill(self, c: int=0, name: str = None):
        self._caller(lambda m: m.fill(c), name)

    def pixel(self, x: int, y: int, c: int, name: str = None):
        self._caller(lambda m: m.pixel(x, y, c), name)

    def hline(self, x: int, y: int, w: int, c: int, name: str = None):
        self._caller(lambda m: m.hline(x, y, w, c), name)

    def vline(self, x: int, y: int, h: int, c: int, name: str = None):
        self._caller(lambda m: m.vline(x, y, h, c), name)

    def line(self, x1: int, y1: int, x2: int, y2: int, c: int, name: str = None):
        self._caller(lambda m: m.line(x1, y1, x2, y2, c), name)

    def rect(self, x: int, y: int, w: int, h: int, c: int, name: str = None):
        self._caller(lambda m: m.rect(x, y, w, h, c), name)

    def fill_rect(self, x: int, y: int, w: int, h: int, c: int, name: str = None):
        self._caller(lambda m: m.fill_rect(x, y, w, h, c), name)

    def text(self, s: str, x: int, y: int, c: int = 1, name: str = None, encoding: str = 'latin1'):
        self._caller(lambda m: m.text(s.encode(encoding), x, y, c), name)

    def brightness(self, value:int, name: str = None):
        self._caller(lambda i: i.brightness(value), name)

    def reset(self, name:str = None):
        self._caller(lambda m: m.reset(), name)

    def update(self, name: str = None):
        self._caller(lambda m: m(), name)

    def _caller(self, call, name:str = None):
        if name is None:
            for i in self._matrix.values():
                call(i)
        else:
            call(self._matrix[name])

    def __iter__(self):
        return self._matrix.keys().__iter__()

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
