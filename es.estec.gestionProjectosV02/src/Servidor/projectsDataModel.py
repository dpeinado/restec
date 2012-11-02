# -*- coding: UTF-8 -*-
'''
Created on 29/10/2012

@author: diego.peinado
'''
import MySQLdb

class projectsTree(object):
    '''
    Clase que encapsula la estructura de datos del �rbol de proyectos
    '''
    def __init__(self, connDB):
        '''
        Inicializa el conector a la base de datos
        '''
        self.conn = connDB
    def display_children_AL(self,parent, level):
        #retrieve all children of parent 
        if parent is None:
            msgStr="SELECT IdProject, IdProjectParent, Code, Description from projects where IdprojectParent is NULL"
        else:
            msgStr="SELECT IdProject, IdProjectParent, Code, Description from projects where IdprojectParent = {}".format(parent)
        try:
            cur = self.conn.cursor()
            cur.execute(msgStr)
            result = cur.fetchall()
            # display each child
            for row in result:
                msgStr ="{0}: {1}".format(row[2],row[3])
                msg2 = ' '*level*5
                msg2=msg2+msgStr
                msg2 = msg2.ljust(90)
                msg2=msg2+str(row[0])
                print msg2
                self.display_children_AL(row[0],level+1)
            cur.close()
        except MySQLdb.Error, e:
            print "Error {0}".format(e)        

    def display_children(self,root):
        try:
            cur = self.conn.cursor() 
            # retrieve left and right value of the root node
            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(root)        
            cur.execute(msgStr)   
            row = cur.fetchone()
            # start with an empty right stack
            right = [];
            # retrieve all descendants of the root node
            msgStr="""SELECT IdProject, lft, rgt , Code, Description FROM projects WHERE
                        lft BETWEEN {0} AND {1} ORDER BY lft ASC""".format(row[0],row[1])
            cur.execute(msgStr)
            data = cur.fetchall()
            cur.close()
            for row in data:
                if(len(right)>0):
                    while right[-1] < row[1]:
                        right.pop()
                msgStr=' '*5*len(right)+ "{0} {1}: {2}".format(row[0], row[3],row[4])
                print msgStr
                right.append(row[2])
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            
    def path_node(self,node):
        try:
            cur = self.conn.cursor() 
            # retrieve left and right value of the root node
            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(node)        
            cur.execute(msgStr)   
            row = cur.fetchone()
            msgStr="""SELECT IdProject FROM projects WHERE
                        lft < {0} AND rgt > {1} ORDER BY lft ASC""".format(row[0],row[1])
            cur.execute(msgStr)
            data = cur.fetchall()
            cur.close()
            pathnode=[]           
            for row in data:
                pathnode.append(row[0])
            pathnode.append(node)
            cur.close()
            return pathnode
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
    def numberDescendents(self,node):
        try:
            cur = self.conn.cursor() 
            # retrieve left and right value of the root node
            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(node)        
            cur.execute(msgStr)   
            row = cur.fetchone()
            cur.close()        
            return (row[1]-row[0]-1)/2                                    
        except MySQLdb.Error, e:
            print "Error {0}".format(e)                                    

    def insertNode_AL(self,code,description,parentID):
        try:
            cur = self.conn.cursor()
            msgStr="INSERT INTO projects(Code,Description,IdProjectParent) VALUES('{0}','{1}',{2})".format(code,description,parentID)
            cur.execute(msgStr)            
            cur.close()
            #self.conn.commit()            
            self.rebuild_tree(1, 1)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            
    def getLeaves(self):
        try:
            cur = self.conn.cursor() 
            
            msgStr="SELECT IdProject FROM projects where rgt = lft + 1"        
            cur.execute(msgStr)   
            data= cur.fetchall()
            result=[]
            for row in data:
                result.append(row[0])
            cur.close()
            return result
        except MySQLdb.Error, e:
            print "Error {0}".format(e)    
            return [None,]
    def insertNode(self,code,description,parentID):
        try:
            cur = self.conn.cursor() 
            # retrieve left and right value of the root node
            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(parentID)        
            cur.execute(msgStr)   
            row = cur.fetchone()
            cmpVal = row[1]-1
            msgStr="UPDATE projects SET rgt = rgt + 2 WHERE rgt > {0}".format(cmpVal)
            cur.execute(msgStr)
            msgStr="UPDATE projects SET lft = lft + 2 WHERE lft > {0}".format(cmpVal)
            cur.execute(msgStr)
            msgStr="""INSERT INTO projects(IdProjectParent,lft,rgt,Code,Description) 
                        VALUES({0},{1},{2},'{3}','{4}')""".format(parentID,row[1],row[1]+1,code,description)
            cur.execute(msgStr)                                    
            cur.close()
        except MySQLdb.Error, e:
            print "Error {0}".format(e)            
                                                        
    def rebuild_tree(self, parent, left):
        # the right value of this node is the left value + 1
        # ahora mismo este valor no es el de right. Al final de la recurrencia lo ser�. Ahora es solo
        # El valor left del pr�ximo nivel    
        right = left+1  
        # get all children of this node
        try:
            cur = self.conn.cursor() 
            msgStr="SELECT IdProject FROM projects where IdprojectParent = {}".format(parent)        
            cur.execute(msgStr)   
            result = cur.fetchall()
            for row in result:
                right = self.rebuild_tree(row[0],right) 
            msgStr="UPDATE projects SET lft = {0}, rgt = {1} WHERE IdProject = {2}".format(left,right,parent)
            cur.execute(msgStr)
            #self.conn.commit()
            cur.close()        
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
        return right + 1   

