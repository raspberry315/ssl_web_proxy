
m SocketServer import BaseRequestHandler, ThreadingTCPServer
import os
import ssl
import socket

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
basedir += '\\ssl_web_proxy\\cert-master'


def getInfo(data):
    header = data.split(' ')
    host = header[1].split(':')[0]
    if host[:4] == 'www.':
        name = host[4:]
    else:
        name = host
    return host, name


def genCert(name):
    cmd = 'cd ' + basedir + ' & _make_site.bat ' + name
    os.system(cmd)


def initCert():
    cmd = 'cd ' + basedir + ' & _init_site.bat'
    os.system(cmd)


def clearCert():
    cmd = 'cd ' + basedir + ' & _clear_site.bat'
    os.system(cmd)


class SockHandler(BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(4096)

        if 'CONNECT' in self.data:
            host, name = getInfo(self.data)
            print host, name
            self.request.sendall('HTTP/1.1 Connection established\r\n\r\n') #respond to client with 'connection established' message

            genCert(name)
            client_sock = ssl.wrap_socket(self.request, server_side=True,
                                          keyfile=os.path.join(basedir, name + '.pem'),
                                          certfile=os.path.join(basedir, name + '.pem'))

            req = client_sock.recv(4096)        #get request

            try:    #openssl to real server
                server_sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                server_sock.connect((host, 443))

                server_sock.sendall(req)

                #relaying
                while 1:
                    res = server_sock.recv(4096)
                    if not res:
                        break

                client_sock.sendall(res)
                return

            except:
                print "[+]Trying Connection...\n\n"

            finally:
                server_sock.close()


if __name__ == '__main__':
    initCert()
    proxy = ThreadingTCPServer(('127.0.0.1', 4433), SockHandler)
    proxy.stop_looping = False
    try:
        proxy.serve_forever()
    except KeyboardInterrupt:
        clearCert()
        print 'ctrl + c'
    proxy.stop_looping = True
