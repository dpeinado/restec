# -*- coding: UTF-8 -*-
'''
Created on 29/10/2012

@author: diego.peinado
'''
import MySQLdb
import operator

class ProjectTreeDB(object):
    '''
    Clase une la base de datos con la clase ProjectTree. Es un helper    
    '''
    def __init__(self,miPT,connDB):
        self.conn = connDB
        self.myPT = miPT
    def updateTree(self):
        msgStr="""SELECT IdProject, IdProjectParent, lft, rgt , Code, Description FROM projects 
                    ORDER BY lft ASC"""
        self.myPT.myProjects={}
        self.myPT.projFromLft={}
        self.myPT.rgtFromLft={}
        try:
            cur=self.conn.cursor()
            cur.execute(msgStr)
            data=cur.fetchall()
            cur.close()
            for row in data:
                myP=[row[0],row[1],row[2],row[3],row[4],row[5]]
                self.myPT.myProjects[row[0]]=myP
                self.myPT.projFromLft[row[2]]=row[0]
                self.myPT.rgtFromLft[row[2]]=row[3]                
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
            msgStr="SELECT * FROM projects where lft = {}".format(row[1])        
            cur.execute(msgStr)   
            row = cur.fetchone()            
            cur.close()
            self.updateTree()
            return row      
        except MySQLdb.Error, e:
            print "Error {0}".format(e)    
            self.conn.rollback()

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
            self.conn.commit()
            cur.close()
            self.updateTree()
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
        return right + 1   

                         
class ProjectTree(object):
    '''
    Clase que encapsula la estructura de datos del árbol de proyectos
    No interactua con la base de datos. Para eso está el helper ProjectTreeDB
    '''
    def __init__(self):
        '''
        Inicializa el conector a la base de datos
        '''
        self.myProjects={}
        self.projFromLft = {}
        self.rgtFromLft = {}

    def __iter__(self):
        pass
        myPrs=self.myProjects.values()
        myPrs.sort(key = operator.itemgetter(1,4))
        for prj in myPrs:
            yield prj
        
        #=======================================================================
        # myKeys=self.projFromLft.keys()
        # myKeys.sort()
        # for lft in myKeys:
        #    yield self.myProjects[self.projFromLft[lft]]
        #=======================================================================

    def displayChildren(self,root):
        lft=self.myProjects[root][2]
        rgt=self.myProjects[root][3]
        myKys=self.projFromLft.keys().sort()
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
    
    def existCode(self,Code):        
        for key in self.myProjects.keys():
            if self.myProjects[key][4]==Code:
                return True
        return False
    
#===============================================================================
# if __name__ == "__main__":
#   myDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'proj',charset="utf8",use_unicode=True)
#   myProjs = ProjectTree()
#   myProjsDB = ProjectTreeDB(myProjs,myDB)
#   myProjsDB.updateTree()
#   myProjs.displayChildren(1)
#   print myProjs.existCode('PR002')
#   print myProjs.path_node(76L)
#   print myProjs.numberDescendents(34)
#   print myProjs.getLeaves()
#               
#===============================================================================
