# -*- coding: utf-8 -*-
'''
Created on 04/10/2012

@author: bicho
'''

import pickle
import struct
import SocketServer
import threading
import time
import myDb

class Finish(Exception): pass

class MyDbServerManagerRequestHandler(SocketServer.StreamRequestHandler):
    # Static data -> the list of myDb functions
    Call = dict(
        GET_PROJECT_LIST=(
            lambda self, *args: self.server.myDataBase.get_project_list(*args)),
            )    
    
    def handle(self):
        SizeStruct = struct.Struct("!I")
        size_data = self.rfile.read(SizeStruct.size)
        size = SizeStruct.unpack(size_data)[0]
        data = pickle.loads(self.rfile.read(size))

        try:
            #===================================================================
            # with self.CallLock:
            #===================================================================
            function = self.Call[data[0]]
            reply = function(self, *data[1:])
        except Finish:
            return
        data = pickle.dumps(reply, 0)
        self.wfile.write(SizeStruct.pack(len(data)))
        self.wfile.write(data)


class ThreadServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def main():
    host = 'localhost'
    port = 9999
    user = 'puser'
    userpwd = 'pu8549'
    database = 'proyectos'
    
    server = ThreadServer((host,port), MyDbServerManagerRequestHandler)
    server.myDataBase=myDb.myDb('localhost', 'puser','pu8549','proyectos')
    server.myDataBase.connect()
    print "Server a la escucha"
    server.serve_forever()
    
main()