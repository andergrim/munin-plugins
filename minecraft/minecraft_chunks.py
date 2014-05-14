#!/usr/local/bin/python
# Change to /usr/bin/env python if other os than FreeBSD
import sys
import os
import socket
import select
import struct
import re

host = "localhost"
port = 25575
pwd = ""

if os.environ.get("host") is not None:
    host = os.environ.get("host")
if os.environ.get("port") is not None:
    port = int(os.environ.get("port"))
if os.environ.get("password") is not None:
    pwd = os.environ.get("password")

class MCRcon:
    def __init__(self, host, port, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.send_real(3, password)
    
    def close(self):
        self.s.close()
    
    def send(self, command):
        return self.send_real(2, command)
    
    def send_real(self, out_type, out_data):
        #Send the data
        buff = struct.pack('<iii', 
            10+len(out_data),
            0,
            out_type) + out_data + "\x00\x00"
        self.s.send(buff)
        
        #Receive a response
        in_data = ''
        ready = True
        while ready:
            #Receive an item
            tmp_len, tmp_req_id, tmp_type = struct.unpack('<iii', self.s.recv(12))
            tmp_data = self.s.recv(tmp_len-8) #-8 because we've already read the 2nd and 3rd integer fields

            #Error checking
            if tmp_data[-2:] != '\x00\x00':
                raise Exception('protocol failure', 'non-null pad bytes')
            tmp_data = tmp_data[:-2]
            
            #if tmp_type != out_type:
            #    raise Exception('protocol failure', 'type mis-match', tmp_type, out_type)
           
            if tmp_req_id == -1:
                raise Exception('auth failure')
           
            m = re.match('^Error executing: %s \((.*)\)$' % re.escape(out_data), tmp_data)
            if m:
                raise Exception('command failure', m.group(1))
            
            #Append
            in_data += tmp_data

            #Check if more data ready...
            ready = select.select([self.s], [], [], 0)[0]
        
        return in_data

r = MCRcon(host, port, pwd)
a = r.send("gc").split("\n")

config = False

if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        print "graph_title Minecraft Chunks"
        print "graph_vlabel chunks"
        print "graph_category minecraft"
        config = True

for b in a[5:-1]:
    enttype = b[3:].split(" ")[0]
    if enttype == "World":
      world_name = b.split(":")[0].split(" ")[1].replace("\"\xc2\xa7c", "").replace("\xc2\xa76\"", "")
      world_data = b.split(":")[1].split(", ");
      chunks = world_data[0].replace("\xc2\xa7c", "").replace("\xc2\xa76 chunks", "")
      entities = world_data[1].replace("\xc2\xa7c", "").replace("\xc2\xa76 entities", "")
      tiles = world_data[2].replace("\xc2\xa7c", "").replace("\xc2\xa76 tiles.", "")
      if config:
        print world_name + ".label " + world_name
      else:
        print world_name + ".value " + chunks
