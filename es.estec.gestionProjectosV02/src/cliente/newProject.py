# -*- coding: UTF-8 -*-
'''
Created on 15/10/2012

@author: bicho
'''

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class newProjectDlg(QDialog):
    '''
    classdocs
    '''
    def __init__(self, myPT,isProject,parent=None):
        super(newProjectDlg,self).__init__(parent)
        self.setMinimumSize(300,200)
        self.isProject=isProject
        self.myPT = myPT
        
        self.msgLabel = QLabel("Ok")
        
        if isProject:        
            self.myCode = QLineEdit("")
            codeLabel = QLabel(u"Código")
            codeLabel.setBuddy(self.myCode)        
            self.myCode.setInputMask("AA999")
        
        self.myDesc = QLineEdit("")            
        descLabel = QLabel(QString(u"Descripción"))
        descLabel.setBuddy(self.myDesc)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        

        if isProject:
            sizePolicy.setHeightForWidth(self.myCode.sizePolicy().hasHeightForWidth())
            self.myCode.setSizePolicy(sizePolicy)
            self.myCode.setMinimumSize(QSize(60, 22))
            self.myCode.setMaximumSize(QSize(60, 22))
            self.myCode.setMaxLength(3)
        
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(okButton)
        hbox3.addWidget(cancelButton)
        hbox1 = QHBoxLayout()
        if isProject:
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
        
        if isProject:
            self.myCode.editingFinished.connect(self.validateCode)
        
        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"),self, SLOT("reject()"))              
        
    def validateCode(self):  
        newCode = self.myCode.text().toUpper()
        if not (newCode.startsWith('PR') or newCode.startsWith('OF')):
            self.myCode.selectAll()
            self.myCode.setFocus()
            self.msgLabel.setText("El código empieza por PR u OF")
            return
        self.myCode.setText(newCode)
        codes = []
        myKs = self.myPT.myProjects.keys()
        for key in myKs:
            myCod=self.myPT.myProjects[key][4]
            codes.append(myCod)
        if newCode in codes:
            self.myCode.selectAll()
            self.myCode.setFocus()
            self.msgLabel.setText("Existe un projecto con ese Codigo")
        else:
            self.msgLabel.setText("Codigo correcto")
    
if __name__ == "__main__":
    app=QApplication(sys.argv)
    projects = []
    current = 1
    form = newProjectDlg(projects)
    form.show()
    if form.exec_():
        print "AceptŽ"
    else:
        print "CancelŽ"
        