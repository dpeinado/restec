# -*- coding: utf-8 -*-
'''
Created on 15/10/2012

@author: bicho
'''

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class newActivityDlg(QDialog):
    '''
    classdocs
    '''
    def __init__(self, myActivityList,parent=None):
        super(newActivityDlg,self).__init__(parent)
        self.setMinimumSize(300,200)
        self.myActivityList = myActivityList
        self.msgLabel = QLabel("Ok")
        activityLabel = QLabel("Actividad")
        self.myActivity = QLineEdit("")
        activityLabel.setBuddy(self.myActivity)
        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(okButton)
        hbox3.addWidget(cancelButton)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(activityLabel)
        hbox1.addWidget(self.myActivity)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
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
    #    for projs in self.myActivityList:
    #        codes.append(projs[1])
    #    if newCode in codes:
    #        self.myCode.selectAll()
    #        self.myCode.setFocus()
    #        self.msgLabel.setText("Existe un Activityo con ese Codigo")
    #    else:
    #        self.msgLabel.setText("Codigo correcto")
    #    pass
    #===========================================================================
    
    
    
if __name__ == "__main__":
    app=QApplication(sys.argv)
    Activitys = []
    current = 1
    form = newActivityDlg(Activitys)
    form.show()
    if form.exec_():
        print "AceptŽ"
    else:
        print "CancelŽ"
        