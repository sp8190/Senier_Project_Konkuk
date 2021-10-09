# -*- coding: utf-8 -*-
import socket
import threading


HOST = '192.168.1.41'
# 서버 주소, 라즈베리파이 IP 입력
PORT = 5521
# 클라이언트 접속 대기 포트 번호

#소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#지정한 HOST와 PORT로 연결
client_socket.connect((HOST,PORT))

#메시지를 전송합니다
client_socket.sendall("안녕".encode())

#메시지 수신

date = client_socket.recv(1024)
print("Received ",repr(date.decode()))
# qkdkranhttps://shoark7.github.io/programming/python/difference-between-__repr__-vs-__str__

#소켓 닫기
client_socket.close()