#!/usr/bin/env python

# Client for testing

import sys
import json
import socket


print('\n# 1st phase\n')

# create server and wait for controller
pre_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pre_sock.bind(('localhost', 0))
pre_addr, pre_port = pre_sock.getsockname()
print('[1st] Run server on address: {}, port: {}'.format(pre_addr, pre_port))

pre_sock.listen(1)
pre_conn, (pre_conn_addr, pre_conn_port) = pre_sock.accept()
print('[1st] Connected by {} {}'.format(pre_conn_addr, pre_conn_port))

pre_received = pre_conn.recv(1024)
print('[1st] Recv: {}'.format(pre_received))
pre_msg = 'ACK from 1st server.'
pre_conn.sendall(pre_msg)
print('[1st] Send: {}'.format(pre_msg))
pre_conn.close()


# create client and connect to controller
print('\n# 2nd phase\n')

# parse received JSON
info = json.loads(pre_received)
controller_info = info.get('controller')
host = controller_info.get('host')
port = controller_info.get('port')
#print('\rEnter host: '),
#host = sys.stdin.readline()
#print('\rEnter port: '),
#port = int(sys.stdin.readline())
print('\rConnecting to {} {} ...'.format(host, port))

# create client, connect to controller
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print('Connected.\n')

# client receive data
client_received = client.recv(1024)
print('Recv: {}'.format(client_received))

# client send message to controller
msg = 'Hi! This is client. How are you?'
client.sendall(msg)
print('Send: {}'.format(msg))

# client receive data
client_received = client.recv(1024)
print('Recv: {}'.format(client_received))

# close
client.close()
