# -*- coding: UTF-8 -*-
'''
Created on 14/10/2012

@author: bicho
'''
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import newProject

class projectDialog(QDialog):
    '''
    classdocs
    '''
    def __init__(self, current, myProjectList,parent=None):
        super(projectDialog,self).__init__(parent)
        self.myParent = parent
        self.setMinimumSize(500,200)
        self.myProjectList = myProjectList
        self.__current = current
        self.__numberRows = len(myProjectList)
        self.__numberCols = 3
        tableLabel = QLabel("Proyectos")
        self.table = QTableWidget()
        #self.myTable=QLineEdit()
        tableLabel.setBuddy(self.table)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        newButton = QPushButton("Proyecto &Nuevo")
        hbox = QHBoxLayout()
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch()
        hbox.addWidget(newButton)
        layout=QVBoxLayout()
        layout.addWidget(tableLabel)
        layout.addWidget(self.table)
        layout.addLayout(hbox)
        self.setLayout(layout)
        
        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"),self, SLOT("reject()"))        
        newButton.clicked.connect(self.makeNewProject)
        
        self.updateTable(self.__current)
        
    def makeNewProject(self):
        myNPD = newProject.newProjectDlg( self.myProjectList, self)
        if myNPD.exec_():
            ncode = myNPD.myCode.text()
            ndesc = myNPD.myDesc.text()
            ok, data = self.myParent.handle_request("SET_NEW_PROJECT",ncode,ndesc)
            if ok:
                self.myProjectList.append(data)
                self.updateTable(str(data[0]))
        else:
            print "Rechacé"
        
    def updateTable(self,current=None):
        self.table.clear()
        self.table.setRowCount(len(self.myProjectList)) 
        self.table.setColumnCount(self.__numberCols) 
        self.table.setColumnHidden(0,True)
        self.table.verticalHeader().setVisible(False)
        tmp1 = QString(u"Código")
        tmp2 = QString(u"Descripción")
        self.table.setHorizontalHeaderLabels([QString("Id"), tmp1,  tmp2])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(False)
        selected = None
        for row, project in enumerate(self.myProjectList):
            val = str(project[0])
            item = QTableWidgetItem(val)
            if current is not None and current == val:
                selected = item           
            self.table.setItem(row,0,item)
            val = project[1]
            item = QTableWidgetItem(val)
            self.table.setItem(row,1,item)
            val = project[2]
            item = QTableWidgetItem(val)
            self.table.setItem(row,2,item)            
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.sortItems(1,Qt.AscendingOrder)
        #self.table.repaint()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)    
        #=======================================================================
        # self.table.clear()
        # self.table.setRowCount(len(self.movies))
        # self.table.setColumnCount(5) 
        # self.table.setHorizontalHeaderLabels(["Title", "Year", "Mins","Acquired", "Notes"])
        #=======================================================================
        
if __name__ == "__main__":
    app=QApplication(sys.argv)
    projects = []
    current = 1
    form = projectDialog(current,projects)
    form.show()
    if form.exec_():
        print "Acepté"
    else:
        print "Cancelé"