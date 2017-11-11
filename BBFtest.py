from dbsMgr import DbsMgr
from sublist import Sublist
import sys
import requests
import config
import readline
from dirb import dirb
import socket
import os
import crlf

use = '''
Use config.py to configure tool settings.\n
COMMANDS:\n
setdb - choose or create the database file. usage: setdb <path to file>
addscope - add comma seperated(no spaces) list to scope (wildcards allowed). usage: addscope *.example.com,*.google.com
setquery - setquery sets query to results of \"SELECT <column> FROM <tablename> WHERE <column> LIKE %<string>%\"
           usage: setquery <column> <tablename> <column> [<string>] (<string> is optional)
show - shows the results of the current query.

findsubdomains - run sublister on the set query.
masscan - run masscan on set query.
dirb - run dirb on set query.
crlfscan - run a crlf injection test on set query.
burp - request all items in set query through a proxy 127.0.0.1:8080
help - this screen
exit - close BBF
'''
print use

def queryset(column,table,column2,string):
    return dbs.selectwhere(column,table,column2,string)

def addscope(scope):
        for domain in scope:
            if '*' not in domain:#if not domain startwith('*')
                dbs.insert('domains',[domain])
            dbs.insert('scope',[domain])
    
while True:

    ACTION = raw_input('\nBBF> ').split(' ')
    
    if ACTION[0] == 'addscope':
        addscope(ACTION[1].split(","))

            
    if ACTION[0] == 'setdb':
        dbfile = ACTION[1]
	dbs = DbsMgr(dbfile)
        print 'db file set to: '+dbfile

    if ACTION[0] == 'dirb':
        dirb().run(query)

    if ACTION[0] == 'findsubdomains':
	sublister = Sublist()
        sublister.run(query,dbfile)
        
    if ACTION[0] == 'show':
        for result in query:
            print result

    if ACTION[0] == 'burp':
       proxies = {
                  'http': 'http://127.0.0.1:8080',
                  'https': 'http://127.0.0.1:8080'
                  }
       for d in query:
	   if 'http' not in d:
           	requests.get('https://'+d, proxies=proxies, verify=False)
	   else:
		requests.get(d, proxies=proxies, verify=False)

    def resolveip(q):
	   ipList = []
	   for host in q:
		try:
			ipList.append(socket.gethostbyname(host))
		except:
			pass
	   return set(ipList)
    
    if ACTION[0] == 'masscan':
	   f = open('tmpip','w')
	   print '[+] Resolving domains and building IP list...'
	   for ip in resolveip(query):
		f.write(ip+'\n')
	   f.close()
		
	   os.system('masscan -p'+config.MASSCAN_PORTS+' -iL tmpip')
		

    if ACTION[0] == 'crlfscan':
	crlf.crlfscan(query)

            
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
