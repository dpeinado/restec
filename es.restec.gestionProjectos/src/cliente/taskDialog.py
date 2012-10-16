# -*- coding: UTF-8 -*-
'''
Created on 14/10/2012

@author: bicho
'''
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import newTask

class taskDialog(QDialog):
    '''
    classdocs
    '''
    def __init__(self, current, myTaskList,parent=None):
        super(taskDialog,self).__init__(parent)
        self.myParent = parent
        self.setMinimumSize(500,200)
        self.myTaskList = myTaskList
        self.__current = current
        self.__numberRows = len(myTaskList)
        self.__numberCols = 3
        tableLabel = QLabel("Tareas")
        self.table = QTreeWidget()
        #self.myTable=QLineEdit()
        tableLabel.setBuddy(self.table)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        newButton = QPushButton("Tarea &Nueva")
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
        newButton.clicked.connect(self.makeNewTask)
        
        self.updateTable(self.__current)
        
    def makeNewTask(self):
        myNPD = newTask.newTaskDlg( self.myTaskList, self)
        if myNPD.exec_():
            ncode = myNPD.myCode.text()
            ndesc = myNPD.myDesc.text()
            ok, data = self.myParent.handle_request("SET_NEW_PROJECT",ncode,ndesc)
            if ok:
                self.myTaskList.append(data)
                self.updateTable(str(data[0]))
        else:
            print "Rechac�"
        
    def updateTable(self,current=None):
        self.table.clear()
        self.table.setRowCount(len(self.myTaskList)) 
        self.table.setColumnCount(self.__numberCols) 
        self.table.setColumnHidden(0,True)
        self.table.verticalHeader().setVisible(False)
        tmp1 = QString("C�digo")
        tmp2 = QString("Descripci�n")
        self.table.setHorizontalHeaderLabels([QString("Id"), tmp1,  tmp2])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        selected = None
        for row, task in enumerate(self.myTaskList):
            val = str(task[0])
            item = QTableWidgetItem(val)
            if current is not None and current == val:
                selected = item           
            self.table.setItem(row,0,item)
            val = task[1]
            item = QTableWidgetItem(val)
            self.table.setItem(row,1,item)
            val = task[2]
            item = QTableWidgetItem(val)
            self.table.setItem(row,2,item)            
        self.table.resizeColumnsToContents()
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
    tasks = []
    current = 1
    form = taskDialog(current,tasks)
    form.show()
    if form.exec_():
        print "Acept�"
    else:
        print "Cancel�"