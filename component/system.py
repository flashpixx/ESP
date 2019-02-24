'''
system model for generic structures
'''

import esp
import machine
import network


def wifi_accesspoint(ssid: str, password: str, channel: int = None, hidden: bool = False):
    '''
    creates an accesspoint, default authentification methode is WPA2-PSK

    :param ssid: network ssid
    :param password: network password
    :param channel optional wifi channel
    :param hidden: optional hidden wifi flag
    '''

    network.WLAN(network.STA_IF).active(False)

    net = network.WLAN(network.AP_IF)
    net.config(essid=ssid, password=password, hidden=1 if hidden else 0)
    if not channel is None:
        net.config(channel=channel)

    net.active(True)
    print('Wifi Config: IP %s - Netmask %s - Router %s - DNS %s' % net.ifconfig())


def wifi_connect(ssid: str, password: str, hostname: str = None):
    '''
    connects to a wifi access point

    :param ssid: wifi ssid
    :param password: wifi password
    :param hostname: optional hostname
    '''

    network.WLAN(network.AP_IF).active(False)

    net = network.WLAN(network.STA_IF)
    net.ifconfig(('dhcp'))
    net.active(True)
    if net.isconnected():
        return

    if not hostname is None:
        net.config(dhcp_hostname=hostname)

    net.connect(ssid, password)
    while not net.isconnected():
        machine.idle()

    print('Wifi Config: IP %s - Netmask %s - Router %s - DNS %s' % net.ifconfig())


def debugoff():
    '''
    disable debugging log
    '''
    esp.osdebug(None)
