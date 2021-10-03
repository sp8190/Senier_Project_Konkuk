import socket

# Server IP
HOST = '192.168.1.52'

PORT = 5521

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket created')


#managing error exception
try:
	s.bind((HOST, PORT))
except socket.error:
	print ('Bind failed ')

s.listen(5)
print ('Socket awaiting messages')
(conn, addr) = s.accept()
print ('Connected')

# awaiting for message
while True:
	data = conn.recv(1024)
	data = str(data,"utf-8")
	print ('I sent a message back in response to: ' + data)
	
	reply = ''
	
	# process your message
	if data == 'Hello':
		reply = 'Hi, back!'
	elif data == 'This is important':
		reply = 'OK, I have done the important thing you have asked me!'
	#and so on and on until...
	elif data == 'quit':
		reply = 'Terminating'
		reply = bytes(reply, 'utf-8')
		conn.send(reply)
		break
	else:
		reply = 'Unknown command'

	reply = bytes(reply, 'utf-8')
	# Sending reply
	conn.send(reply)

conn.close() 
# Close connections
