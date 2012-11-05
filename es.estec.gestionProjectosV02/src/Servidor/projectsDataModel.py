# -*- coding: UTF-8 -*-
'''
Created on 29/10/2012

@author: diego.peinado
'''
import MySQLdb

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
        self.rgtFromLft = {}
    def updateTree(self):
        msgStr="""SELECT IdProject, IdProjectParent, lft, rgt , Code, Description FROM projects 
                    ORDER BY lft ASC"""
        self.myProjects={}
        self.projFromLft={}
        self.rgtFromLft={}
        try:
            cur=self.conn.cursor()
            cur.execute(msgStr)
            data=cur.fetchall()
            cur.close()
            for row in data:
                myP=[row[0],row[1],row[2],row[3],row[4],row[5]]
                self.myProjects[row[0]]=myP
                self.projFromLft[row[2]]=row[0]
                self.rgtFromLft[row[2]]=row[3]                
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
            self.conn.commit()
            msgStr="UPDATE projects SET lft = lft + 2 WHERE lft > {0}".format(cmpVal)
            cur.execute(msgStr)
            self.conn.commit()
            msgStr="""INSERT INTO projects(IdProjectParent,lft,rgt,Code,Description) 
                        VALUES({0},{1},{2},'{3}','{4}')""".format(parentID,row[1],row[1]+1,code,description)
            cur.execute(msgStr)                                    
            self.conn.commit()
            cur.close()      
        except MySQLdb.Error, e:
            print "Error {0}".format(e)    
            self.conn.rollback()     
    def displayChildren(self,root):
        lft=self.myProjects[root][2]
        rgt=self.myProjects[root][3]
        myKys=self.projFromLft.keys()
        myKeys=[e for e in myKys if (e>=lft and e<=rgt)]
        right=[]
        for key in myKeys:
            row=self.myProjects[self.projFromLft[key]]
            if (len(right)>0):
                while right[-1]<row[2]:
                    right.pop()
            msgStr=' '*5*len(right)+"{0} {1}: {2}".format(row[0],row[4],row[5])
            print msgStr
            right.append(row[3])
    def path_node(self,node):
        lft=self.myProjects[node][2]
        rgt=self.myProjects[node][3]
        myKys=self.projFromLft.keys()
        myKeys=[e for e in myKys if (e<lft and self.rgtFromLft[e]>rgt)]
        pathnode=[self.projFromLft[e] for e in myKeys]
        pathnode.append(node)        
        return pathnode
    def numberDescendents(self,node):
        lft=self.myProjects[node][2]
        rgt=self.myProjects[node][3]
        return (rgt-lft-1)/2        
    def getLeaves(self):
        myKys=self.projFromLft.keys()        
        myKeys=[self.projFromLft[e] for e in myKys if (self.rgtFromLft[e]==e+1)]                
        return myKeys
    
if __name__ == "__main__":
    myDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'proj',charset="utf8",use_unicode=True)
    myProjs = ProjectTree(myDB)
    myProjs.updateTree()
    myProjs.displayChildren(34)
    myProjs.path_node(76L)
    print myProjs.numberDescendents(34)
    print myProjs.getLeaves()

                        
            
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
