# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Utils file
class Utils :

    # ------------------- Fungsi message_received(client,server,message) ------------------- #
    # Akan pass karena di fungsi akan di set oleh set_fn_message_received
    def message_received(self, client, server, message):
        pass

    # ------------------- Fungsi binary_message_received(client,server,message) ------------------- #
    # Akan pass karena di fungsi akan di set oleh set_fn_binary)message_received
    def binary_message_received(self, client, server, message):
        pass

    # ------------------- Fungsi set_fn_message_received(self, fn) ------------------- #
    # Akan passing fungsi message_received dengan fungsi fn
    def set_fn_message_received(self, fn):
        self.message_received = fn
    
    # ------------------- Fungsi set_fn_binary_message_received(self, fn) ------------------- #
    # Akan passing fungsi binary_message_received dengan fungsi fn
    def set_fn_binary_message_received(self, fn):
        self.binary_message_received = fn