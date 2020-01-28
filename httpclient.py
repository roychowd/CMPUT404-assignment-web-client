#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
        print(self.body, self.code)


class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code =data.split()
        return int(code[1])

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        newurl = urllib.parse.urlparse(url)
        # print(newurl.hostname, newurl.port)
        port = newurl.port
        host = newurl.hostname
        path = newurl.path  
        if port == None: 
            port = 80
        # print("PATH " ,newurl.path)
        if path is "":
            path = "/"
        httpmessage = "GET {path} HTTP/1.1\r\nHost: {hostname}\r\nAccept:  */*\r\nConnection: Close\r\n\r\n".format(path=path, hostname=newurl.hostname)
        # print("HOST, PORT",  host, port, "\nhttpmessage:\n", httpmessage)
        self.connect(host, port)
        self.sendall(httpmessage)
        recvalue = self.recvall(self.socket)
        try:
            code = int(self.get_code(recvalue))
        except:
            code = 500
        # code = 500
        body = self.get_body(recvalue)
        # print("***********CODE: " , code, "************BODY: \n", body , "\n ***END TRANSMISSION")
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        newurl = urllib.parse.urlparse(url)
        host = newurl.hostname
        path = newurl.path
        port = newurl.port
      
        if (args):
            args = urllib.parse.urlencode(args)
            contentlength=len(args)
        else: 
            args = ""
            contentlength = 0
        httpmessage = 'POST {path} HTTP/1.1\r\nHost: {host}\r\nACCEPT: */*\r\nContent-Length: {contentlength}\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: Close\r\n\r\n'.format(path=path, host=host, contentlength=contentlength)
        httpmessage+=args
        print(httpmessage)
        # httpmessage.encode("utf-8")
        if port == None:
            port = 80
        self.connect(host,port)
        self.sendall(httpmessage)
        recvalue = self.recvall(self.socket)
        try:
            code = int(self.get_code(recvalue))
        except:
            code = 500
        body = self.get_body(recvalue)
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
