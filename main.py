import network

def sever(ip, port, allowed):
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(allowed)
    print('server listen: ', ip, port)

    while True:
        connection, address = s.accept()
        while True:
            data = connection.recv(2048)

            if data == str.encode('quit\r\n'):
                connection.close()
                print('close socket: ', address)
                break

            elif data == str.encode('shutdown\r\n'):
                connection.close()
                s.close()
                print('close server')
                return

            else:
                result = data.decode()
                connection.send(('-> ' + result).encode())
                print(result)

print('--- main ---')
net = network.WLAN(network.STA_IF)
if net.isconnected():
    sever(net.ifconfig()[0], 3030, 10)
