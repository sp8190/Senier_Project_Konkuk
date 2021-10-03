import socket

HOST = '192.168.1.52'
# Enter IP or Hostname of your server
PORT = 5521
# Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
        command = raw_input('Enter your command: ')
        s.send(command)
        reply = s.recv(1024)
        reply = str(reply,"utf-8")
        if reply == 'Terminating':
                break
        print (reply)
