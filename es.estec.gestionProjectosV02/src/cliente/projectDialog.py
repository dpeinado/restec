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
    def __init__(self, current, myProjectTree,parent=None):
        super(projectDialog,self).__init__(parent)
        self.myParent = parent
        self.setMinimumSize(500,200)
        self.setWindowTitle('Selección del Proyecto/Tarea')
        self.myPT = myProjectTree
        self.__current = current        
        self.__numberCols = 3
        treeLabel = QLabel("Proyectos")
        self.tree = QTreeWidget()                
        treeLabel.setBuddy(self.tree)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        newButton = QPushButton("Proyecto/Tarea &Nuevo")
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
        newButton.clicked.connect(self.makeNewProject)
        
        self.updateTable(self.__current)
        
    def makeNewProject(self):
        currPID=self.tree.currentItem().text(2)
        myProj=self.myPT.myProjects[int(currPID)]
        if len(self.myPT.path_node(myProj[0]))==1:
            isProject=True
        else:
            isProject=False
        myNPD = newProject.newProjectDlg(self.myPT, isProject, self)
        if myNPD.exec_():
            pass
            if isProject:
                ncode = myNPD.myCode.text()
            else:
                ncode = myProj[4]
            ndesc = myNPD.myDesc.text()
            nparent = myProj[0]
            ok, newNode, newPT = self.myParent.handle_request("SET_NEW_PROJECT",nparent,ncode,ndesc)
            if ok:
                current=str(newNode[0])
                self.myPT=newPT
                self.updateTable(current) 
        else:
            print "Rechacé"
        
    def updateTable(self,current=None):
        self.tree.clear()
        self.tree.setColumnCount(self.__numberCols)
        #self.tree.setColumnHidden(2,True)
        self.tree.setHeaderLabels([QString('Codigo'),QString("Descripcion"),QString('IdProj')])
        self.tree.setEditTriggers(QTreeWidget.NoEditTriggers)
        self.tree.setSelectionBehavior(QTreeWidget.SelectRows)
        self.tree.setSelectionMode(QTreeWidget.SingleSelection)

        self.tree.setItemsExpandable(True)
        selected = None
        self.parentFromTask ={}        
        for row in self.myPT:        
            msg1=QString(row[4])
            msg2=QString(row[5])
            msg3=QString(str(row[0]))
            if row[1] is None:
                rootNode=QTreeWidgetItem(self.tree,[msg1,msg2,msg3])
                self.parentFromTask[row[0]]=rootNode
                self.tree.expandItem(rootNode)
                if current is None:
                    selected = None                
            else:
                ancestor=self.parentFromTask[row[1]]
                if ancestor is None:
                    raise ValueError('There is a subproject without parent and is not the root')
                treeTask = QTreeWidgetItem(ancestor,[msg1,msg2,msg3])
                self.parentFromTask[row[0]]=treeTask
                if current is not None and current == str(row[0]):
                    selected = treeTask                
                self.tree.expandItem(treeTask)
                self.tree.expandItem(ancestor)
            #print row
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        self.tree.resizeColumnToContents(2)
        if selected is not None:
            selected.setSelected(True)
            self.tree.setCurrentItem(selected)        

        
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