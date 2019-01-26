import framebuf
from machine import SPI, Pin


class Max7219Matrix8x8:
    # https://howtomechatronics.com/tutorials/arduino/8x8-led-matrix-max7219-tutorial-scrolling-text-android-control-via-bluetooth/
    # https://www.bastelgarage.ch/index.php?route=extension/d_blog_module/post&post_id=6
    # https://github.com/mcauser/micropython-max7219

    def __init__(self, din: int, cs: int, clk: int, spiid: int = 1, baudrate: int = 10000000):
        self._spi = SPI(spiid, baudrate=baudrate, polarity=1, phase=0, sck=Pin(clk), mosi=Pin(din))
        self._ss = Pin(cs, Pin.OUT)
        self._num = clk

        self._buffer = bytearray(8 * self._num)
        self._frame = framebuf.FrameBuffer(self._buffer, 8 * self._num, 8, framebuf.MONO_HLSB)

    def pixel(self, x: int, y: int):
        self._frame.pixel(x, y)
