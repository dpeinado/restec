# -*- coding: UTF-8 -*-
'''
Created on 29/10/2012

@author: diego.peinado
'''
import MySQLdb

#===============================================================================
# class Project(object):
#    '''
#    Clase que representa una fila en la tabla de proyectos
#    '''
#    def __init__(self,IdP,IdPP,lft,rgt,Code,Description):
#        self.IdP=IdP
#        self.IdPP=IdPP
#        self.lft=lft
#        self.rgt=rgt
#        self.Code=Code
#        self.Description=Description
#===============================================================================

class ProjectTree(object):
    '''
    Clase que encapsula la estructura de datos del árbol de proyectos
    '''
    def __init__(self, connDB):
        '''
        Inicializa el conector a la base de datos
        '''
        self.conn = connDB
        self.myProjects={}
        self.projFromLft = {}
        self.projFromRgt = {}
    def updateTree(self):
        msgStr="""SELECT IdProject, IdProjectParent, lft, rgt , Code, Description FROM projects 
                    ORDER BY lft ASC"""
        self.myProjects={}
        try:
            cur=self.conn.cursor()
            cur.execute(msgStr)
            data=cur.fetchall()
            cur.close()
            for row in data:
                myP=[row[0],row[1],row[2],row[3],row[4],row[5]]
                self.myProjects[row[0]]=myP
                self.projFromLft[row[2]]=row[0]
                self.projFromRgt[row[3]]=row[0]                
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
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
            self.conn.commit()
            self.updateTree()
        except MySQLdb.Error, e:
            print "Error {0}".format(e)    
                 
if __name__ == "__main__":
    myDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'proj',charset="utf8",use_unicode=True)
    myProjs = ProjectTree(myDB)
    myProjs.updateTree()
    myProjs.insertNode('PR001', 'OTRA TAREA COLGANDO DE PR001', 50)
    myKys = myProjs.projFromLft.keys()
    for lft in myKys:
        myID=int(myProjs.projFromLft[lft])
        print lft,myID,myProjs.myProjects[myID]
    pass        
#===============================================================================
#    def display_children(self,root):
#        try:
#            cur = self.conn.cursor() 
#            # retrieve left and right value of the root node
#            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(root)        
#            cur.execute(msgStr)   
#            row = cur.fetchone()
#            # start with an empty right stack
#            right = [];
#            # retrieve all descendants of the root node
#            msgStr="""SELECT IdProject, lft, rgt , Code, Description FROM projects WHERE
#                        lft BETWEEN {0} AND {1} ORDER BY lft ASC""".format(row[0],row[1])
#            cur.execute(msgStr)
#            data = cur.fetchall()
#            cur.close()
#            for row in data:
#                if(len(right)>0):
#                    while right[-1] < row[1]:
#                        right.pop()
#                msgStr=' '*5*len(right)+ "{0} {1}: {2}".format(row[0], row[3],row[4])
#                print msgStr
#                right.append(row[2])
#        except MySQLdb.Error, e:
#            print "Error {0}".format(e)
#            
#    def path_node(self,node):
#        try:
#            cur = self.conn.cursor() 
#            # retrieve left and right value of the root node
#            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(node)        
#            cur.execute(msgStr)   
#            row = cur.fetchone()
#            msgStr="""SELECT IdProject FROM projects WHERE
#                        lft < {0} AND rgt > {1} ORDER BY lft ASC""".format(row[0],row[1])
#            cur.execute(msgStr)
#            data = cur.fetchall()
#            cur.close()
#            pathnode=[]           
#            for row in data:
#                pathnode.append(row[0])
#            pathnode.append(node)
#            cur.close()
#            return pathnode
#        except MySQLdb.Error, e:
#            print "Error {0}".format(e)
#    def numberDescendents(self,node):
#        try:
#            cur = self.conn.cursor() 
#            # retrieve left and right value of the root node
#            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(node)        
#            cur.execute(msgStr)   
#            row = cur.fetchone()
#            cur.close()        
#            return (row[1]-row[0]-1)/2                                    
#        except MySQLdb.Error, e:
#            print "Error {0}".format(e)                                    
# 
#    def insertNode_AL(self,code,description,parentID):
#        try:
#            cur = self.conn.cursor()
#            msgStr="INSERT INTO projects(Code,Description,IdProjectParent) VALUES('{0}','{1}',{2})".format(code,description,parentID)
#            cur.execute(msgStr)            
#            cur.close()
#            #self.conn.commit()            
#            self.rebuild_tree(1, 1)
#        except MySQLdb.Error, e:
#            print "Error {0}".format(e)
#            
#    def getLeaves(self):
#        try:
#            cur = self.conn.cursor() 
#            
#            msgStr="SELECT IdProject FROM projects where rgt = lft + 1"        
#            cur.execute(msgStr)   
#            data= cur.fetchall()
#            result=[]
#            for row in data:
#                result.append(row[0])
#            cur.close()
#            return result
#        except MySQLdb.Error, e:
#            print "Error {0}".format(e)    
#            return [None,]
#    def insertNode(self,code,description,parentID):
#        try:
#            cur = self.conn.cursor() 
#            # retrieve left and right value of the root node
#            msgStr="SELECT lft, rgt FROM projects where Idproject = {}".format(parentID)        
#            cur.execute(msgStr)   
#            row = cur.fetchone()
#            cmpVal = row[1]-1
#            msgStr="UPDATE projects SET rgt = rgt + 2 WHERE rgt > {0}".format(cmpVal)
#            cur.execute(msgStr)
#            msgStr="UPDATE projects SET lft = lft + 2 WHERE lft > {0}".format(cmpVal)
#            cur.execute(msgStr)
#            msgStr="""INSERT INTO projects(IdProjectParent,lft,rgt,Code,Description) 
#                        VALUES({0},{1},{2},'{3}','{4}')""".format(parentID,row[1],row[1]+1,code,description)
#            cur.execute(msgStr)                                    
#            cur.close()
#        except MySQLdb.Error, e:
#            print "Error {0}".format(e)            
#                                                        
#    def rebuild_tree(self, parent, left):
#        # the right value of this node is the left value + 1
#        # ahora mismo este valor no es el de right. Al final de la recurrencia lo ser�. Ahora es solo
#        # El valor left del pr�ximo nivel    
#        right = left+1  
#        # get all children of this node
#        try:
#            cur = self.conn.cursor() 
#            msgStr="SELECT IdProject FROM projects where IdprojectParent = {}".format(parent)        
#            cur.execute(msgStr)   
#            result = cur.fetchall()
#            for row in result:
#                right = self.rebuild_tree(row[0],right) 
#            msgStr="UPDATE projects SET lft = {0}, rgt = {1} WHERE IdProject = {2}".format(left,right,parent)
#            cur.execute(msgStr)
#            #self.conn.commit()
#            cur.close()        
#        except MySQLdb.Error, e:
#            print "Error {0}".format(e)
#        return right + 1   
#===============================================================================