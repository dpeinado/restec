# -*- coding: utf-8 -*-
'''
Created on 15/10/2012

@author: bicho
'''

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class newResourceDlg(QDialog):
    '''
    classdocs
    '''
    def __init__(self, myResourceList,parent=None):
        super(newResourceDlg,self).__init__(parent)
        self.setMinimumSize(300,200)
        self.myResourceList = myResourceList
        self.msgLabel = QLabel("Ok")
        nameLabel = QLabel("Nombre")
        costLabel = QLabel(QString("Coste"))
        self.myName = QLineEdit("")
        self.myCost = QLineEdit("")
        nameLabel.setBuddy(self.myName)
        costLabel.setBuddy(self.myCost)
        self.myCost.setInputMask("00.0")
        self.myCost.setMinimumSize(QSize(40, 22))
        self.myCost.setMaximumSize(QSize(40, 22))
        self.myCost.setMaxLength(4)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(okButton)
        hbox3.addWidget(cancelButton)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(nameLabel)
        hbox1.addWidget(self.myName)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(costLabel)
        hbox2.addWidget(self.myCost)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.msgLabel)
        self.setLayout(vbox)
        #self.myCode.editingFinished.connect(self.validateCode)
        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"),self, SLOT("reject()"))              
        
    #===========================================================================
    # def validateCode(self):
    #    newCode = self.myCode.text()
    #    codes = []
    #    for projs in self.myResourceList:
    #        codes.append(projs[1])
    #    if newCode in codes:
    #        self.myCode.selectAll()
    #        self.myCode.setFocus()
    #        self.msgLabel.setText("Existe un Resourceo con ese Codigo")
    #    else:
    #        self.msgLabel.setText("Codigo correcto")
    #    pass
    #===========================================================================
    
    
    
if __name__ == "__main__":
    app=QApplication(sys.argv)
    Resources = []
    current = 1
    form = newResourceDlg(Resources)
    form.show()
    if form.exec_():
        print "AceptŽ"
    else:
        print "CancelŽ"
        