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
    right = left+1  
    # get all children of this node 
    cur.execute()
    result = mysql_query('SELECT title FROM tree '.   <br>  
                           'WHERE parent="'.$parent.'";');   <br>  
    while ($row = mysql_fetch_array($result)) {   <br>  
        // recursive execution of this function for each   <br>  
        // child of this node   <br>  
        // $right is the current right value, which is   <br>  
        // incremented by the rebuild_tree function   <br>  
        $right = rebuild_tree($row['title'], $right);   <br>  
    }   <br>  
   <br>  
    // we've got the left value, and now that we've processed   <br>  
    // the children of this node we also know the right value   <br>  
    mysql_query('UPDATE tree SET lft='.$left.', rgt='.   <br>  
                 $right.' WHERE title="'.$parent.'";');   <br>  
   <br>  
    // return the right value of this node + 1   <br>  
    return $right+1;   <br>  
}   <br>  
?>  <?php   <br>  
function rebuild_tree($parent, $left) {   <br>  
    // the right value of this node is the left value + 1   <br>  
    $right = $left+1;   <br>  
   <br>  
    // get all children of this node   <br>  
    $result = mysql_query('SELECT title FROM tree '.   <br>  
                           'WHERE parent="'.$parent.'";');   <br>  
    while ($row = mysql_fetch_array($result)) {   <br>  
        // recursive execution of this function for each   <br>  
        // child of this node   <br>  
        // $right is the current right value, which is   <br>  
        // incremented by the rebuild_tree function   <br>  
        $right = rebuild_tree($row['title'], $right);   <br>  
    }   <br>  
   <br>  
    // we've got the left value, and now that we've processed   <br>  
    // the children of this node we also know the right value   <br>  
    mysql_query('UPDATE tree SET lft='.$left.', rgt='.   <br>  
                 $right.' WHERE title="'.$parent.'";');   <br>  
   <br>  
    // return the right value of this node + 1   <br>  
    return $right+1;   <br>  
}   <br>  
?>  

def main():
    
    try:
        newDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'proj',charset="utf8",use_unicode=True)
        oldDB=MySQLdb.connect(host = 'localhost', user = 'puser', passwd = 'pu8549', db = 'projects',charset="utf8",use_unicode=True)
    except MySQLdb.Error, e:
        print "Error {0}".format(e)   

    try:
        curNew=newDB.cursor()
        curOld=oldDB.cursor()
        
#===============================================================================
#        curOld.execute("Select * from resources")
#        data = curOld.fetchall()
#        for pp in data:
#            msgStr = "INSERT INTO resources(IdResource,Name,Cost) VALUES({0},'{1}','{2}')".format(pp[0],pp[1],pp[2])
#            ok = curNew.execute(msgStr)
#        newDB.commit()
#        
#        curOld.execute("Select * from Activities")
#        data = curOld.fetchall()
#        for pp in data:
#            msgStr = "INSERT INTO activities(IdActivity,Activity) VALUES({0},'{1}')".format(pp[0],pp[1])
#            ok = curNew.execute(msgStr)
#        newDB.commit()    
#        
#        curOld.execute("Select * from projects")
#        data = curOld.fetchall()
#        
#        misCodes={}
#        msgStr = "INSERT INTO PROJECTS(IdProject,Code,Description) VALUES({0},'{1}','{2}')".format(1,'','Proyectos')
#        ok = curNew.execute(msgStr)
#        for pp in data:
#            idP = int(pp[0])+1
#            misCodes[idP] = pp[1]
#            msgStr = "INSERT INTO PROJECTS(IdProject,IdProjectParent,Code,Description) VALUES({0},{1},'{2}','{3}')".format(idP,1,pp[1],pp[2])
#            ok = curNew.execute(msgStr)
#        newDB.commit()
# 
#        curOld.execute("select * from tasks order by idprojectparent, idtaskparent")
#        data = curOld.fetchall()
#        idP = 50
#        oldIndexes = {}
#        for entrada in data:
#            if entrada[2] is None:
#                indx = entrada[1]+1
#            else:
#                indx = oldIndexes[entrada[2]]
#            oldIndexes[entrada[0]]=idP
#            code = misCodes[int(entrada[1])+1]
#            msgStr = "INSERT INTO PROJECTS(IdProject,IdProjectParent,Code,Description) VALUES({0},'{1}','{2}','{3}')".format(idP,indx,code,entrada[3])
#            ok = curNew.execute(msgStr)
#            idP += 1
#        newDB.commit()
#        curOld.execute("select * from entries order by idproject, idtask")
#        data = curOld.fetchall()
#        for entrada in data:
#            if entrada[3] is None:
#                indx = entrada[2]
#            else:
#                indx = oldIndexes[entrada[3]]
#            msgStr = """INSERT INTO ENTRIES(IdEntry,IdResource,IdProject,IdActivity,Tsec,creation_time,update_time) 
#                VALUES({0},{1},{2},{3},{4},'{5}','{6}')""".format(entrada[0],entrada[1],indx,entrada[4],entrada[5],entrada[6],entrada[7])
#            ok = curNew.execute(msgStr)
#        newDB.commit()
#===============================================================================
        display_children(curNew,None,0)
    except MySQLdb.Error, e:
        print "Error {0}".format(e)   
    

main()
