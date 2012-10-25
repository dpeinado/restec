# -*- coding: UTF-8 -*-
'''
Created on 25/10/2012

@author: diego.peinado
'''

import MySQLdb

try:
    newDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'proj',charset="utf8",use_unicode=True)
    oldDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'projects',charset="utf8",use_unicode=True)
except MySQLdb.Error, e:
    print "Error {0}".format(e)   


try:
    curNew=newDB.cursor()
    curOld=oldDB.cursor()
    
    curOld.execute("Select * from resources")
    data = curOld.fetchall()
    for pp in data:
        msgStr = "INSERT INTO resources(IdResource,Name,Cost) VALUES({0},'{1}','{2}')".format(pp[0],pp[1],pp[2])
        ok = curNew.execute(msgStr)
    newDB.commit()
    
    curOld.execute("Select * from Activities")
    data = curOld.fetchall()
    for pp in data:
        msgStr = "INSERT INTO activities(IdActivity,Activity) VALUES({0},'{1}')".format(pp[0],pp[1])
        ok = curNew.execute(msgStr)
    newDB.commit()    
    
    curOld.execute("Select * from projects")
    data = curOld.fetchall()
    misCodes={}
    for pp in data:
        misCodes[pp[0]] = pp[1]
          
    for entrada in data:
        msgStr = "INSERT INTO PROJECTS(IdProject,Code,Description) VALUES({0},'{1}','{2}')".format(entrada[0],entrada[1],entrada[2])
        ok = curNew.execute(msgStr)
    newDB.commit()
    pass
    curOld.execute("select * from tasks order by idprojectparent, idtaskparent")
    data = curOld.fetchall()
    idP = 50
    oldIndexes = {}
    for entrada in data:
        if entrada[2] is None:
            indx = entrada[1]
        else:
            indx = oldIndexes[entrada[2]]
        oldIndexes[entrada[0]]=idP
        code = misCodes[entrada[1]]
        msgStr = "INSERT INTO PROJECTS(IdProject,IdProjectParent,Code,Description) VALUES({0},'{1}','{2}','{3}')".format(idP,indx,code,entrada[3])
        ok = curNew.execute(msgStr)
        idP += 1
    newDB.commit()
    curOld.execute("select * from entries order by idproject, idtask")
    data = curOld.fetchall()
    for entrada in data:
        if entrada[3] is None:
            indx = entrada[2]
        else:
            indx = oldIndexes[entrada[3]]
        msgStr = """INSERT INTO ENTRIES(IdEntry,IdResource,IdProject,IdActivity,Tsec,creation_time,update_time) 
            VALUES({0},{1},{2},{3},{4},'{5}','{6}')""".format(entrada[0],entrada[1],indx,entrada[4],entrada[5],entrada[6],entrada[7])
        ok = curNew.execute(msgStr)
    newDB.commit()
    pass
except MySQLdb.Error, e:
    print "Error {0}".format(e)   