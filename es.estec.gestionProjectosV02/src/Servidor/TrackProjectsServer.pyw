# -*- coding: UTF-8 -*-
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
import sys

class Finish(Exception): pass

class MyDbServerManagerRequestHandler(SocketServer.StreamRequestHandler):
    # Static data -> the list of myDb functions
    Call = dict(
        GET_INFO_ENTRIES=(
            lambda self, *args: self.server.myDataBase.get_info_entries(*args)),                          
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
        GET_TASK_ENTRIES_TIMETOTAL=(
            lambda self, *args: self.server.myDataBase.get_task_entries_timeTotal(*args)),
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Uso: TrackprojectsServer host port"
        sys.exit(1)
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except Exception as err:
        print "Error conversión del puerto a entero", err

    try:
        server = ThreadServer((host,port), MyDbServerManagerRequestHandler)
        server.myDataBase=myDb.myDb(host, 'puser','pu8549','projects')
        if not server.myDataBase.connect():
            sys.exit(1)
        print "Server a la escucha"
        #ok, data = server.myDataBase.get_info_entries()        
        server.serve_forever()
    except Exception as err:
        print("ERROR", err)
    finally:
        print "Estoy en Finally"
        if server.myDataBase.conn() is not None:
            server.myDataBase.disconnect()