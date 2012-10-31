# -*- coding: UTF-8 -*-
'''
Created on 25/10/2012

@author: diego.peinado
'''

import MySQLdb


# parent is the parent of the children we want to see   
# level is increased when we go deeper into the tree,   
#        used to display a nice indented tree
def display_children(cur, parent, level):
    #retrieve all children of parent 
    if parent is None:
        msgStr="SELECT IdProject, IdProjectParent, Code, Description from projects where IdprojectParent is NULL"
    else:
        msgStr="SELECT IdProject, IdProjectParent, Code, Description from projects where IdprojectParent = {}".format(parent)
    cur.execute(msgStr)
    result = cur.fetchall()
    # display each child
    for row in result:
        msgStr ="{0}: {1}".format(row[2],row[3])
        msg2 = ' '*level*5
        msg2=msg2+msgStr 
        print msg2
        display_children(cur,row[0],level+1)

def rebuild_tree(cur, parent, left):
    # the right value of this node is the left value + 1
    # ahora mismo este valor no es el de right. Al final de la recurrencia lo será. Ahora es solo
    # El valor left del próximo nivel    
    right = left+1  
    # get all children of this node 
    msgStr="SELECT IdProject FROM projects where IdprojectParent = {}".format(parent)
    cur.execute(msgStr)   
    result = cur.fetchall()
    for row in result:
        right = rebuild_tree(cur,row[0],right) 
    msgStr="UPDATE projects SET lft = {0}, rgt = {1} WHERE IdProject = {2}".format(left,right,parent)
    cur.execute(msgStr)
    
    return right + 1
   

def main():
    
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
        msgStr = "INSERT INTO PROJECTS(IdProject,Code,Description) VALUES({0},'{1}','{2}')".format(1,'','Proyectos')
        ok = curNew.execute(msgStr)
        for pp in data:
            idP = int(pp[0])+1
            misCodes[idP] = pp[1]
            msgStr = "INSERT INTO PROJECTS(IdProject,IdProjectParent,Code,Description) VALUES({0},{1},'{2}','{3}')".format(idP,1,pp[1],pp[2])
            ok = curNew.execute(msgStr)
        newDB.commit()
 
        curOld.execute("select * from tasks order by idprojectparent, idtaskparent")
        data = curOld.fetchall()
        idP = 50
        oldIndexes = {}
        for entrada in data:
            if entrada[2] is None:
                indx = entrada[1]+1
            else:
                indx = oldIndexes[entrada[2]]
            oldIndexes[entrada[0]]=idP
            code = misCodes[int(entrada[1])+1]
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
        display_children(curNew,None,0)
        rebuild_tree(curNew,1,1)
        newDB.commit()
    except MySQLdb.Error, e:
        print "Error {0}".format(e)   
    

main()
