import network
import machine

from config import Config
from microWebSrv import MicroWebSrv


# --- led initialize ---

LED = {
    4 : machine.Pin(4, machine.Pin.OUT)
}



# --- server routes ---

@MicroWebSrv.route('/reset')
def route_reset(client, response) :
    machine.reset()


@MicroWebSrv.route('/info')
def route_info(client, response) :
    import ubinascii
    import gc

    net = network.WLAN(network.STA_IF)
    response.WriteResponseJSONOk(
        {
            'machine': {
                'frequence_mhz': machine.freq() / 1000000,
                'id': ubinascii.hexlify(machine.unique_id(), ':').decode(),
                'free_mem_kb': gc.mem_free() / 1000
            },
            'net': {
                'hostname': net.config('dhcp_hostname'),
                'mac': ubinascii.hexlify(net.config('mac'), ':').decode(),
                'ssid': net.config('essid'),
                'ip': net.ifconfig()[0],
                'netmask': net.ifconfig()[1],
                'router': net.ifconfig()[2],
                'dns': net.ifconfig()[3]
            }
        }
    )


@MicroWebSrv.route('/led/<id>/on')
def route_led_on(client, response, args):
    id = int(args['id'])
    if id in LED:
        LED[id].value(1)
        response.WriteResponseOk()
    else:
        response.WriteResponseBadRequest()


@MicroWebSrv.route('/led/<id>/off')
def route_led_off(client, response, args):
    id = int(args['id'])
    if id in LED:
        LED[id].value(0)
        response.WriteResponseOk()
    else:
        response.WriteResponseBadRequest()




# --- main program ---

print('--- start webserver ---')
net = network.WLAN(network.STA_IF)
if net.isconnected():
    c = Config()
    w = MicroWebSrv(bindIP=net.ifconfig()[0], port=c.get('port', 80), webPath=c.get('www', '/www'))
    w.Start(threaded=c.get('threaded', True))
