# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Kelompok Apeni
# Pandyaka Aptanagi / 13517003
# Ainun Fitryh V. / 13517057
# Kintan Sekar Adinda / 13517102

from WSserver import *
import hashlib

# ------------------- Fungsi message_received(client, server, message) ------------------- #
# Digunakan untuk menerima pesan dari client dalam bentuk text
# Akan dikirim balik berupa text tanpa "!echo" untuk soal nomor 1
# Akan dikirim balik file "submission.zip" berupa binary untuk soal nomor 2 
def message_received(client, server, message):
	if '!echo' in message :
		server._unicast_(client,message.split('!echo ')[1])
	elif '!submission' in message :
		temp = b''
		with open('submission.zip','rb') as f:
			temp = f.read()
		server._binary_unicast(client,temp)

# ------------------- Fungsi binary_message_received(client, server, message) ------------------- #
# Digunakan untuk menerima pesan dari client dalam bentuk binary
# Akan dijadikan sebuah file dengan ekstensi .zip, kemudian dibandingkan
# md5 file yang dikirim dengan md5 file yang kita miliki
# Return 0 jika tidak sesuai dan 1 jika sesuai
def binary_message_received(client, server, message):
	temp = b''
	temp = temp + message
	with open('submiss-result.zip','wb') as f :
		f.write(temp)
	
	with open('submission.zip','rb') as f:
		data = f.read()
		original_md5 = hashlib.md5(data).hexdigest()
	
	with open('submiss-result.zip','rb') as f :
		data = f.read()
		compared_md5 = hashlib.md5(data).hexdigest()
	
	original_md5 = original_md5.lower()
	compared_md5 = compared_md5.lower()

	if original_md5 == compared_md5 :
		server._unicast_(client,'1')
	else :
		server._unicast_(client,'0')

if __name__ == "__main__":	
	PORT = 9001
	server = WSserver(PORT)
	server.set_fn_message_received(message_received)
	server.set_fn_binary_message_received(binary_message_received)
	server.serve_forever()