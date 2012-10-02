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
    def connect(self):
        try:
            self.__conn = MySQLdb.connect(host = self.__host,
                                   user = self.__user,
                                   passwd = self.__userpwd,
                                   db = self.__database)
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
                
def main():
    InPr = myDb('localhost', 'puser','pu8549','proyectos')
    InPr.connect()
    print "me conecte"
    InPr.disconnect()
    print "me desconecte"
main()