class resultsTree(object):
    '''
    Clase que encapsula la estructura de datos del �rbol de resultados
    '''
    def __init__(self, connDB):
        '''
        Inicializa el conector a la base de datos
        '''
        self.conn = connDB

    def display_children(self,root):
        try:
            cur = self.conn.cursor() 
            # retrieve left and right value of the root node
            msgStr="SELECT lft, rgt FROM tmpResults where Idproject = {}".format(root)        
            cur.execute(msgStr)   
            row = cur.fetchone()
            # start with an empty right stack
            right = [];
            # retrieve all descendants of the root node
            msgStr="""SELECT IdProject, lft, rgt , Tsec FROM tmpResults WHERE
                        lft BETWEEN {0} AND {1} ORDER BY lft ASC""".format(row[0],row[1])
            cur.execute(msgStr)
            data = cur.fetchall()
            cur.close()
            for row in data:
                if(len(right)>0):
                    while right[-1] < row[1]:
                        right.pop()
                msgStr=' '*5*len(right)+ "{0} --> {1}".format(row[0], row[3])
                print msgStr
                right.append(row[2])
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            
    def path_node(self,node):
        try:
            cur = self.conn.cursor() 
            # retrieve left and right value of the root node
            msgStr="SELECT lft, rgt FROM tmpResults where Idproject = {}".format(node)        
            cur.execute(msgStr)   
            row = cur.fetchone()
            msgStr="""SELECT IdProject FROM tmpResults WHERE
                        lft < {0} AND rgt > {1} ORDER BY lft ASC""".format(row[0],row[1])
            cur.execute(msgStr)
            data = cur.fetchall()
            cur.close()
            pathnode=[]           
            for row in data:
                pathnode.append(row[0])
            pathnode.append(node)
            cur.close()
            return pathnode
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
    def numberDescendents(self,node):
        try:
            cur = self.conn.cursor() 
            # retrieve left and right value of the root node
            msgStr="SELECT lft, rgt FROM tmpResults where Idproject = {}".format(node)        
            cur.execute(msgStr)   
            row = cur.fetchone()
            cur.close()        
            return (row[1]-row[0]-1)/2                                    
        except MySQLdb.Error, e:
            print "Error {0}".format(e)                                    
                                                        
    def rebuild_tree(self, parent, left):
        # the right value of this node is the left value + 1
        # ahora mismo este valor no es el de right. Al final de la recurrencia lo ser�. Ahora es solo
        # El valor left del pr�ximo nivel    
        right = left+1  
        # get all children of this node
        try:
            cur = self.conn.cursor() 
            msgStr="SELECT IdProject FROM tmpResults where IdprojectParent = {}".format(parent)        
            cur.execute(msgStr)   
            result = cur.fetchall()
            for row in result:
                right = self.rebuild_tree(row[0],right) 
            msgStr="UPDATE tmpResults SET lft = {0}, rgt = {1} WHERE IdProject = {2}".format(left,right,parent)
            cur.execute(msgStr)
            #self.conn.commit()
            cur.close()        
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
        return right + 1       

