'''
system model for generic structures
'''

import network
import esp
import machine


def wifi_accesspoint(
        ssid: str,
        password: str,
        ip: str,
        netmask: str,
        gateway: str,
        dns: str,
        channel: int = None,
        hidden: bool = False,
        hostname: str = None):
    '''
    creates an accesspoint, default authentification methode is WPA2-PSK

    :param ssid: network ssid
    :param password: network password
    :param ip: ip address
    :param netmask: network mask
    :param channel optional wifi channel
    :param hidden: optional hidden wifi flag
    :param hostname: optional hostname
    '''

    net = network.WLAN(network.AP_IF)
    net.active(True)

    net.ifconfig((ip, netmask, gateway, dns))
    net.config(essid=ssid, password=password, hidden=0 if hidden else 1)
    net.config(authmode=3)


    if not hostname is None:
        net.config(dhcp_hostname=hostname)
    if not channel is None:
        net.config(channel=channel)


def wifi_connect(ssid: str, password: str, hostname: str = None):
    '''
    connects to a wifi access point

    :param ssid: wifi ssid
    :param password: wifi password
    :param hostname: optional hostname
    '''


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
