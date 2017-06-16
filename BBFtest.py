from dbsMgr import DbsMgr
from sublist import Sublist
import sys
import requests
import config
import readline
from dirb import dirb

use = '''
COMMANDS:\n
setdb - choose or create the database file example: db <filename>
addscope - add comma seperated(no spaces) list to scope example: addscope *.example.com,*.google.com
setquery - setquery sets query to results of \"SELECT <column> FROM <tablename> WHERE <column> LIKE %<string>%\"
           usage: setquery <column> <tablename> <column> <string> (<string> can be a space and will select everything from column)
findsubdomains - run sublister on the set query
show - scope,domains or urls usage: show scope * will show everything in scope show scope google will show evrything with google in it
help - this screen
exit - close BBF
'''
print use

dbfile = config.DATABASE_FILE

def queryset(column,table,column2,string):
    return dbs.selectwhere(column,table,column2,string)

def addscope(scope):
        for domain in scope:
            if '*' not in domain:
                dbs.insert('domains',[domain])
            dbs.insert('scope',[domain])
    
while True:
    dbs = DbsMgr(dbfile)
    sublister = Sublist()
    
    ACTION = raw_input('\nBBF> ').split(' ')
    
    if ACTION[0] == 'addscope':
        addscope(ACTION[1].split(","))

            
    if ACTION[0] == 'setdb':
        dbfile = ACTION[1]
        print 'db file set to: '+dbfile

    if ACTION[0] == 'dirb':
        dirb().run(query)

    if ACTION[0] == 'findsubdomains':
        sublister.run(query)
        
    if ACTION[0] == 'show':
        for result in query:
            print '\t'+result
#####BURP ADD TEST#####
    if ACTION[0] == 'burp':
       proxies = {
                  'http': 'http://127.0.0.1:8080',
                  'https': 'http://127.0.0.1:8080'
                  }
       for d in query:
           requests.get('https://'+d, proxies=proxies, verify=False)
       
##########
        
            
    if ACTION[0] == 'setquery':
        if len(ACTION) == 4:
            query = queryset(ACTION[1],ACTION[2],ACTION[3],'')
            print 'query set to: SELECT '+ACTION[1]+' FROM '+ACTION[2]+'\n'
            
        elif len(ACTION) == 5:
            query = queryset(ACTION[1],ACTION[2],ACTION[3],ACTION[4])
            print 'query set to: SELECT '+ACTION[1]+' FROM '+ACTION[2]+' WHERE '+ACTION[3]+'=*'+ACTION[4]+'*\n'

        else:
            print 'query unchanged\n'

    if ACTION[0] == 'help':
        print use
        
    if ACTION[0] == 'exit':
        break
