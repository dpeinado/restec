# -*- coding: utf-8 -*-
'''
Created on 02/10/2012

@author: bicho
'''

import MySQLdb
import sys

class myDb(object):
    '''
    Clase mi base de datos. Se encarga de interaccionar con la base de datos MySql
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
        except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit (1)
                
    def disconnect(self):
        try:
            self.__conn.commit()
            self.__conn.close()
        except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit (1)
    def get_project_list(self):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Proyectos")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en get_project_list",))
        finally:
            if cur:
                cur.close()
    
    def get_resource_list(self):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Recursos")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en get_resource_list",))
        finally:
            if cur:
                cur.close()
 
    def get_activity_list(self):
        try:
            cur=self.__conn.cursor()
            cur.execute("SELECT * from Fases")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en get_activities_list",))
        finally:
            if cur:
                cur.close()
    def get_task_list(self, grouping):
        """Grouping:
                0, no grouping at all
                1, Resource,Project,Activity
                2, Resource,Project,
                3, Project, Activity
                4, Project"""
        try:
            cur=self.__conn.cursor()
            if grouping == 0:
                cur.execute("""select nombre, Codigo, descripcion, fase, segundos, creation_time, 
                    update_time from recursos, Proyectos, fases, Cargas 
                    where recursos.Idrecurso=Cargas.IdRecurso 
                    and Proyectos.idProyecto=Cargas.idProyecto
                    and fases.idfase = Cargas.idfase""")
            elif grouping == 1:
                cur.execute("""select nombre, Codigo, descripcion, fase, SUM(segundos)
                    from recursos, Proyectos, fases, Cargas 
                    where recursos.Idrecurso=Cargas.IdRecurso 
                    and Proyectos.idProyecto=Cargas.idProyecto
                    and fases.idfase = Cargas.idfase
                    group by Cargas.IdRecurso, Cargas.IdProyecto, Cargas.IdFase""")                
            elif grouping == 2:
                cur.execute("""select nombre, Codigo, descripcion, SUM(segundos)
                    from recursos, Proyectos, Cargas 
                    where recursos.Idrecurso=Cargas.IdRecurso 
                    and Proyectos.idProyecto=Cargas.idProyecto
                    group by Cargas.IdRecurso, Cargas.IdProyecto""")
            elif grouping == 3:
                cur.execute("""select Codigo, descripcion, fase, SUM(segundos)
                    from Proyectos, fases, Cargas 
                    where Proyectos.idProyecto=Cargas.idProyecto
                    and fases.idfase = Cargas.idfase
                    group by Cargas.IdProyecto, Cargas.IdFase""")
            elif grouping == 4:
                cur.execute("""select Codigo, descripcion, SUM(segundos)
                    from Proyectos, Cargas 
                    where Proyectos.idProyecto=Cargas.idProyecto
                    group by Cargas.IdProyecto""")
                
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error {0}".format(e.args)
            return (False, ("Error en get_task_list",))
        finally:
            if cur:
                cur.close()    
    def get_task_raw_list(self):
        try:
            cur=self.__conn.cursor()
            cur.execute("select * from Cargas")
            desc = cur.description
            rows = cur.fetchall()
            cabeceras = tuple([cab[0] for cab in desc])
            return (True,(cabeceras,rows))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en get_task_raw_list",))
        finally:
            if cur:
                cur.close()
    def set_new_project(self, Codigo, Descripcion):
        try:
            cur=self.__conn.cursor()
            cur.execute ("INSERT INTO Proyectos(Codigo,Descripcion) VALUES(%s,%s)",(Codigo,Descripcion))
            return (True, ("Insertado nuevo proyecto",))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en set_new_project",))
        
    def set_new_resource(self, Nombre, Coste):
        try:
            cur=self.__conn.cursor()
            cur.execute ("INSERT INTO Recursos(Nombre, Coste) VALUES(%s,%s)",(Nombre,Coste))
            return (True, ("Insertado nuevo recurso",))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en set_new_resource",))
    def set_new_activity(self, Fase):
        try:
            cur=self.__conn.cursor()
            cur.execute ("INSERT INTO Fases(Fase) VALUES(%s)",(Fase))
            return (True, ("Insertado nueva fase",))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en set_new_activity",))

    def set_new_task(self, IdRecurso,IdProyecto,IdFase,segundos):
        try:
            cur=self.__conn.cursor()
            cur.execute ("""INSERT INTO Cargas(IdRecurso,IdProyecto,IdFase,segundos) 
            VALUES(%s,%s,%s,%s)""",(IdRecurso,IdProyecto,IdFase,segundos))
            return (True, ("Insertado nueva Carga",))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return (False, ("Error en set_new_activity",))

def print_tuples(data):
    for detail in data[0]:
        print detail, "\t",
    print
    for row in data[1]:
        for detail in row:
            print detail, "\t",
        print    
        
def main():
    InPr = myDb('localhost', 'puser','pu8549','proyectos')
    InPr.connect()
    print "me conecté"

    for i in range(10):
        ok,lista = InPr.set_new_task('1', '1', '1', '300')
        
    for i in range(10):
        ok,lista = InPr.set_new_task('1', '1', '2', '300')

    for i in range(10):
        ok,lista = InPr.set_new_task('1', '2', '3', '300')
 
    ok,lista = InPr.get_task_list(3)
    print_tuples(lista)
    ok,lista = InPr.get_task_list(4)
    print_tuples(lista)
   
    InPr.disconnect()
    print "me desconecté"
main()