def get_entries(myP):
    try:
        cur=myP.conn.cursor()
        msgStr="select idproject,idresource, idactivity, sum(Tsec)/60 from entries group by idproject,idresource,idactivity order by idproject"
        cur.execute(msgStr)
        data = cur.fetchall()
        myL = []
        result={}
        for row in data:
            myP = row[0]
            if len(myL)==0:
                myL.append(row)
            else:
                prevP = myL[-1][0]
                if myP == prevP:
                    myL.append(row)
                else:
                    result[prevP]=myL
                    myL=[row]
        result[prevP]=myL
        return result
    except MySQLdb.Error, e:
        print "Error {0}".format(e)    
    pass        
    
if __name__ == "__main__":
    myDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'proj',charset="utf8",use_unicode=True)
    myProjs = projectsTree(myDB)    
    #===========================================================================
    myProjs.rebuild_tree(1, 1)
    # myProjs.display_children_AL(1, 0)
    myProjs.display_children(1) 
    # myPath = myProjs.path_node(55)
    # print myPath
    # for i in range(1,56):
    #   num = myProjs.numberDescendents(i)
    #   print i, num
    # myProjs.insertNode('PR034', 'COLORITOS', 34)
    # myProjs.insertNode('PR034', 'noCOLORITOS', 54)
    # myProjs.getLeaves()
    # myProjs.conn.commit()
    #===========================================================================
    
    entries= get_entries(myProjs)
    projWithEntries = sorted(entries.keys())

    cur=myDB.cursor()
    
    cur.execute("DROP TABLE IF EXISTS tmp1")
    cur.execute("CREATE TABLE tmp1(Id INT PRIMARY KEY AUTO_INCREMENT, IdProject INT, IdProjectParent INT, IdResource INT, IdActivity INT, Tsec real) ENGINE=INNODB character set utf8")
    cur.execute("TRUNCATE tmp1")    
    for mP in projWithEntries:        
        myC = myProjs.path_node(mP)
        for myE in entries[mP]:
            for upP in myC:                            
                myPPath = myProjs.path_node(upP)
                if len(myPPath)==1:
                    msgStr="INSERT INTO tmp1(IdProject,IdResource,IdActivity,Tsec) VALUES({0},{1},{2},{3})".format(upP, myE[1], myE[2], myE[3])
                else:
                    myPP = myPPath[-2]
                    msgStr="INSERT INTO tmp1(IdProject,IdProjectParent,IdResource,IdActivity,Tsec) VALUES({0},{1},{2},{3},{4})".format(upP, myPP, myE[1], myE[2], myE[3])
                cur.execute(msgStr)                
    myDB.commit()
    cur.execute("DROP TABLE IF EXISTS tmpResults")
    cur.execute("CREATE TABLE tmpResults(Id INT PRIMARY KEY AUTO_INCREMENT, IdProject INT, IdProjectParent INT, lft INT, rgt INT, Tsec real) ENGINE=INNODB character set utf8 ")
    msgStr = "INSERT INTO tmpResults(IdProject,IdProjectParent,Tsec) SELECT idproject,idprojectparent,sum(tsec) from tmp1 group by idproject order by idproject"            
    cur.execute(msgStr)
    myDB.commit()
    myRes = resultsTree(myDB)
    myRes.rebuild_tree(1,1)
    myDB.commit()
    myRes.display_children(1)
    pass                    