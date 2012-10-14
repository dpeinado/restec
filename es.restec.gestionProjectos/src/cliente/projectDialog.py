
# -*- coding: utf-8 -*-
'''
Created on 14/10/2012

@author: bicho
'''
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class projectDialog(QDialog):
    '''
    classdocs
    '''
    def __init__(self, current, myProjectList,parent=None):
        super(projectDialog,self).__init__(parent)
        self.setMinimumSize(400,200)
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
        #hbox.addStretch()
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
        pass
        
    def updateTable(self,current=None):
        self.table.clear()
        self.table.setRowCount(len(self.myProjectList)) 
        self.table.setColumnCount(self.__numberCols) 
        #self.table.setColumnHidden(0,True)
        self.table.verticalHeader().setVisible(False)
        tmp1 = unicode("Código")
        tmp2 = unicode("Descripción")
        self.table.setHorizontalHeaderLabels([QString("Id"), QString(tmp1),  QString(tmp2)])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
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
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)    
        pass
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