# -*- coding: UTF-8 -*-
'''
Created on 22/10/2012

@author: diego.peinado
'''
import struct
import pickle
import socket
import time
import datetime
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import managementconsole_ui

class SocketManager:
    def __init__(self, address):
        self.address = address
    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        return self.sock
    def __exit__(self, *ignore):
        self.sock.close()
class mmForm(QDialog,
               managementconsole_ui.Ui_Dialog):
    '''
    classdocs
    '''
    def __init__(self, myHost, myPort, parent=None):
        super(mmForm, self).__init__(parent)
        self.__Address = [myHost, myPort]        
        
        self.setupUi(self)
        self.updateUi()

    def updateUi(self):
        ok, data = self.handle_request("GET_INFO_ENTRIES")
        pass

    def handle_request(self, *items, **kwargs):
        wait_for_reply=kwargs.pop('wait_for_reply', True)
        SizeStruct = struct.Struct("!I")
        data = pickle.dumps(items, 0)
    
        try:
            with SocketManager(tuple(self.__Address)) as sock:
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
        
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Uso: TrackprojectsServer host port"
        sys.exit(1)
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except Exception as err:
        print "Error conversi�n del puerto a entero", err

    app = QApplication(sys.argv)
    app.setOrganizationName("Restec")
    app.setOrganizationDomain("restec.es")
    app.setApplicationName("ProjectTimesManagementConsole")
    form = mmForm(host,port)
    form.show()
    form.exec_()
    #form.closeEvent('a')
    sys.exit()
    print "He acabado"