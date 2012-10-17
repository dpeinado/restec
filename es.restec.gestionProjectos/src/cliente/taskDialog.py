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
    def __init__(self, current, myTaskList,myProjLegend, parent=None):
        super(taskDialog,self).__init__(parent)
        self.myParent = parent
        self.setMinimumSize(500,200)
        self.myTaskList = myTaskList
        self.__current = current
        self.__numberRows = len(myTaskList)
        self.__numberCols = 2
        msgLbl = QString("Tareas del projecto -- %1").arg(myProjLegend)
        treeLabel = QLabel(msgLbl)
        self.tree = QTreeWidget()
        treeLabel.setBuddy(self.tree)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        newButton = QPushButton("Tarea &Nueva")
        hbox = QHBoxLayout()
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch()
        hbox.addWidget(newButton)
        layout=QVBoxLayout()
        layout.addWidget(treeLabel)
        layout.addWidget(self.tree)
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
        self.tree.clear()
        self.tree.setColumnCount(self.__numberCols)
        self.tree.setColumnHidden(1,True)
        self.tree.setHeaderLabels([QString('IdTarea'),QString("Tarea")])
        self.tree.setEditTriggers(QTreeWidget.NoEditTriggers)
        self.tree.setSelectionBehavior(QTreeWidget.SelectRows)
        self.tree.setSelectionMode(QTreeWidget.SingleSelection)

        self.tree.setItemsExpandable(True)
        selected = None
        parentFromTask ={}
        for row, task in enumerate(self.myTaskList):
            try:
                if task[2] is None:
                    ancestor = QTreeWidgetItem(self.tree, [QString(task[3]), QString(str(task[0]))] )
                    parentFromTask[task[0]]=ancestor
                else:
                    ancestor = parentFromTask[task[2]]
                    if ancestor is None:
                        raise ValueError('There is a Task without Parent ??')
                    treeTask = QTreeWidgetItem(ancestor, [QString(task[3]), QString(str(task[0]))] )
                    parentFromTask[task[0]]=treeTask
                    self.tree.expandItem(treeTask)
                self.tree.expandItem(ancestor)
            except ValueError as e:
                print "TreeWidget Error ({0}): {1}".format(e.errno, e.strerror)
                continue
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        
                
        
        
        
        
        #=======================================================================
        # for row, task in enumerate(self.myTaskList):
        #    val = str(task[0])
        #    item = QTableWidgetItem(val)
        #    if current is not None and current == val:
        #        selected = item           
        #    self.table.setItem(row,0,item)
        #    val = task[1]
        #    item = QTableWidgetItem(val)
        #    self.table.setItem(row,1,item)
        #    val = task[2]
        #    item = QTableWidgetItem(val)
        #    self.table.setItem(row,2,item)            
        # self.table.resizeColumnsToContents()
        # self.table.sortItems(1,Qt.AscendingOrder)
        # #self.table.repaint()
        # if selected is not None:
        #    selected.setSelected(True)
        #    self.table.setCurrentItem(selected)
        #    self.table.scrollToItem(selected)    
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