#  coding: utf-8 
import socketserver

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

    path = "www/" #hmm
    status = {'200': "OK", '404':"404 Page Not Found", '405':"405 Method Not Allowed", '301':"301 Page Moved"}
    
    
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode()
        print ("Got a request of: %s\n" % self.data)
        response = self.parse(self.data)
        self.request.sendall(bytearray(response,'utf-8'))
        #self.request.sendall(bytearray(open('www/index.html','r').read(), 'utf-8'))
        
    def parse(self, request):
        http = "HTTP/1.1"
        statusCode = '200'
        statusMessage = MyWebServer.status[statusCode]
        
        response_line = http + ' ' + statusCode + ' ' + statusMessage + '\n\n' + open('www/index.html','r').read()
        
        print("-----------------")
        print(response_line)
        
        return response_line
        
    
    
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    
    #print(bytearray(open('README.md','r').read(), 'utf-8'))

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    #server.shutdown()
    #server.server_close()
    