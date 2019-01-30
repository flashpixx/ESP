from component.config import Config
from component.pinout import PinOut

# --- initialization ---
from component.system import debugoff, wifi_connect, wifi_accesspoint

print('--- booting & initialization ---')
c = Config()

if not c.get("debug", False):
    debugoff()

if 'ssid' in c and 'password' in c:

    if c.get('accesspoint', True):
        wifi_accesspoint(
            ssid=c.ssid,
            password=c.password,
            ip=c.get('ip', '192.168.100.1'),
            netmask=c.get('netmask', '255.255.255.0'),
            gateway=c.get('gateway', '0.0.0.0'),
            dns=c.get('dns', '0.0.0.0'),
            channel=c.get('channel', None),
            hidden=c.get('hidden', False),
            hostname=c.hostname
        )
    else:
        wifi_connect(
            ssid=c.ssid,
            password=c.password,
            hostname=c.hostname
        )

PinOut({'white': 2, 'blue': 4, 'yellow': 0})
