# -*- coding: UTF-8 -*-
'''
Created on 09/10/2012

@author: bicho
'''

import struct
import pickle
import socket
import time
import datetime
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainform
import projectDialog
import resourceDialog
import activityDialog
#import taskDialog

import os
mypath = os.path.dirname(__file__)
otherpath=os.path.join(mypath,'..','Common')
sys.path.append(otherpath)
import projectsDataModel

TIMEINTERVAL = 900000

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
    def __init__(self, myHost, myPort, parent=None):
        super(MainForm, self).__init__(parent)
        settings = QSettings()
        myResource = str(settings.value('IdResource').toPyObject())
        if myResource == 'None':
            myResource=None
        myProject = str(settings.value('IdProject').toPyObject())
        #myProject = None
        if myProject=='None':
            myProject=None
        myActivity = str(settings.value('IdActivity').toPyObject())
        if myActivity =='None':
            myActivity=None

        myAddress = [myHost,myPort]
        
        if (myResource is None) or (myProject is None) or (myActivity is None):
            self.__ready = False
        else:
            self.__ready = True
        self.__IdResource = myResource
        self.__IdProject = myProject
        self.__IdActivity=myActivity
        self.__Address = myAddress
        self.__timeFromGo = 0
        self.__timeFromLast = 0
        self.__running = False
    
        self.setupUi(self)	
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        
        self.goButton.clicked.connect(self.goUpdating)
        self.stopButton.clicked.connect(self.stopUpdating)
        self.exitButton.clicked.connect(self.exitApp)
        self.setProyectoButton.clicked.connect(self.setProject)
        self.setRecursoButton.clicked.connect(self.setResource)
        self.setActividadButton.clicked.connect(self.setActivity)

        self.stopButton.setEnabled(False)
        self.goButton.setEnabled(False)
        if(self.__ready):
            self.goButton.setEnabled(True)
        self.showTimeFromGo.setText(self.getHHMM(0))
        self.showTimeFromStart.setText(self.getHHMM(0))
        
        #=======================================================================
        # self.connect(self.goButton, SIGNAL("Clicked()"), self.goUpdating)
        # self.connect(self.stopButton, SIGNAL("Clicked()"), self.stopUpdating)
        #=======================================================================
        self.updateUi()
        
    def setProject(self):
        print "Estoy en setProject"
        ok, data = self.handle_request("GET_PROJECT_TREE")
        if ok:
            myPT = data
            #self.__IdProject='2'
            myPD = projectDialog.projectDialog(self.__IdProject, myPT, self)
            if myPD.exec_():
                ntaskid = myPD.tree.currentItem().text(2)
                self.__IdProject = ntaskid if ntaskid != '1' else None
                if self.__IdProject is not None:
                    self.displayProject(self.__IdProject, myPT)
                if (self.__IdResource is None) or (self.__IdProject is None) \
                                                or (self.__IdActivity is None):
                    self.__ready = False
                else:
                    self.__ready = True
                if self.__ready:
                    ok, data = self.handle_request("GET_TASK_ENTRIES_TIMETOTAL",
                                                  self.__IdResource,self.__IdProject,
                                                  self.__IdActivity)
                    self.showTimeFromStart.setText(self.getHHMM(data[0]))
            else:
                print "Rechacé"                

    def displayProject(self,idP,myPT):
        lista=myPT.path_node(int(idP))
        Cod1 = myPT.myProjects[lista[1]][4]
        Des1 = myPT.myProjects[lista[1]][5]
        if len(lista)>2:
            Cod2 = myPT.myProjects[lista[-1]][4]
            Des2 = myPT.myProjects[lista[-1]][5]
        else:
            Cod2 = ""
            Des2 = ""
        msgProject=QString("%1: %2").arg(Cod1).arg(Des1)
        msgTask =QString("\t%1").arg(Des2)                        
        self.displayProyecto.setText(msgProject)
        self.displayTarea.setText(msgTask)
    
    def setResource(self):
        print "Estoy en setResource"
        ok, data = self.handle_request("GET_RESOURCE_LIST")
        if ok:
            if len(data)==2:
                myResourceList = list(data[1])
                myRD = resourceDialog.resourceDialog(self.__IdResource, myResourceList, self)
                if myRD.exec_():
                    self.__IdResource = myRD.table.item(myRD.table.currentRow(),0).text()
                    itemText1 = myRD.table.item(myRD.table.currentRow(),1).text()
                    msgProject = QString("%1").arg(itemText1)
                    #msgProject = "{0}".format(itemText1)
                    self.displayRecurso.setText(msgProject)
                    if (self.__IdResource is None) or (self.__IdProject is None) \
                        or (self.__IdActivity is None):
                        self.__ready = False
                    else:
                        self.__ready = True
                if self.__ready:
                    ok, data = self.handle_request("GET_TASK_ENTRIES_TIMETOTAL",
                                                   self.__IdResource,self.__IdProject,
                                                   self.__IdActivity)
                    self.showTimeFromStart.setText(self.getHHMM(data[0]))      
                else:
                    print "Rechacé"
        pass    

    def setActivity(self):
        print "Estoy en setActivity"
        ok, data = self.handle_request("GET_ACTIVITY_LIST")
        if ok:
            if len(data)==2:
                myActivityList = list(data[1])
                myAD = activityDialog.activityDialog(self.__IdActivity, myActivityList, self)
                if myAD.exec_():
                    self.__IdActivity = myAD.table.item(myAD.table.currentRow(),0).text()
                    itemText1 = myAD.table.item(myAD.table.currentRow(),1).text()
                    msgProject = QString("%1").arg(itemText1)
                    self.displayActividad.setText(msgProject)
                    if (self.__IdResource is None) or (self.__IdProject is None) \
                        or (self.__IdActivity is None):
                        self.__ready = False
                    else:
                        self.__ready = True
                if self.__ready:
                    ok, data = self.handle_request("GET_TASK_ENTRIES_TIMETOTAL",
                                                  self.__IdResource,self.__IdProject,
                                                  self.__IdActivity)
                    self.showTimeFromStart.setText(self.getHHMM(data[0]))                        
                else:
                    print "Rechacé"

    def getHHMM(self,timeEntry):
        if timeEntry is None:
            return '00:00'
        prueba1 = str(datetime.timedelta(seconds=timeEntry)).split('.')[0]
        prueba2 = prueba1.split(':')
        prueba3 = ':'.join(prueba2[0:2])
        return prueba3
    
    def goUpdating(self):
        self.__timeFromGo = time.time()
        self.__timeFromLast= self.__timeFromGo
        self.__running = True
        self.goButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.exitButton.setEnabled(False)
        self.setProyectoButton.setEnabled(False)
        self.setRecursoButton.setEnabled(False)
        self.setActividadButton.setEnabled(False)
        
        QTimer.singleShot(TIMEINTERVAL, self.callback_Entry)
        
    def callback_Entry(self):
        if self.__running:
            try:
                tmpTime = time.time()
                timeEntry1 = tmpTime - self.__timeFromLast
                timeEntry2 = tmpTime - self.__timeFromGo
                self.__timeFromLast = tmpTime
                totalTime = self.send_entry(timeEntry1)
                print "TOTAL TIME = ", totalTime
                self.showTimeFromGo.setText(self.getHHMM(timeEntry2))
                self.showTimeFromStart.setText(self.getHHMM(totalTime))
                print "Desde Go = %{0}\t Duración de esta carga = {1}".format(timeEntry2, timeEntry1)
            finally:
                QTimer.singleShot(TIMEINTERVAL, self.callback_Entry)
                
    def send_entry(self, timeEntry):
        myRes = self.__IdResource
        myProj = self.__IdProject
        myAct = self.__IdActivity
        ok, data = self.handle_request("SET_NEW_ENTRY",myRes,myProj,myAct,timeEntry)
        if not ok:
            QMessageBox.critical(self,"Error","Error sending new Entry")
            self.close()
        ok, data = self.handle_request("GET_TASK_ENTRIES_TIMETOTAL",myRes,myProj,myAct)
        print data[0]
        return data[0]
        
    def stopUpdating(self):
        self.__running = False
        tmpTime = time.time()
        timeEntry1 = tmpTime - self.__timeFromLast
        timeEntry2 = tmpTime-self.__timeFromGo
        totalTime = self.send_entry(timeEntry1)
        self.showTimeFromGo.setText(self.getHHMM(timeEntry2))
        self.showTimeFromStart.setText(self.getHHMM(totalTime))
        self.__timeFromGo = 0
        self.__timeFromLast = 0
        print "Desde Go = %{0}\t Duración de la última carga = {1}".format(timeEntry2, timeEntry1)
        self.goButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.exitButton.setEnabled(True)
        self.setProyectoButton.setEnabled(True)
        self.setRecursoButton.setEnabled(True)        
        self.setActividadButton.setEnabled(True)
        self.showTimeFromGo.setText(self.getHHMM(0)) 
    
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
        if not self.__ready:
            return
        myRes = self.__IdResource
        myProj = self.__IdProject
        myAct = self.__IdActivity

        ok, data = self.handle_request("GET_TASK_ENTRIES_TIMETOTAL",myRes,myProj,myAct)
        if ok:
            if data[0] is not None:
                tmpTime = data[0]
            else:
                tmpTime = 0
            self.showTimeFromStart.setText(self.getHHMM(tmpTime))
        
        ok, data = self.handle_request("GET_PROJECT_TREE")
        if ok:
            myPT = data
            myK =myPT.myProjects.keys()             
            if int(myProj) in myK:                
                self.displayProject(myProj, myPT)
            else:
                msgProject = "Salir del programa INMEDIATAMENTE, IdProjecto = {0}".format(myProj)
                reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
                raise ValueError, "Error al recuperar el proyecto inicial"
        else:
            msgProject = "Salir del programa INMEDIATAMENTE, Error al obtener GET_PROJECT_TREE}"
            reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
            raise ValueError, "Error al recuperar el proyecto inicial"            
        
        ok, data = self.handle_request("GET_RESOURCE_BYID", myRes)
        if ok:
            if myRes != str(data[0]):
                msgProject = "Salir del programa INMEDIATAMENTE, IdResource = {0}, Valor devuelto = {1}".format(myRes, str(data[0]))
                reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
                raise ValueError, "Error al recuperar el recurso inicial"
            msgProject = QString(data[1])
            self.displayRecurso.setText(msgProject)
        else:
            msgProject = "ERROR en el almacenamiento de los datos iniciales No existe el recurso = {0}".format(myRes)
            reply = QMessageBox.warning(self, 'ERROR',msgProject)
            self.__IdResource=None
            
        ok, data = self.handle_request("GET_ACTIVITY_BYID", myAct)
        if ok:
            if myAct != str(data[0]):
                msgProject = "Salir del programa INMEDIATAMENTE, IdActivity = {0}, Valor devuelto = {1}".format(myAct, str(data[0]))
                reply = QMessageBox.warning(self, 'ERROR de consistencia Interna',
                                             msgProject)
                raise ValueError, "Error al recuperar la actividad inicial"
            msgProject = QString(data[1])
            self.displayActividad.setText(msgProject)
        else:
            msgProject = "ERROR en el almacenamiento de los datos iniciales No existe la Actividad = {0}".format(myAct)
            reply = QMessageBox.warning(self, 'ERROR',msgProject)
            self.__IdActivity=None
                 
    def closeEvent(self, event):
        if self.__running:
            if self.__timeFromLast > 0:
                timeEntry = time.time()-self.__timeFromLast
                self.send_entry(timeEntry)
        settings = QSettings()
       
        #=======================================================================
        # self.__IdResource='1'
        # self.__IdProject='1'
        # self.__IdActivity='1'
        #=======================================================================

        settings.setValue("IdResource", (self.__IdResource))
        settings.setValue("IdProject", (self.__IdProject))
        settings.setValue("IdActivity", (self.__IdActivity))
        print "Aqui estoy"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Uso: TrackprojectsServer host port"
        sys.exit(1)
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except Exception as err:
        print "Error conversión del puerto a entero", err

    app = QApplication(sys.argv)
    app.setOrganizationName("Restec")
    app.setOrganizationDomain("restec.es")
    app.setApplicationName("ProjectAutomaticEntryTimes")
    form = MainForm(host,port)
    form.show()
    form.exec_()
    form.closeEvent('a')
    sys.exit()
    print "He acabado"