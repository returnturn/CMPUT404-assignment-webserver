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
        response = ''
        if method != 'GET':
            response = self.combine('405 Method Not Allowed')
        else:
            dire = os.getcwd()
            path = dire + '/www' + url
            secur = False
            if os.path.realpath(path).startswith(dire):
                secur = True
            if os.path.isfile(path) and secur:
                root_ext = os.path.splitext(path)
                if root_ext[1] == '.html' or root_ext[1] == '.css' :
                    size = open(path).read()
                    if root_ext[1] == '.html':
                        response = self.combine(body=size)
                    else:
                        response = self.combine(t='text/css',body=size)
            elif os.path.isdir(path) and secur:
                newPath = path + '/index.html'
                if os.path.isfile(newPath):
                    if url[-1] == '/':
                        size = open(newPath).read()
                        response = self.combine(body=size)
                    else:
                        redirect = 'http://localhost:8080' + url
                        response = self.combine('301 Moved Permanently',redirect)
            else:
                response = self.combine('404 Not Found')
        self.request.sendall(response.encode())

    def parse(self,data):
        lines = data.splitlines()
        return lines[0].split()
    
    def combine(self,status='200 OK',t='text/html',body=''):
        response = 'HTTP/1.1 ' + status + '\n' + 'Content-Type: ' + t + '\n' + body
        return response
   
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()			
