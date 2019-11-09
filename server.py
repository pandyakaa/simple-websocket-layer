# Tugas Besar 2 Jaringan Komputer
# Simple WebSocket Server

# Kelompok Apeni
# Pandyaka Aptanagi / 13517003
# Ainun Fitryh V. / 13517057
# Kintan Sekar Adinda / 13517102

from WSserver import *

def message_received(client, server, message):
	if '!echo' in message :
		server.send_message(client,message.split('!echo')[1])
		print(message.split('!echo ')[1])
	else :
		server.send_message(client,message)

PORT=9001
server = WSserver(PORT)
server.set_fn_message_received(message_received)
server.run_forever()