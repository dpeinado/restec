# -*- coding: UTF-8 -*-
'''
Created on 15/10/2012

@author: bicho
'''

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class newTaskDlg(QDialog):
    '''
    classdocs
    '''
    def __init__(self, myTaskList,parent=None):
        super(newTaskDlg,self).__init__(parent)
        self.setMinimumSize(500,200)
        self.myTaskList = myTaskList
        msgText = "Esta actividad va a colgar de:\n {}".format(parent.tree.currentItem().text(0))
        self.msgLabel = QLabel(msgText)
        taskLabel = QLabel("Tarea")
        self.myTask = QLineEdit("")
        taskLabel.setBuddy(self.myTask)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(okButton)
        hbox3.addWidget(cancelButton)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(taskLabel)
        hbox1.addWidget(self.myTask)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.msgLabel)
        self.setLayout(vbox)
        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"),self, SLOT("reject()"))              
        
    
if __name__ == "__main__":
    app=QApplication(sys.argv)
    tasks = []
    current = 1
    form = newTaskDlg(tasks)
    form.show()
    if form.exec_():
        print "AceptŽ"
    else:
        print "CancelŽ"
        