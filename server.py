#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        method, url, version = self.parse(self.data)
        response = self.combine('404 Not Found',t='text/plain')
        if method != 'GET':
            response = self.combine('405 Method Not Allowed',t='text/plain')
        else:
            dire = os.getcwd()
            path = dire + '/www' + url
            if os.path.realpath(path).startswith(dire):
                if os.path.isfile(path):
                    c = open(path).read()
                    l=len(c)
                    if url[-1] == 'l':
                        response = self.combine(body=c,l=l)
                    elif url[-1] == 's':
                        response = self.combine(t='text/css',body=c,l=l)
                elif os.path.isdir(path):
                    newPath = path + '/index.html'
                    if url[-1] != '/':
                        response = 'HTTP/1.1 301 Moved Permanently\n' + 'Content-Type: text/plain\n' + 'Content-Length: 0\n'+'Location: ' + url + '/\n'
                    elif os.path.isfile(newPath) and url[-1] == '/':
                        c = open(newPath).read()
                        l=len(c)
                        response = self.combine(body=c,l=l)
        self.request.sendall(response.encode())

    def parse(self,data):
        lines = data.splitlines()
        return lines[0].split()
    
    def combine(self,status='200 OK',t='text/html',l=0,body=''):
        response = 'HTTP/1.1 ' + status + '\n' + 'Content-Type: ' + t + '\n' + 'Content-Length: ' + str(l) + '\n\n' + body
        return response
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()			