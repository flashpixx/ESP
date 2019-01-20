from component.config import Config
from component.pinout import PinOut
from component.systemglobal import SystemGlobal


# --- initialization ---
print('--- booting & initialization ---')
c = Config()

if not c.get("debug", False):
    SystemGlobal.debugoff()

if 'ssid' in c and 'password' in c:
    SystemGlobal.wifi_connect( c.ssid, c.password, c.hostname )

PinOut({'white': 2, 'blue': 4, 'yellow': 16})
