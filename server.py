# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server
# Kelompok Apeni 
# Pandyaka Aptanagi / 13517003
# Ainun Fitryh V. / 13517057
# Kintan Sekar Adinda / 13517102

import socketserver
from base64 import standard_b64encode
from hashlib import sha1

class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Mendapatkan request handshake dari client kemudian diubah dari byte ke string
        self.data = self.request.recv(1024).strip().decode()
        # Splitting headers request handshake
        headers = self.data.split("\r\n")

        # Jika request yang didapatkan merupakan request handshake yang valid
        if "Connection: Upgrade" in self.data and "Upgrade: websocket" in self.data :
            for h in headers:
                if "Sec-WebSocket-Key" in h :
                    # Ambil key yang dikirim bersama dengan request client
                    key = h.split()[1]
            # Panggil fungsi untuk handshake dengan key yang sudah diberikan       
            self.shake_hand(key)
            print('connection established')

            # Ketika handshake sudah valid, dan server akan menerima secara terus menerus
            # data yang diberikan oleh client
            while True:
                # Payload merupakan frame yang dikirimkan oleh client dan sudah di parsing
                # oleh fungsi decode_frame
                payload = self.decode_frame(bytearray(self.request.recv(1024).strip()))
                # Decode payload ke string
                decoded_payload = payload.decode('UTF-8')
                # TODO: Case payload here
                self.send_frame(payload)
                if "bye" == decoded_payload.lower() :
                    print("Closing connection..")
                    # End connection
                    return
        
        # Jika request handshake tidak valid
        else :
            self.request.sendall("HTTP/1.1 400 Bad Request\r\n" + \
                                 "Content-Type: text/plain\r\n" + \
                                 "Connection: close\r\n" + \
                                 "\r\n" + \
                                 "Incorrect request")
    
    def shake_hand(self,key) :
        # Globally Unique Identifier (GUID)
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        
        # Hitung key yang harus dikirim ke client dengan cara :
        # key + GUID (concat) -> hash dengan sha1 -> encode dengan base64
        hash = sha1(key.encode() + GUID.encode())
        response_key = standard_b64encode(hash.digest()).strip()

        # Response yang dikirim ke client
        response = "HTTP/1.1 101 Switching Protocols\r\n" + \
                    "Upgrade: websocket\r\n" + \
                    "Connection: Upgrade\r\n" + \
                    "Sec-WebSocket-Accept: %s\r\n\r\n"%(response_key.decode('ASCII'))

        # Send response ke client
        self.request.sendall(response.encode())

    def decode_frame(self,frame):
        # opcode and fin ada di frame[0] -> bit ke 0 sampai 7
        opcode_and_fin = frame[0]

        # length dari payload ada di frame[1] - 128 -> bit ke 9-15 dimana bit ke 8 isinya mask
        # dan diasumsikan pasti ter-mask
        payload_len = frame[1] - 128

        # Asumsi panjang <= 125, sehingga mask ada di frame[2] sampai [5]
        mask = frame [2:6] 

        # Payload ada di frame[6] sampai frame ke [6+payload_len]
        encrypted_payload = frame [6: 6+payload_len]

        # Decode payload dengan mask
        # untuk setiap byte payload akan di XOR dengan mask pada byte module 4
        payload = bytearray([ encrypted_payload[i] ^ mask[i%4] for i in range(payload_len)])

        return payload

    def send_frame(self, payload):
        # Set opcode menjadi 0x1 (text) dan FIN menjadi 1
        frame = [129]
        # Tambahkan frame dengan payload_len
        frame += [len(payload)]
        # Tambahkan frame dengan payload TANPA mask
        frame_to_send = bytearray(frame) + payload

        self.request.sendall(frame_to_send)

if __name__ == "__main__":
    # HOST dan PORT yang akan di bind server
    HOST, PORT = "localhost", 9999

    # Membuat server dengan binding ke PORT 9999 dan HOST LOCALHOST
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        # Aktivasi server sehingg dapat serve selamanya
        server.serve_forever()