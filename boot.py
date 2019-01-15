import network

def wifi_connect(ssid, password) -> network.WLAN:
    net = network.WLAN(network.STA_IF)
    net.active(True)
    
    if net.isconnected():
        return net

    net.connect(ssid, password)
    while not net.isconnected():
        pass

    print('wifi config:', net.ifconfig())


def load_config() -> dict:
    import ujson

    with open('config.json', 'r') as stream:
        return ujson.load(stream)


def debug_off():
    import esp

    esp.osdebug(None)



print('--- boot ---')
c = load_config()

if not c.get('debug', False):
    debug_off()

if 'ssid' in c and 'password' in c:
    wifi_connect( c.get('ssid'), c.get('password') )
