# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Utils file
class Utils :

    def run_forever(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.server_close()
        except Exception as e:
            exit(1)

    def new_client(self, client, server):
        pass

    def client_left(self, client, server):
        pass

    def message_received(self, client, server, message):
        pass

    def set_fn_new_client(self, fn):
        self.new_client = fn

    def set_fn_client_left(self, fn):
        self.client_left = fn

    def set_fn_message_received(self, fn):
        self.message_received = fn

    def send_message(self, client, msg):
        self._unicast_(client, msg)