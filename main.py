import network
import machine

from config import Config
from microWebSrv import MicroWebSrv



# --- server routes ---

@MicroWebSrv.route('/hello-world')
def route_hellow_world(client, response) :
    print('Hello World...')
    response.WriteResponseOk()


@MicroWebSrv.route('/reset')
def route_reset(client, response) :
    machine.reset()



# --- main program ---

print('--- start webserver ---')
net = network.WLAN(network.STA_IF)
if net.isconnected():
    c = Config()
    w = MicroWebSrv(bindIP=net.ifconfig()[0], port=c.get('port', 80), webPath=c.get('www', '/www'))
    w.Start(threaded=c.get('threaded', True))
