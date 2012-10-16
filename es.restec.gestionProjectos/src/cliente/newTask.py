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
        self.setMinimumSize(300,200)
        self.myTaskList = myTaskList
        self.msgLabel = QLabel("Ok")
        codeLabel = QLabel("Codigo")
        descLabel = QLabel(QString("Descripcion"))
        self.myCode = QLineEdit("")
        self.myDesc = QLineEdit("")
        codeLabel.setBuddy(self.myCode)
        descLabel.setBuddy(self.myDesc)
        self.myCode.setInputMask("999")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myCode.sizePolicy().hasHeightForWidth())
        self.myCode.setSizePolicy(sizePolicy)
        self.myCode.setMinimumSize(QSize(40, 22))
        self.myCode.setMaximumSize(QSize(40, 22))
        self.myCode.setMaxLength(3)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(okButton)
        hbox3.addWidget(cancelButton)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(codeLabel)
        hbox1.addWidget(self.myCode)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(descLabel)
        hbox2.addWidget(self.myDesc)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.msgLabel)
        self.setLayout(vbox)
        self.myCode.editingFinished.connect(self.validateCode)
        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"),self, SLOT("reject()"))              
        
    def validateCode(self):
        newCode = self.myCode.text()
        codes = []
        for projs in self.myTaskList:
            codes.append(projs[1])
        if newCode in codes:
            self.myCode.selectAll()
            self.myCode.setFocus()
            self.msgLabel.setText("Existe un tasko con ese Codigo")
        else:
            self.msgLabel.setText("Codigo correcto")
        pass
    
    
    
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
        