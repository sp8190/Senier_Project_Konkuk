# -*- coding: utf-8 -*-
import socket
import threading


HOST = '192.168.1.52'
# Enter IP or Hostname of your server
PORT = 5521
# Pick an open Port (1000+ recommended), must match the server port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF INET 주소체계로 IPv4 인터넷 프로토콜
#SOCK STREAM TCP를 사용하기 위해 지정
client_socket.connect((HOST,PORT))

for i in range(1,10):
        msg = 'Hello World!'

        data = msg.encode()

        length = len(data)

        client_socket.sendall(length.to_bytes(4, byteorder="little"))

        client_socket.sendall(data)


        data = client_socket.recv(4)

        length = int.from_bytes(data, "little")

        data = client_socket.recv(length)

        msg = data.decode()

        print('Received from : ',msg)

client_socket.close()