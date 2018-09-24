import SocketServer
import logging

import django_setup_env

from doorac.models import Log
from django.utils import timezone

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S',
                   )

class DevicesTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(2048)
        logging.debug("TCP {} received: %s".format(self.client_address[0]) %data)
        self.request.sendall("Hello")
#        if "LOG" in data:
#        mylog = Log(text=data, created_date=timezone.now())
#        mylog.save()
#        logging.debug("Updated log to database with data: %s" %mylog.text)
#        else:
#            logging.debug("NOT update database")

class DevicesUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        logging.debug("UDP {} received: %s".format(self.client_address[0]) %data)
#        self.request.sendall("Hello")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

if __name__ == "__main__":
    import threading
    import time
    import sys

    if len(sys.argv) is not 3:
        logging.debug("Usage: python demosocket.py <serverIPaddr> <port>")
        logging.debug("Press Ctrl-C to exit")
    else:
        server_addr = (str(sys.argv[1]), int(sys.argv[2]))
#        server_addr = ('127.0.0.1', 8000)
        broadcast_addr = ('', 5000)
        tcpserver = ThreadedTCPServer(server_addr, DevicesTCPRequestHandler)
        udpserver = ThreadedUDPServer(broadcast_addr, DevicesUDPRequestHandler)
        tcpserver.allow_reuse_address = True
        tcpserver_thr = threading.Thread(target=tcpserver.serve_forever)
        udpserver_thr = threading.Thread(target=udpserver.serve_forever)
        tcpserver_thr.setDaemon(True)
        udpserver_thr.setDaemon(True)
        tcpserver_thr.start()
        udpserver_thr.start()
        logging.debug("Start TCP Server at %s", server_addr)
        logging.debug("Start UDP Server at %s", server_addr)

while True:
    time.sleep(1)

