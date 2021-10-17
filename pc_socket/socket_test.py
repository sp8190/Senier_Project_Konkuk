# -*- coding: utf-8 -*-
import socket
import threading

HOST = '192.168.1.165'
# 서버 주소, 라즈베리파이 IP 입력
PORT = 5521
# 클라이언트 접속 대기 포트 번호


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF_INET : 주소 체계 IPv4 인터넷 프로토콜, SOCK_STREAM : TCP 통신

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# setsockopt : 소켓 옵션을 정하는 함수 
# SOL_SOCKET : 소켓 옵션 레벨 중 하나
# SO_REUSEADDR : 커널이 소켓을 사용하는 중에도 계속 소켓을 사용할 수 있도록 한다.

#소켓을 특정 네트워크 인터페이스와 포트 번호에 연결.
server_socket.bind((HOST,PORT))

#서버가 클라이언트의 접속을 허용하도록 함.
server_socket.listen()

#accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓과 주소을 리턴
client_socket, addr = server_socket.accept()

#클라이언트의 주소 리턴
print("Connected by ",addr)


while True:

	#클라이언트 보낸 메시지를 수신하기 위해 대기합니다.
	data = client_socket.recv(1024)
	
	#빈 문자열을 수신하면 루프를 중지합니다.
	if not data:
		break

	#수신받은 문자열을 출력합니다.
	print("Received from ", addr, data.decode())

	#받은 문자열을 사디 클라리언트로 (에코)
	client_socket.sendall(data)

#소켓을 닫습니다.
client_socket.close()
server_socket.close()

