# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Server file
from WShandler import WShandler
import socketserver
from WSutils import Utils

class WSserver(socketserver.ThreadingMixIn,socketserver.TCPServer, Utils) :

    clients = []

    # ------------------- Constructor ------------------- #
    # Akan membuat instance dari WSserver yang menggunakan library TCPServer
    # dan binding pada host:port dan menggunakan handler dari WShandler
    def __init__(self, port, host='0.0.0.0'):
        socketserver.TCPServer.__init__(self, (host, port), WShandler)
        self.port = self.socket.getsockname()[1]

    # ------------------- Fungsi _message_received_ ------------------- #
    # Akan membuat sebuah fungsi baru yaitu message_received
    def _message_received_(self, handler, msg):
        self.message_received(self.handler_to_client(handler), self, msg)

    # ------------------- Fungsi _binary_message_received_ ------------------- #
    # Akan membuat sebuah fungsi baru yaitu binary_message_received
    def _binary_message_received_(self, handler, msg):
        self.binary_message_received(self.handler_to_client(handler), self, msg)

    # ------------------- Fungsi _ping_received_ ------------------- #
    # Jika menerima PING, maka akan membalas dengan pesan berisi PONG (opcode = 0xA)
    def _ping_received_(self, handler, msg):
        handler.send_pong(msg)

    def _pong_received_(self, handler, msg):
        pass
    
    # ------------------- Fungsi _new_client_ ------------------- #
    # Akan menambahkan client baru ke dalam clients jika berhasil handshake
    def _new_client_(self, handler):
        client = {
            'handler': handler,
            'address': handler.client_address
        }
        self.clients.append(client)

    # ------------------- Fungsi _client_left ------------------- #
    # Akan menghapus client dari clients ketika client memutuskan koneksi
    def _client_left_(self, handler):
        client = self.handler_to_client(handler)
        if client in self.clients:
            self.clients.remove(client)

    # ------------------- Fungsi _unicast_ ------------------- #
    # Akan mengirimkan msg yang memiliki bentuk text kepada client
    def _unicast_(self, to_client, msg):
        to_client['handler'].send_message(msg)
    
    # ------------------- Fungsi _binary_unicast_ ------------------- #
    # Akan mengirimkan msg yang memiliki bentuk binary kepada client
    def _binary_unicast(self, to_client, msg):
        to_client['handler'].send_binary_message(msg)

    # ------------------- Fungsi _binary_unicast_ ------------------- #
    # Akan mereturn client yang memiliki handler == handler
    def handler_to_client(self, handler):
        for client in self.clients:
            if client['handler'] == handler:
                return client