class DotMatrix:
    # https://howtomechatronics.com/tutorials/arduino/8x8-led-matrix-max7219-tutorial-scrolling-text-android-control-via-bluetooth/
    # https://www.bastelgarage.ch/index.php?route=extension/d_blog_module/post&post_id=6

    def __init__(self, rows:int, cols:int):
        self._rows = rows
        self._cols = cols
