# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Server file
from WShandler import WShandler
import socketserver
from WSutils import Utils

class WSserver(socketserver.ThreadingMixIn,socketserver.TCPServer, Utils) :

    clients = []

    def __init__(self, port, host='0.0.0.0'):
        socketserver.TCPServer.__init__(self, (host, port), WShandler)
        self.port = self.socket.getsockname()[1]

    def _message_received_(self, handler, msg):
        self.message_received(self.handler_to_client(handler), self, msg)

    def _binary_message_received_(self, handler, msg):
        self.binary_message_received(self.handler_to_client(handler), self, msg)

    def _ping_received_(self, handler, msg):
        handler.send_pong(msg)

    def _pong_received_(self, handler, msg):
        pass

    def _new_client_(self, handler):
        client = {
            'handler': handler,
            'address': handler.client_address
        }
        self.clients.append(client)

    def _client_left_(self, handler):
        client = self.handler_to_client(handler)
        if client in self.clients:
            self.clients.remove(client)

    def _unicast_(self, to_client, msg):
        to_client['handler'].send_message(msg)
    
    def _binary_unicast(self, to_client, msg):
        to_client['handler'].send_binary_message(msg)

    def handler_to_client(self, handler):
        for client in self.clients:
            if client['handler'] == handler:
                return client