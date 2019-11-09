# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Server file
from WShandler import WShandler
import socketserver
from WSutils import Utils

class WSserver(socketserver.TCPServer, Utils) :

    clients = []
    id_counter = 0

    def __init__(self, port, host='127.0.0.1'):
        socketserver.TCPServer.__init__(self, (host, port), WShandler)
        self.port = self.socket.getsockname()[1]

    def _message_received_(self, handler, msg):
        self.message_received(self.handler_to_client(handler), self, msg)

    def _ping_received_(self, handler, msg):
        handler.send_pong(msg)

    def _pong_received_(self, handler, msg):
        pass

    def _new_client_(self, handler):
        self.id_counter += 1
        client = {
            'id': self.id_counter,
            'handler': handler,
            'address': handler.client_address
        }
        self.clients.append(client)
        self.new_client(client, self)

    def _client_left_(self, handler):
        client = self.handler_to_client(handler)
        self.client_left(client, self)
        if client in self.clients:
            self.clients.remove(client)

    def _unicast_(self, to_client, msg):
        to_client['handler'].send_message(msg)

    def handler_to_client(self, handler):
        for client in self.clients:
            if client['handler'] == handler:
                return client