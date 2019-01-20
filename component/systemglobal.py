class SystemGlobal(object):
    '''
    system access
    '''

    @staticmethod
    def wifi_connect(ssid: str, password: str, hostname: str = None):
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

        print('Wifi Config: IP %s - Netmask %s - Router %s - DNS %s' % net.ifconfig())


    @staticmethod
    def debugoff():
        import esp

        esp.osdebug(None)