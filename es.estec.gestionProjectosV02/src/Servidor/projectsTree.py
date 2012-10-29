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
                msgStr=' '*5*len(right)+ "{0}: {1}".format(row[3],row[4])
                print msgStr
                right.append(row[2])
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
            cur.close()        
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
        return right + 1   
    
if __name__ == "__main__":
    myDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'proj',charset="utf8",use_unicode=True)
    myProjs = projectsTree(myDB)
    myProjs.rebuild_tree(1, 1)
    myProjs.display_children_AL(1, 0)
    myProjs.display_children(1) 