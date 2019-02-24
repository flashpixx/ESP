import time

import machine
import network

from component.config import Config
from component.max7219matrix import Max7219Matrix
from component.pinout import PinOut
from server.microWebSrv import MicroWebSrv

x = Max7219Matrix(8, 8, clk=14, din=13, cs=12)


@MicroWebSrv.route('/matrix/char/<c>')
def matrix_char(client, response, args):
    x.text(str(args['c']), 0, 0)
    x()
    response.WriteResponseOk()


@MicroWebSrv.route('/matrix/text', 'POST')
def matrix_text(client, response):
    for i in str(client.ReadRequestContentAsJSON()['text']):
        x.reset()
        x.text(i, 0, 0)
        x()
        time.sleep_ms(750)
    x.reset()
    response.WriteResponseOk()


@MicroWebSrv.route('/matrix/brightness/<v>')
def matrix_brightness(client, response, args):
    x.brightness(int(args['v']))
    response.WriteResponseOk()


@MicroWebSrv.route('/matrix/reset')
def matrix_reset(client, response):
    x.reset()
    response.WriteResponseOk()


# --- server routes ---

@MicroWebSrv.route('/reset')
def route_reset(client, response):
    machine.reset()


@MicroWebSrv.route('/info')
def route_info(client, response):
    import ubinascii
    import gc

    net = network.WLAN(network.STA_IF)
    response.WriteResponseJSONOk({
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
        },
        'pinout': PinOut().pindis(),
        'current_state': {
            'pinout': {i: PinOut().isup(i) for i in PinOut().pindis().keys()}
        }
    })


@MicroWebSrv.route('/toggle/<id>')
def route_toggle(client, response, args):
    p = PinOut()
    if args['id'] in p:
        p.toggle(args['id'])
        response.WriteResponseJSONOk({i: PinOut().isup(i) for i in PinOut().pindis().keys()})
    else:
        response.WriteResponseBadRequest()


@MicroWebSrv.route('/random')
def route_random(client, response):
    import time
    import random

    p = PinOut()
    p.alldown()

    for i in range(3):
        for j in p.pindis().keys():
            p.up(j)
            time.sleep(0.25)
            p.down(j)

    p.up(random.choice(p.pins()))
    response.WriteResponseJSONOk({i: PinOut().isup(i) for i in PinOut().pindis().keys()})


# --- main program ---

print('--- start webserver ---')
c = Config()
if c.get('accesspoint', True):
    net = network.WLAN(network.AP_IF)
    w = MicroWebSrv(bindIP=net.ifconfig()[0], port=c.get('port', 80), webPath=c.get('www', '/www'))
    w.Start(threaded=c.get('threaded', True))
else:
    net = network.WLAN(network.STA_IF)
    if net.isconnected():
        w = MicroWebSrv(bindIP=net.ifconfig()[0], port=c.get('port', 80), webPath=c.get('www', '/www'))
        w.Start(threaded=c.get('threaded', True))
