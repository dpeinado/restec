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
        GET_PROJECT_BYID=(
            lambda self, *args: self.server.myDataBase.get_project_byId(*args)),                
        GET_RESOURCE_LIST=(
            lambda self, *args: self.server.myDataBase.get_resource_list(*args)),
        GET_RESOURCE_BYID=(
            lambda self, *args: self.server.myDataBase.get_resource_byId(*args)),                
        GET_ACTIVITY_LIST=(
            lambda self, *args: self.server.myDataBase.get_activity_list(*args)),
        GET_ACTIVITY_BYID=(
            lambda self, *args: self.server.myDataBase.get_activity_byId(*args)), 
        GET_TASK_LIST=(
            lambda self, *args: self.server.myDataBase.get_task_list(*args)),
        GET_TASK_BYID=(
            lambda self, *args: self.server.myDataBase.get_task_byId(*args)),                               
        GET_ENTRY_LIST=(
            lambda self, *args: self.server.myDataBase.get_entries_list(*args)),
        GET_ENTRY_RAW_LIST=(
            lambda self, *args: self.server.myDataBase.get_entries_raw_list(*args)),
        SET_NEW_PROJECT=(
            lambda self, *args: self.server.myDataBase.set_new_project(*args)),
        SET_NEW_RESOURCE=(
            lambda self, *args: self.server.myDataBase.set_new_resource(*args)),
        SET_NEW_ACTIVITY=(
            lambda self, *args: self.server.myDataBase.set_new_activity(*args)),
        SET_NEW_TASK=(
            lambda self, *args: self.server.myDataBase.set_new_task(*args)),       
        SET_NEW_ENTRY=(
            lambda self, *args: self.server.myDataBase.set_new_entry(*args)),                                
        SHUTDOWN_SERVER=lambda self, *args: self.shutdown(*args)
        )
    
    def handle(self):
        SizeStruct = struct.Struct("!I")
        size_data = self.rfile.read(SizeStruct.size)
        size = SizeStruct.unpack(size_data)[0]
        data = pickle.loads(self.rfile.read(size))

        try:
            function = self.Call[data[0]]
            reply = function(self, *data[1:])
        except Finish:
            return
        data = pickle.dumps(reply, 0)
        self.wfile.write(SizeStruct.pack(len(data)))
        self.wfile.write(data)
        
        
    def shutdown(self, *ignore):
        self.server.shutdown()
        self.server.myDataBase.disconnect()
        raise Finish()
        

class ThreadServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def main():
    host = 'localhost'
    port = 9999
    user = 'puser'
    userpwd = 'pu8549'
    database = 'proyectos'
    try:
        server = ThreadServer((host,port), MyDbServerManagerRequestHandler)
        server.myDataBase=myDb.myDb('localhost', 'puser','pu8549','projects')
        server.myDataBase.connect()
        print "Server a la escucha"
        server.serve_forever()
    except Exception as err:
        print("ERROR", err)
    finally:
        print "Estoy en Finally"
        if server is not None:
            server.shutdown()


main()