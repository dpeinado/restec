# -*- coding: utf-8 -*-
'''
Created on 02/10/2012

@author: bicho
'''

import MySQLdb
#import sys

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
        Constructor
        '''
        self.__host = host
        self.__user = user
        self.__userpwd = userpwd
        self.__database = database
        self.__conn=None
    def connect(self):
        try:
            self.__conn = MySQLdb.connect(host = self.__host,
                                   user = self.__user,
                                   passwd = self.__userpwd,
                                   db = self.__database,
                                   charset="utf8",
                                   use_unicode=True)
            return True
        except MySQLdb.Error, e:
                print "Error {0}".format(e)
                return False
                
    def disconnect(self):
        try:
            self.__conn.commit()
            self.__conn.close()
            self.__conn = None
            return True
        except MySQLdb.Error, e:
                print "Error {0}".format(e)
                return False
            
    def conn(self):
        return self.__conn
    def get_project_list(self):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Projects order by Code")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_project_list",))
        finally:
            if cur:
                cur.close()
                               
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
    
    def get_resource_list(self):
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
 
    def get_activity_list(self):
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

    def get_task_list(self, IdProject):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Tasks WHERE IdProjectParent = %s", (IdProject,))
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_Task_list",))
        finally:
            if cur:
                cur.close()
                
    def get_task_byId(self, IdProject, IdTask):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Tasks WHERE IdTask = %s and IdProjectParent = %s", (IdTask,IdProject))
            if cur.rowcount == 1:
                row = cur.fetchone()
                return (True,row)
            else:
                return(False,())
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            return (False, ("Error en get_task_byId", IdTask))
        finally:
            if cur:
                cur.close()    
    
    def get_task_entries_timeTotal(self,IdResource,IdProject,IdActivity,IdTask=None):
        try:
            cur=self.__conn.cursor()
            if IdTask is not None:
                cur.execute("""SELECT SUM(Tsec) from Entries where IdResource = %s and IdProject = %s and
                        IdActivity = %s and IdTask = %s""",(IdResource,IdProject,IdActivity,IdTask))
            else:
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
                
    def set_new_project(self, Code, Description):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Projects WHERE Code = %s", (Code,))
            if cur.rowcount > 0:
                return (False, ("Proyecto existente con este mismo código",))
            cur.execute("SELECT * from Projects WHERE Description LIKE %s", (Description,))
            if cur.rowcount > 0:
                return (False, ("Proyecto existente con esta misma descripción",))
            # Parece que no existe un proyecto igual ... luego inserto
            cur.execute ("INSERT INTO Projects(Code,Description) VALUES(%s,%s)",(Code,Description))
            self.__conn.commit()
            cur.execute("select * from Projects where Code = %s",(Code,))
            row = cur.fetchone()
            return (True, row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            self.__conn.rollback()
            return (False, ("Error en set_new_project",))
        finally:
            if cur:
                cur.close()
    def set_new_resource(self, Name, Cost):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Resources WHERE Name LIKE %s", (Name,))
            if cur.rowcount > 0:
                return (False, ("Recurso existente con este mismo Nombre",))
            # Parece que no existe un recurso igual ... luego inserto
            cur.execute ("INSERT INTO Resources(Name, Cost) VALUES(%s,%s)",(Name,Cost))
            self.__conn.commit()
            cur.execute("select * from resources where Name like %s",(Name,))
            row=cur.fetchone()
            return (True, row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            self.__conn.rollback()
            return (False, ("Error en set_new_resource",))
        finally:
            if cur:
                cur.close()
                
                
    def set_new_activity(self, Activity):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Activities WHERE Activity LIKE %s", (Activity,))
            if cur.rowcount > 0:
                return (False, ("Fase existente con este mismo Nombre",))
            # Parece que no existe una actividad igual ... luego inserto            
            cur.execute ("INSERT INTO Activities(Activity) VALUES(%s)",(Activity,))
            self.__conn.commit()
            cur.execute("select * from Activities where Activity like %s",(Activity,))
            row=cur.fetchone()
            return (True, row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            self.__conn.rollback()
            return (False, ("Error en set_new_activity",))
        finally:
            if cur:
                cur.close()

    def set_new_task(self, IdProjectParent, IdTaskParent, Task):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Tasks WHERE Task LIKE %s and IdProjectParent = %s", (Task,IdProjectParent))
            if cur.rowcount > 0:
                return (False, ("Tarea existente con este mismo Nombre en el mismo proyecto",))
            # Parece que no existe una fase igual ... luego inserto
            cur.execute("SELECT * from Projects where IdProject = %s",(IdProjectParent,))
            if cur.rowcount == 0:
                return (False, ("Error IdProjectParent Inexistente",))
            if IdTaskParent is not None:
                cur.execute("SELECT * from Tasks where IdTask = %s",(IdTaskParent,))
                if cur.rowcount == 0:
                    return (False, ("Error IdTaskParent Inexistente",))
            cur.execute ("INSERT INTO Tasks(IdProjectParent,IdTaskParent,Task) VALUES(%s,%s,%s)",(IdProjectParent,IdTaskParent,Task))
            self.__conn.commit()
            cur.execute("select * from tasks where IdProjectParent = %s and IdTaskParent = %s and Task like %s",(IdProjectParent,IdTaskParent,Task))
            row=cur.fetchone()
            return (True, row)
        except MySQLdb.Error, e:
            print "Error {0}".format(e)
            self.__conn.rollback()
            return (False, ("Error en set_new_task",))
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

#===============================================================================
# 
# def print_tuples(data):
# for detail in data[0]:
#     print detail, "\t",
# print
# for row in data[1]:
#     for detail in row:
#         print detail, "\t",
#     print    
#     
# def main():
# InPr = myDb('localhost', 'puser','pu8549','projects')
# InPr.connect()
# print "me conecté"
# 
# #ok, lista = InPr.set_new_task('1', None, 'Esta es una tarea con TaskParent = None') 
# ok, lista = InPr.set_new_task('102', '2', 'Esta es una tarea con TaskParent = 2')
# print_tuples(lista)
# for i in range(10):
#    ok,lista = InPr.set_new_task('2', '1', '5', '400')
#    
# for i in range(7):
#    ok,lista = InPr.set_new_task('2', '5', '4', '308')
# 
# for i in range(10):
#    ok,lista = InPr.set_new_task('3', '5', '6', '285')
# 
# ok,lista = InPr.get_task_list(0)
# print_tuples(lista)
# ok,lista = InPr.get_task_list(1)
# print_tuples(lista)
# ok,lista = InPr.get_task_list(2)
# print_tuples(lista)
# ok,lista = InPr.get_task_list(3)
# print_tuples(lista)
# ok,lista = InPr.get_task_list(4)
# print_tuples(lista)
# ok,lista = InPr.get_task_list(5)
# print_tuples(lista)
# ok,lista = InPr.get_task_list(6)
# print_tuples(lista)
#  
# InPr.disconnect()
# print "me desconecté"
# main()
#===============================================================================
