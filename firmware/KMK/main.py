import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.scanners import DiodeOrientation
from kmk.extensions.RGB import RGB
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys


layers = Layers()

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP26, board.GP27, board.GP28)
keyboard.row_pins = (board.GP4, board.GP2, board.GP1)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

rgb = RGB(pixel_pin=board.GP11, num_pixels=16)
keyboard.extensions.append(rgb)

display = Display(
    display=SSD1306(sda=board.GP6, scl=board.GP7),
    entries=[
        TextEntry(text='>:3c "hehe"', x=0, y=0), 
        TextEntry(text='randompad', x=0, y=10),
        TextEntry(text='KMK Firmware', x=0, y=20),
    ],
    height=32
)
keyboard.extensions.append(display)

media_keys = MediaKeys()
keyboard.extensions.append(media_keys)

encoder_handler = EncoderHandler()
encoder_handler.divisor = 2
encoder_handler.pins = ((board.GP29, board.GP0, None),)
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.NO),),
]
keyboard.modules.append(encoder_handler)
keyboard.modules.append(layers)


def update_display_on_press(key):
    def _update_display(keyboard):
        display.display.fill(0)
        display.display.text(key, 0, 0)
        display.display.show()
    return _update_display


def clear_display(keyboard):
    display.display.fill(0)
    display.display.show()


COPY = KC.MACRO(on_press=update_display_on_press('Copy'), on_release=clear_display, macro=(KC.LCTL(KC.C)))
PASTE = KC.MACRO(on_press=update_display_on_press('Paste'), on_release=clear_display, macro=(KC.LCTL(KC.V)))
CUT = KC.MACRO(on_press=update_display_on_press('Cut'), on_release=clear_display, macro=(KC.LCTL(KC.X)))
LOCK = KC.MACRO(on_press=update_display_on_press('Lock'), on_release=clear_display, macro=(KC.LGUI(KC.L)))
RESTART = KC.MACRO(on_press=update_display_on_press('Restart'), on_release=clear_display, macro=(KC.LGUI(KC.R)))
SHUTDOWN = KC.MACRO(on_press=update_display_on_press('Shutdown'), on_release=clear_display, macro=(KC.LALT(KC.F4), KC.ENTER))
PREV_TRACK = KC.MACRO(on_press=update_display_on_press('Previous'), on_release=clear_display, macro=(KC.MPRV))
PLAY_PAUSE = KC.MACRO(on_press=update_display_on_press('Play/Pause'), on_release=clear_display, macro=(KC.MPLY))
NEXT_TRACK = KC.MACRO(on_press=update_display_on_press('Next'), on_release=clear_display, macro=(KC.MNXT))




















keyboard.keymap = [
    [COPY,    PASTE, CUT],
    [LOCK,   RESTART, SHUTDOWN],
    [PREV_TRACK,   PLAY_PAUSE, NEXT_TRACK],
]

if __name__ == '__main__':
    keyboard.go()