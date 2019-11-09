# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Handler file

import socketserver
from base64 import standard_b64encode
from hashlib import sha1
import struct

class WShandler(socketserver.StreamRequestHandler):

    # ------------------- Representasi dari frames ------------------- #

    #   0                   1                   2                   3
    #   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    #  +-+-+-+-+-------+-+-------------+-------------------------------+
    #  |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
    #  |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
    #  |N|V|V|V|       |S|             |   (if payload len==126/127)   |
    #  | |1|2|3|       |K|             |                               |
    #  +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
    #  |     Extended payload length continued, if payload len == 127  |
    #  + - - - - - - - - - - - - - - - +-------------------------------+
    #  |                               |Masking-key, if MASK set to 1  |
    #  +-------------------------------+-------------------------------+
    #  | Masking-key (continued)       |          Payload Data         |
    #  +-------------------------------- - - - - - - - - - - - - - - - +
    #  :                     Payload Data continued ...                :
    #  + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    #  |                     Payload Data continued ...                |
    #  +---------------------------------------------------------------+

    # ------------------- Constructor ------------------- #
    def __init__(self, sock, address, server) :
        self.server = server
        socketserver.StreamRequestHandler.__init__(self,sock,address,server)
    
    # ------------------- Override fungsi setup()  ------------------- #
    # Digunakan untuk melakukan initialize sebelum handle request
    def setup(self) :
        socketserver.StreamRequestHandler.setup(self)
        self.keep_alive = True
        self.handshake_done = False
        self.valid_client = False
    
    # ------------------- Override handle() ------------------- #
    # Digunakan meng-handle semua pekerjaan pada requests yang masuk
    def handle(self) :
        while self.keep_alive == True :
            if self.handshake_done == False :
                self.make_handshake()
            elif self.valid_client == True :
                self.read_next_message()
    
    # ------------------- Fungsi read_headers() ------------------- #
    # Digunakan untuk membaca headers dari request yang dikirim client

    # GET /chat HTTP/1.1
    # Host: example.com:8000
    # Upgrade: websocket
    # Connection: Upgrade
    # Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
    # Sec-WebSocket-Version: 13

    def read_headers(self) :
        headers = {}
        # First line dari headers adalah HTTP GET (GET /chat HTTP/1.1)
        first_line_headers = self.rfile.readline().decode().strip()

        while True:
            header = self.rfile.readline().decode().strip()
            if not header:
                break
            h, v = header.split(':', 1)
            headers[h.lower().strip()] = v.strip()
        return headers

    # ------------------- Fungsi make_handshake_response(key) ------------------- #
    # Digunakan untuk membuat response handshake yang akan dikirim balik ke client
    def make_handshake_response(self,key) :
        # Globally Unique Identifier (GUID)
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        
        # Hitung key yang harus dikirim ke client dengan cara :
        # key + GUID (concat) -> hash dengan sha1 -> encode dengan base64
        hash = sha1(key.encode() + GUID.encode())
        response_key = standard_b64encode(hash.digest()).strip()

        # Response yang dikirim ke client
        response =  "HTTP/1.1 101 Switching Protocols\r\n" + \
                    "Upgrade: websocket\r\n" + \
                    "Connection: Upgrade\r\n" + \
                    "Sec-WebSocket-Accept: %s\r\n\r\n"%(response_key.decode('ASCII'))

        return response
        
    # ------------------- Fungsi make_handshake() ------------------- #
    # Digunakan untuk melakukan aksi handshake() sehingga client dan server
    # dapat tersambung 
    def make_handshake(self) :
        headers = self.read_headers()

        if headers['upgrade'].lower() != 'websocket' :
            self.keep_alive = False
            return
        
        if not headers['sec-websocket-key'] :
            self.keep_alive = False
            return
        else :
            key = headers['sec-websocket-key']
        
        response_handshake = self.make_handshake_response(key)
        self.handshake_done = self.request.send(response_handshake.encode())
        self.valid_client = True
        self.server._new_client_(self)
    
    # ------------------- Fungsi read_bytes(idx) ------------------- #
    # Digunakan untuk membaca bytes dari index ke 0 hingga index ke idx-1 
    def read_bytes(self,idx) :
        byte = self.rfile.read(idx)
        return byte

    # ------------------- Fungsi read_next_message() ------------------- #
    # Digunakan untuk melakukan read message dari frame yang dikirimkan
    # oleh client
    def read_next_message(self) :
        # Baca first byte dan second byte yang berisi :
        # FIN, OPCODE, dan PAYLOAD LENGTH
        first_byte, second_byte = self.read_bytes(2)
        if first_byte == 0 and second_byte == 0 :
            print('Frame error')
        
        # Ambil nilai FIN, OPCODE dan PAYLOAD LENGTH
        fin_val = first_byte & 0x80 # FIN = 1000 0000
        opcode_val = first_byte & 0x0f # OPCODE = 0000 1111
        masked_val = second_byte & 0x80 # MASKED = 1000 0000
        payload_len_val = second_byte & 0x7f # PAYLOAD_LEN jika <= 125 = 0111 1111

        # Case jika payload tidak di-mask oleh client
        if not masked_val :
            print('Request not masked')
            self.keep_alive = False
            return

        # Case jika request untuk close connection
        if opcode_val == 0x8 : # Jika isi frame untuk close connection
            print('Client request close connection')
            self.keep_alive = False
            return

        # Case untuk tipe frames
        # Jika isi frame merupakan continuation
        if opcode_val == 0x0 :
            print('Continuation frames not supported')
            return
        # Jika isi frame merupakan binary
        elif opcode_val == 0x2 :
            print('Binary frames not supported')
            return
        # Jika isi frame merupakan text
        elif opcode_val == 0x1 :
            opcode_handler = self.server._message_received_
        # Jika isi frame untuk PING
        elif opcode_val == 0x9 :
            opcode_handler = self.server._ping_received_
        # Jika isi frame untuk PONG
        elif opcode_val == 0xA :
            opcode_handler = self.server._pong_received_
        else :
            print('Unknown OPCODE')
            self.keep_alive = False
            return
        
        # Case untuk payload_length
        # Jika payload length 126 -> baca 2 bit selanjutnya
        # Jika payload length 127 -> baca 8 bit selanjutnya
        if payload_len_val == 126 :
            payload_len_val = struct.unpack(">H",self.rfile.read(2))[0]
        elif payload_len_val == 127 :
            payload_len_val = struct.unpack(">H",self.rfile.read(8))[0]
        
        # Baca 4 byte mask
        mask = self.read_bytes(4)
        # Encode payload text dengan mask
        # Untuk setiap byte pada message akan di XOR dengan mask[len(messages) mod 4]
        messages = bytearray()
        for message in self.read_bytes(payload_len_val) :
            message = message ^ mask[len(messages)%4]
            messages.append(message)
        opcode_handler(self, messages.decode('utf8'))
    
    # ------------------- Fungsi send_message(message) ------------------- #
    # Digunakan untuk mengirim message kepada client
    def send_message(self,message) :
        self.send_text(message)
    
    # ------------------- Fungsi send_pong_message() ------------------- #
    # Digunakan untuk mengirim PONG kepada client
    def send_pong_message(self,message) :
        self.send_text(message, 0xA)
    
    # ------------------- Fungsi send_text() ------------------- #
    # Digunakan untuk mengirim text kepada client
    def send_text(self,message, opcode=0x1) :
        header = bytearray()
        payload = message.encode('utf-8')
        payload_length = len(payload)

        # Case untuk payload dengan length <= 125
        if payload_length <= 125 :
            header.append(0x80 | opcode)
            header.append(payload_length)
        
        # Case untuk payload dengan length < 125 dan <= 65535 (16 bit)
        elif payload_length > 125 and payload_length <= 65536 :
            header.append(0x80 | opcode)
            header.append(0x7e)
            header.extend(struct.pack(">H",payload_length))
        
        # Case untuk payload dengan length > 65535 dan < 18446744073709551616 (64 bit)
        elif payload_length < 18446744073709551616 :
            header.append(0x80 | opcode)
            header.append(0x7f)
            header.extend(struct.pack(">Q", payload_length))

        self.request.send(header+payload)