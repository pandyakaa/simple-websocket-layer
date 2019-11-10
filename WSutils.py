# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Utils file
class Utils :

    def message_received(self, client, server, message):
        pass

    def binary_message_received(self, client, server, message):
        pass

    def set_fn_message_received(self, fn):
        self.message_received = fn
    
    def set_fn_binary_message_received(self, fn):
        self.binary_message_received = fn