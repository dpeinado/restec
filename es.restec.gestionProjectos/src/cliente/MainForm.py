'''
Created on 09/10/2012

@author: bicho
'''

import struct
import pickle
import socket
import time
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainform

MAC = "qt_mac_set_native_menubar" in dir()


class SocketManager:
    def __init__(self, address):
        self.address = address
    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        return self.sock
    def __exit__(self, *ignore):
        self.sock.close()

class MainForm(QDialog,
               ui_mainform.Ui_MainForm):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        settings = QSettings()
        myResource = str(settings.value('IdResource').toPyObject())
        myProject = str(settings.value('IdProject').toPyObject())
        myActivity = str(settings.value('IdActivity').toPyObject())
        myTask = str(settings.value('IdTask').toPyObject())
        if myTask == 'None':
            myTask = None
        myAddress = [str(settings.value("Host").toPyObject()), settings.value("Port").toPyObject()]

        self.__IdResource = myResource
        self.__IdProject = myProject
        self.__IdTask = myTask
        self.__IdActivity=myActivity
        self.__Address = myAddress
    
        self.setupUi(self)
        
        self.goButton.clicked.connect(self.goUpdating)
        self.stopButton.clicked.connect(self.stopUpdating)
        self.exitButton.clicked.connect(self.exitApp)
        #=======================================================================
        # self.connect(self.goButton, SIGNAL("Clicked()"), self.goUpdating)
        # self.connect(self.stopButton, SIGNAL("Clicked()"), self.stopUpdating)
        #=======================================================================
        self.updateUi()
    
    def goUpdating(self):
        QMessageBox.warning(self, 'He llegado a Go','-Go')
    
    def stopUpdating(self):
        QMessageBox.warning(self, 'He llegado a Stop','-Go')
    
    def exitApp(self):
        self.close()
        
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

    def updateUi(self):
        cual = self.__IdProject
        ok, data = self.handle_request("GET_PROJECT_BYID", cual)
        if ok:
            if cual != str(data[0]):
                msgProject = "Salir del programa INMEDIATAMENTE, IdProjecto = {0}, Valor devuelto = {1}".format(cual, str(data[0]))
                reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
                raise ValueError, "Error al recuperar el proyecto inicial"
            msgProject = unicode("{0}: {1}".format(data[1], data[2]))
            self.displayProyecto.setText(msgProject)
        else:
            msgProject = "No existe el Proyecto = {0}".format(cual)
            reply = QMessageBox.warning(self, 'ERROR en el almacenamiento de los datos iniciales',
                                             msgProject)
            
        cual = self.__IdResource
        ok, data = self.handle_request("GET_RESOURCE_BYID", cual)
        if ok:
            if cual != str(data[0]):
                msgProject = "Salir del programa INMEDIATAMENTE, IdResource = {0}, Valor devuelto = {1}".format(cual, str(data[0]))
                reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
                raise ValueError, "Error al recuperar el recurso inicial"
            msgProject = unicode("{0}".format(data[1]))
            self.displayRecurso.setText(msgProject)
        else:
            msgProject = "No existe el Recurso = {0}".format(cual)
            reply = QMessageBox.warning(self, 'ERROR en el almacenamiento de los datos iniciales',
                                             msgProject)
            
        cual = self.__IdActivity
        ok, data = self.handle_request("GET_ACTIVITY_BYID", cual)
        if ok:
            if cual != str(data[0]):
                msgProject = "Salir del programa INMEDIATAMENTE, IdActivity = {0}, Valor devuelto = {1}".format(cual, str(data[0]))
                reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
                raise ValueError, "Error al recuperar la actividad inicial"
            msgProject = unicode("{0}".format(data[1]))
            self.displayActividad.setText(msgProject)
        else:
            msgProject = "No existe el Recurso = {0}".format(cual)
            reply = QMessageBox.warning(self, 'ERROR en el almacenamiento de los datos iniciales',
                                             msgProject)
                 
        cual = self.__IdTask
        if cual is not None:
            ok, data = self.handle_request("GET_TASK_BYID", cual, self.__IdProject)
            if ok:
                if cual != str(data[0]):
                    msgProject = "Salir del programa INMEDIATAMENTE, IdActivity = {0}, Valor devuelto = {1}".format(cual, str(data[0]))
                    reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
                    raise ValueError, "Error al recuperar la actividad inicial"
                msgProject = unicode("{0}".format(data[3]))
                self.displayTarea.setText(msgProject)
            else:   
                msgProject = "No existe el Recurso = {0}".format(cual)
                reply = QMessageBox.warning(self, 'ERROR en el almacenamiento de los datos iniciales',
                                             msgProject)

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("IdResource", (self.__IdResource))
        settings.setValue("IdProject", (self.__IdProject))
        if self.__IdTask is None:
            myTask = QVariant()
        else:
            myTask = self.__IdTask
        settings.setValue("IdTask", myTask)
        settings.setValue("IdActivity", (self.__IdActivity))
        settings.setValue("Host", (self.__Address[0]))
        settings.setValue("Port", (self.__Address[1]))
        print "Aqui estoy"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("Restec")
    app.setOrganizationDomain("restec.es")
    app.setApplicationName("ProjectAutomaticEntryTimes")
    form = MainForm()
    form.show()
    sys.exit(app.exec_())
    print "He acabado"
