import sqlite3
import time

#
#class to modify database
#TODO ADD DELETE FUNCTION TO REMOVE ITEM FROM DB
class DbsMgr():
    #
    #connect to DB. try to create tables if not already done.
    #
    def __init__(self, dbFile):
        self.dbconn = sqlite3.connect(dbFile)
        self.db = self.dbconn.cursor()
        self.db.execute('''CREATE TABLE IF NOT EXISTS scope (
                         date DATE NOT NULL,
                         domain VARCHAR UNIQUE
                         );''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS urls (
                         date DATE NOT NULL,
                         url VARCHAR NOT NULL,
                         source VARCHAR NOT NULL,
                         parameters VARCHAR
                         );''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS domains (
                         date DATE NOT NULL,
                         domain VARCHAR UNIQUE
                         );''')

#
#Generic insert function. All tables contain date column so current
#date/time is always added. If unique columns are set and a dup is
#attempted to be inserted catch this error and continue, this should
#prevent duplicates.
#
    def insert(self,table,values):
        value = '?,'*len(values)
        value = value[:-1]
        query = 'INSERT INTO '+table+' VALUES (DateTime(\'now\'),'+value+');'
        try:
            self.db.execute(query,values)
            self.dbconn.commit()
        except sqlite3.IntegrityError:
            pass

#
#Generic select. should return list of columns selected. columns are
#taken as a list.
#
    def select(self,columns,table):
        retl = []
        column = ",".join(columns)
        query = 'SELECT '+column+' FROM '+table+';'
        self.db.execute(query)
        for row in self.db.fetchall():
            for item in row:
                retl.append(item)
        return retl

#
#select columns that match string i.e. WHERE %google%
#               
    def selectwhere(self,column,table,item,match):
        retl = []
        query = 'SELECT '+column+' FROM '+table+' WHERE '+item+' LIKE \"%'+match+'%\";'
        self.db.execute(query)
        for row in self.db.fetchall():
            for item in row:
                retl.append(item)
        return retl

#
#Close connection when object is destroyed.
#
    def __del__(self):
        self.dbconn.close()



