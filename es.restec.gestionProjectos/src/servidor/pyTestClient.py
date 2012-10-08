'''
Created on 04/10/2012

@author: bicho
'''

import struct
import pickle
import socket
import time
import sys


Address = ["localhost", 9999]


class SocketManager:
    def __init__(self, address):
        self.address = address
    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        return self.sock
    def __exit__(self, *ignore):
        self.sock.close()

def handle_request( *items, **kwargs):
    wait_for_reply=kwargs.pop('wait_for_reply', True)
    SizeStruct = struct.Struct("!I")
    data = pickle.dumps(items, 0)
    
    try:
        with SocketManager(tuple(Address)) as sock:
            sock.sendall(SizeStruct.pack(len(data)))
            sock.sendall(data)
            if not wait_for_reply:
                return

            size_data = sock.recv(SizeStruct.size)
            size = SizeStruct.unpack(size_data)[0]
            result = bytearray()
            while True:
                data = sock.recv(4000)
                if not data:
                    break
                result.extend(data)
                if len(result) >= size:
                    break
        return pickle.loads(result)
    except socket.error as err:
        print("{0}: is the server running?".format(err))
        sys.exit(1)


def print_tuples(data):
    cuantos=len(data)
    if cuantos ==1:
        print data[0]
    else:
        for detail in data[0]:
            print detail, "\t",
        print
        for row in data[1]:
            for detail in row:
                print detail, "\t",
            print    

def main():
    ok, data = handle_request("SET_NEW_PROJECT", '145', 'Torre InNOVa S 2')
    if(ok):
       print_tuples(data)
    else:
        print "Error: ", data[0]
    #===========================================================================
    # ok, data = handle_request("SET_NEW_RESOURCE", 'Paco Martinez Soria', '12.5')
    # if(ok):
    #   print_tuples(data)                                          
    # 
    # ok = handle_request("SHUTDOWN_SERVER",wait_for_reply=False)
    #===========================================================================

        
main()