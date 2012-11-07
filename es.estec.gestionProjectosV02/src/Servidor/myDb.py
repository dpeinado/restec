# -*- coding: UTF-8 -*-
'''
Created on 02/10/2012

@author: bicho
'''

import MySQLdb
import sys,os
mypath = os.path.dirname(__file__)
from projectsDataModel import *
#import sys

class lineaResumen(object):
    pass
    def __init__(self,s1,s2,s3,s4,t=0.0):
        self.str1=s1
        self.str2=s2
        self.str3=s3
        self.str4=s4
        self.myT = t

class myDb(object):
    '''
    Clase mi base de datos. Se encarga de interaccionar con la base de datos MySql
    FALTA IMPLEMENTAR CONSULTAS CON PERIODOS DE FECHAS. QUIZÁ LO MEJOR ES COJER
    get_task_list QUE HASTA AHORA SOLO TIENE UN PARAMETRO (TIPO DE INFORME), CON 
    DOS PARÁMETROS OPCIONALES: FECHA INICIO, FECHA FINAL, E INCLUIR EN LA CONSULTA 
    EN INTERVALO DE FECHAS
    '''
        
    def __init__(self,host,user,userpwd,database):
        '''
        OK V02
        '''
        self.__host = host
        self.__user = user
        self.__userpwd = userpwd
        self.__database = database
        self.__conn=None
        self.myPT=ProjectTree()
    def connect(self):
        '''
        OK V02
        '''        
        try:
            self.__conn = MySQLdb.connect(host = self.__host,
                                   user = self.__user,
                                   passwd = self.__userpwd,
                                   db = self.__database,
                                   charset="utf8",
                                   use_unicode=True)
            self.myPTDB=ProjectTreeDB(self.myPT,self.__conn)
            #self.myPTDB.rebuild_tree(1, 1)
            return True
        except MySQLdb.Error, e:
                print "Error {0}".format(e)
                return False
                
    def disconnect(self):
        '''
        OK V02
        '''        
        try:
            self.__conn.commit()
            self.__conn.close()
            self.__conn = None
            return True
        except MySQLdb.Error, e:
                print "Error {0}".format(e)
                return False
            
    def conn(self):
        '''
        OK V02
        '''        
        return self.__conn
    
    def get_project_tree(self):
        '''
        OK V02
        '''        
        try:
            self.myPTDB.updateTree()
            return (True,self.myPT)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_project_list",))
                               
    def get_project_byId(self, IdProject):
        try:            
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Projects WHERE IdProject = %s", (IdProject,))
            if cur.rowcount == 1:
                row = cur.fetchone()
                return (True,row)
            else:
                return(False,())
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_project_byId", IdProject))
        finally:
            if cur:
                cur.close()                
    
    def set_new_project(self, Parent, Code, Description):
        nivel = self.myPT.path_node(int(Parent))
        if len(nivel)==1:        
            if self.myPT.existCode(Code):            
                return (False, "Proyecto existente con este mismo código","Estas fastidiado")
        newNode=self.myPTDB.insertNode(Code,Description,Parent)
        return (True, newNode, self.myPT)
    def get_task_entries_timeTotal(self,IdResource,IdProject,IdActivity):
        try:
            cur=self.__conn.cursor()
            cur.execute("""SELECT SUM(Tsec) from Entries where IdResource = %s and IdProject = %s and
                       IdActivity = %s""",(IdResource,IdProject,IdActivity))            
            row = cur.fetchone()
            return (True,row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_task_entries_timeTotal"))
        finally:
            if cur:
                cur.close()
                
                                
    def get_resource_list(self):
        '''
        OK V02
        '''        
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Resources")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_resource_list",))
        finally:
            if cur:
                cur.close()
    
    def get_resource_byId(self, IdResource):
        '''
        OK V02
        '''        
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Resources WHERE IdResource = %s", (IdResource,))
            if cur.rowcount == 1:
                row = cur.fetchone()
                return (True,row)
            else:
                return(False,())
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_resource_byId", IdResource))
        finally:
            if cur:
                cur.close()    
    def set_new_resource(self, Name, Cost):
        '''
        OK V02
        '''        
        try:
            if Cost is None:
                Cost = 0.0;
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Resources WHERE Name LIKE %s", (unicode(Name,)))
            if cur.rowcount > 0:
                return (False, ("Recurso existente con este mismo Nombre",))
            # Parece que no existe un recurso igual ... luego inserto
            cur.execute ("INSERT INTO Resources(Name, Cost) VALUES(%s,%s)",(unicode(Name),Cost))
            self.__conn.commit()
            cur.execute("select * from resources where Name like %s",(unicode(Name,)))
            row=cur.fetchone()
            return (True, row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            self.__conn.rollback()
            return (False, ("Error en set_new_resource",))
        finally:
            if cur:
                cur.close()
 
    def get_activity_list(self):
        '''
        OK V02
        '''        
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Activities")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_activities_list",))
        finally:
            if cur:
                cur.close()
                
    def get_activity_byId(self, IdResource):
        '''
        OK V02
        '''        
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Activities WHERE IdActivity = %s", (IdResource,))
            if cur.rowcount == 1:
                row = cur.fetchone()
                return (True,row)
            else:
                return(False,())
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_activity_byId", IdResource))
        finally:
            if cur:
                cur.close()    

    def set_new_activity(self, Activity):
        '''
        OK V02
        '''        
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Activities WHERE Activity LIKE %s", (unicode(Activity,)))
            if cur.rowcount > 0:
                return (False, ("Fase existente con este mismo Nombre",))
            # Parece que no existe una actividad igual ... luego inserto            
            cur.execute ("INSERT INTO Activities(Activity) VALUES(%s)",(unicode(Activity,)))
            self.__conn.commit()
            cur.execute("select * from Activities where Activity like %s",(unicode(Activity,)))
            row=cur.fetchone()
            return (True, row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            self.__conn.rollback()
            return (False, ("Error en set_new_activity",))
        finally:
            if cur:
                cur.close()
                
 

  
    def get_info_entries(self):
        try:
            cur=self.__conn.cursor()
            cur.execute("""select idproject, idtask, idresource, idactivity, sum(tsec) from 
            (select idproject, idtask, idresource, idactivity, tsec from 
            entries order by idproject, idtask, idresource, idactivity) as t 
            group by t.idproject, t.idtask, t.idresource, t.idactivity
            """)            
            entradas = cur.fetchall()                                    
            return (True,entradas)
        except MySQLdb.Error, e:
            print "Error {0}".format(e.args)
            return (False, ("Error en get_entries_list",))
        finally:
            if cur:
                cur.close()        
    def get_entries_list(self, grouping):
        """Grouping:
                0, no grouping at all
                1, Resource,Project,Activity
                2, Resource,Project,
                3, Project, Activity
                4, Project
                5, Project, Resource
                6, Project, Resource, Activity"""
        try:
            cur=self.__conn.cursor()
            if grouping == 0:
                cur.execute("""select Name, Code, Description, Activity, Tsec, creation_time, 
                    update_time from Resources, Projects, Activities, Entries 
                    where Resources.IdResource=Entries.IdResource 
                    and Projects.IdProject=Entries.IdProject
                    and Activities.IdActivity = Entries.IdActivity""")
            elif grouping == 1:
                cur.execute("""select Name, Code, Description, Activity, SUM(Tsec)
                    from Resources, Projects, Activities, Entries 
                    where Resources.IdResource=Entries.IdResource 
                    and Projects.idProject=Entries.idProject
                    and Activities.idActivity = Entries.idActivity
                    group by Entries.IdResource, Entries.IdProject, Entries.IdActivity""")                
            elif grouping == 2:
                cur.execute("""select Name, Code, Description, SUM(Tsec)
                    from Resources, Projects, Entries 
                    where Resources.IdResource=Entries.IdResource 
                    and Projects.idProject=Entries.idProject
                    group by Entries.IdResource, Entries.IdProject""")
            elif grouping == 3:
                cur.execute("""select Code, Description, Activity, SUM(Tsec)
                    from Projects, Activities, Entries 
                    where Projects.idProject=Entries.idProject
                    and Activitys.idActivity = Entries.idActivity
                    group by Entries.IdProject, Entries.IdActivity""")
            elif grouping == 4:
                cur.execute("""select Code, Description, SUM(Tsec)
                    from Projects, Entries 
                    where Projects.idProject=Entries.idProject
                    group by Entries.IdProject""")
            elif grouping == 5:
                cur.execute("""select Code, Description, Name, SUM(Tsec)
                    from Projects, Resources, Entries 
                    where Projects.idProject=Entries.idProject
                    and Resources.idResource = Entries.idResource
                    group by Entries.IdProject, Entries.IdResource""")
            elif grouping == 6:
                cur.execute("""select Code, Description, Name, Activity, SUM(Tsec)
                    from Resources, Projects, Activities, Entries 
                    where Resources.IdResource=Entries.IdResource 
                    and Projects.idProject=Entries.idProject
                    and Activitys.idActivity = Entries.idActivity
                    group by Entries.IdProject, Entries.IdResource, Entries.IdActivity""")                   
                
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error {0}".format(e.args)
            return (False, ("Error en get_entries_list",))
        finally:
            if cur:
                cur.close()    
    def get_entries_raw_list(self):
        try:
            cur=self.__conn.cursor()
            cur.execute("select * from Entries")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_entries_raw_list",))
        finally:
            if cur:
                cur.close()

    def set_new_entry(self, IdResource,IdProject,IdActivity,Tsec, IdTask=None):
        try:
            cur=self.__conn.cursor()
            if IdTask is not None:
                cur.execute ("""INSERT INTO Entries(IdResource,IdProject,IdTask,IdActivity,Tsec) 
                    VALUES(%s,%s,%s,%s,%s)""",(IdResource,IdProject,IdTask, IdActivity,Tsec))
            else:
                cur.execute ("""INSERT INTO Entries(IdResource,IdProject,IdActivity,Tsec) 
                    VALUES(%s,%s,%s,%s)""",(IdResource,IdProject,IdActivity,Tsec))          
            self.__conn.commit()
            cur.execute("select * from entries where Idresource = %s and Idproject = %s and Idactivity = %s and Tsec = %s",(IdResource,IdProject,IdActivity,Tsec))
            row=cur.fetchone()
            return (True, row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            self.__conn.rollback()
            return (False, ("Error en set_new_entry",))
        finally:
            if cur:
                cur.close()
