class SystemGlobal:
    '''
    global system access methods
    '''

    @staticmethod
    def wifi_connect(ssid: str, password: str, hostname: str = None):
        '''
        connects to a wifi access point

        :param ssid: wifi ssid
        :param password: wifi password
        :param hostname: optional hostname
        '''
        import network

        net = network.WLAN(network.STA_IF)
        net.active(True)
        if net.isconnected():
            return

        if not hostname is None:
            net.config(dhcp_hostname=hostname)

        net.connect(ssid, password)
        while not net.isconnected():
            pass

        print('Wifi Config: IP %s - Netmask %s - Router %s - DNS %s' % net.ifconfig())

    @staticmethod
    def debugoff():
        '''
        disable debugging log
        '''
        import esp

        esp.osdebug(None)
