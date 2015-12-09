#!/usr/bin/env python

import argparse
import socket
import sys
import fcntl
import os
import base64

from Crypto.Cipher import AES

def validat_signature(host, port, signature):
    
    key = 'GJG74JK49457JG7H'
    iv = 16 * '\x00'

    cipher = AES.new(key, AES.MODE_CFB, IV=iv)
    sig = cipher.encrypt(host + str(port))
    
    if signature != base64.b64encode(sig):
        print 'Not Authorized'
        exit(100)
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='pycat', description='Simple socket proxy')
    
    parser.add_argument('-t', required=True, default=None, dest='host', 
        help='The target host name or ip address to connect to.')
    
    parser.add_argument('-p', required=False, default=22, dest='port', type=int, 
        help='The target port to connect to. Defaults to 22')
    
    parser.add_argument('-s', required=True, default=None, dest='signature', 
        help='The signature value to be validated prior to establishing the connection.')
    
    args = parser.parse_args()

validat_signature(args.host, args.port, args.signature) 

'''
Establish connection to the target host.
'''
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((args.host, args.port))
    s.setblocking(0)
except Exception:
    print 'Failed to connect to remote host.'
    exit(100)

'''
Configure the standard input to be non-blocking. This is allows
for repeated bi-directional exchange over the TCP connection.
'''
flags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, flags | os.O_NONBLOCK)

while(1):
    
    is_closed = False
    
    try:
        
        while(1):
            
            data = s.recv(1024)
            
            if not data:
                is_closed = True
                break
            
            sys.stdout.write(data)
            sys.stdout.flush()
        
    except socket.error:
        pass
    
    if is_closed : break
    
    try:
        
        while(1):
            
            data = sys.stdin.read(1024)
            
            if data: 
                s.sendall(data)
            else:
                break
            
    except Exception:
        pass
    
