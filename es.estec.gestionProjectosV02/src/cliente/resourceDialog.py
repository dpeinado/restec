# -*- coding: UTF-8 -*-
'''
Created on 14/10/2012

@author: bicho
'''
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import newResource

class resourceDialog(QDialog):
    '''
    classdocs
    '''
    def __init__(self, current, myResourceList,parent=None):
        super(resourceDialog,self).__init__(parent)
        self.myParent = parent
        self.setMinimumSize(500,200)
        self.myResourceList = myResourceList
        self.__current = current
        self.__numberRows = len(myResourceList)
        self.__numberCols = 3
        tableLabel = QLabel("Recursos")
        self.table = QTableWidget()
        #self.myTable=QLineEdit()
        tableLabel.setBuddy(self.table)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        newButton = QPushButton("Recurso &Nuevo")
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
        newButton.clicked.connect(self.makeNewResource)
        
        self.updateTable(self.__current)
        
    def makeNewResource(self):
        myNRD = newResource.newResourceDlg( self.myResourceList, self)
        if myNRD.exec_():
            nname = myNRD.myName.text()
            ncost = myNRD.myCost.text()
            ok, data = self.myParent.handle_request("SET_NEW_RESOURCE",nname,ncost)
            if ok:
                self.myResourceList.append(data)
                self.updateTable(str(data[0]))
        else:
            print "RechacŽ"
        
    def updateTable(self,current=None):
        self.table.clear()
        self.table.setRowCount(len(self.myResourceList)) 
        self.table.setColumnCount(self.__numberCols) 
        self.table.setColumnHidden(0,True)
        self.table.setColumnHidden(2,True)
        self.table.verticalHeader().setVisible(False)
        tmp1 = QString("Nombre")
        tmp2 = QString("Coste")
        self.table.setHorizontalHeaderLabels([QString("Id"), tmp1,  tmp2])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        selected = None
        for row, Resource in enumerate(self.myResourceList):
            val = str(Resource[0])
            item = QTableWidgetItem(val)
            if current is not None and current == val:
                selected = item           
            self.table.setItem(row,0,item)
            val = Resource[1]
            item = QTableWidgetItem(val)
            self.table.setItem(row,1,item)
            val = str(Resource[2])
            item = QTableWidgetItem(val)
            self.table.setItem(row,2,item)            
        self.table.resizeColumnsToContents()
        #self.table.sortItems(1,Qt.AscendingOrder)
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
    Resources = []
    current = 1
    form = resourceDialog(current,Resources)
    form.show()
    if form.exec_():
        print "Acept�"
    else:
        print "Cancel�"