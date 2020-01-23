#  coding: utf-8 
import socketserver
import datetime
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

# https://stackoverflow.com/questions/10114224/how-to-properly-send-http-response-with-python-using-socket-library-only
class MyWebServer(socketserver.BaseRequestHandler):

    path_start = "www" #hmm
    status = {200: "HTTP/1.1 200 OK\r\n", 404:"HTTP/1.1 404 Page Not Found\r\n", 405:"HTTP/1.1 405 Method Not Allowed\r\n", 301:"HTTP/1.1 301 Page Moved\r\n"}
    hostname = "127.0.0.1:8080"
    absPath = os.path.abspath("www/")
    
    
    def handle(self):
        self.data = self.request.recv(4096).strip().decode()
        print ("Got a request of: %s\n" % self.data)
        parse_result = self.parse(self.data)
        response = self.get(parse_result)
        self.request.sendall(bytearray(response,'utf-8'))
        
    def parse(self, request):
        
        parts = request.split('\n')
        verb = parts[0].split()
        #host = parts[1].split(': ')

        if (verb == []):
            return 0

        if (verb[0] != 'GET'):
            # 405, verb not supported
            return 405
        
        #if (MyWebServer.hostname not in host[1]):
            #return 404
            
        return verb[1]  # path
        
    def get(self, statusCode):    
         
        if (statusCode == 0):
            return ''
        
        # headers
        server = "Server: " + MyWebServer.hostname + "\r\n"
        date = "Date: " + str(datetime.datetime.now()) + "\r\n"
        #conType = "Content-Type: text/html\r\n"
        conLen = "Content-Length: " + '0' + "\r\n"
        connection = "Connection: keep-alive\r\n"
        #location = "Location: " + ""
        end = "\r\n"
        body = ''
        
        if ((statusCode == 405) or (statusCode == 404)):
            statusMessage = MyWebServer.status[statusCode]
            conType = "Content-Type: text/html\r\n"
            body = open('405.html','r').read() if (statusCode == 405) else open('404.html','r').read()
            conLen = "Content-Length: " + str(len(body)) + "\r\n"
            response_line = ''.join([statusMessage, server, date, conType, conLen, connection, end, body])
                
        else:
            if (('.' not in statusCode) and (statusCode[-1] != '/')):
                # redirect to for a slash
                statusCode += '/'
                statusMessage = MyWebServer.status[301]
                location = "Location: http://" + MyWebServer.hostname + statusCode + "\r\n"
                conType = "Content-Type: text/html\r\n"
                body = open('301.html','r').read()
                conLen = "Content-Length: " + str(len(body)) + "\r\n"
                response_line = ''.join([statusMessage, server, date, conType, conLen, connection, location, end, body])
            
            else:
                try:
                    # open file to send
                    if (statusCode[-1] == '/'):
                        statusCode += 'index.html'
                    self.verify(statusCode)
                    body = open(MyWebServer.path_start + statusCode,'r').read()
                    statusMessage = MyWebServer.status[200]
                    conLen = "Content-Length: " + str(len(body)) + "\r\n"
                    conType = "Content-Type: text/" + statusCode.split('.')[-1] + "\r\n"
                except:
                    statusMessage = MyWebServer.status[404]
                    conType = "Content-Type: text/html\r\n"
                    body = open('404.html','r').read()
                    conLen = "Content-Length: " + str(len(body)) + "\r\n"

                response_line = ''.join([statusMessage, server, date, conType, conLen, connection, end, body])
        
        print("-----------------")
        print(statusCode)  # what was requested
        print(response_line)
        
        return response_line
        
    def verify(self, path):
        # verify that the requested path is in www
        requestedPath = os.path.abspath(MyWebServer.path_start + path)
        #common = os.path.commonpath([requestedPath, MyWebServer.absPath])
        
        if (MyWebServer.absPath not in requestedPath):
            raise
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    
    #print(bytearray(open('README.md','r').read(), 'utf-8'))

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    server.shutdown()
    server.server_close()
    