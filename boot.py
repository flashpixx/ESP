from component.config import Config


# --- initialization function ----
def wifi_connect(ssid:str, password:str, hostname:str=None):
    import network

    net = network.WLAN(network.STA_IF)
    net.active(True)
    if net.isconnected():
        return net

    if not hostname is None:
        net.config(dhcp_hostname=hostname)

    net.connect(ssid, password)
    while not net.isconnected():
        pass

    print('wifi config:', net.ifconfig())


def debug_off():
    import esp

    esp.osdebug(None)



# --- initialization ---
print('--- booting ---')
c = Config()

if not c.get("debug", False):
    debug_off()

if 'ssid' in c and 'password' in c:
    wifi_connect( c.ssid, c.password, c.hostname )
