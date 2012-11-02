# -*- coding: UTF-8 -*-
'''
Created on 14/10/2012

@author: bicho
'''
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import newActivity

class activityDialog(QDialog):
    '''
    classdocs
    '''
    def __init__(self, current, myActivityList,parent=None):
        super(activityDialog,self).__init__(parent)
        self.myParent = parent
        self.setMinimumSize(500,200)
        self.myActivityList = myActivityList
        self.__current = current
        self.__numberRows = len(myActivityList)
        self.__numberCols = 2
        tableLabel = QLabel("Actividades")
        self.table = QTableWidget()
        #self.myTable=QLineEdit()
        tableLabel.setBuddy(self.table)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        newButton = QPushButton("Actividad &Nueva")
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
        newButton.clicked.connect(self.makeNewActivity)
        
        self.updateTable(self.__current)
        
    def makeNewActivity(self):
        myNAD = newActivity.newActivityDlg( self.myActivityList, self)
        if myNAD.exec_():
            nactivity = myNAD.myActivity.text()
            ok, data = self.myParent.handle_request("SET_NEW_ACTIVITY",nactivity)
            if ok:
                self.myActivityList.append(data)
                self.updateTable(str(data[0]))
        else:
            print "RechacŽ"
        
    def updateTable(self,current=None):
        self.table.clear()
        self.table.setRowCount(len(self.myActivityList)) 
        self.table.setColumnCount(self.__numberCols) 
        self.table.setColumnHidden(0,True)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels([QString("Id"), QString("Actividad")])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        selected = None
        for row, Activity in enumerate(self.myActivityList):
            val = str(Activity[0])
            item = QTableWidgetItem(val)
            if current is not None and current == val:
                selected = item           
            self.table.setItem(row,0,item)
            val = Activity[1]
            item = QTableWidgetItem(val)
            self.table.setItem(row,1,item)
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
    Activitys = []
    current = 1
    form = ActivityDialog(current,Activitys)
    form.show()
    if form.exec_():
        print "Acept�"
    else:
        print "Cancel�"