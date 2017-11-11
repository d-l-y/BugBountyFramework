from dbsMgr import DbsMgr
import requests
import config
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import socket
from termcolor import colored

class Domains():
    def __init__(self,domainsToCheck,dbsfile):
        ##config variable define in main when done
        self.dbs = DbsMgr(dbsfile)
        self.domainsToCheck = domainsToCheck
        self.alldomains = self.dbs.select(['domain'],'domains')
        self.count = 0
        self.newSubDomains = []
        self.diasbleSSL = requests.packages.urllib3.disable_warnings()
	self.domainstrings = open(config.DOMAIN_STRINGS,'r').readlines()  
      


#
#verify each domain making sure it returns anything and does not error out.
#called by threads of Verifydomains().
#
    def request(self,domain):
        try:
            r = requests.get('http://'+domain,verify=False,timeout=10)
	    if r.status_code:
		self.newSubDomains.append(domain)
        except:
            pass

#
#try to resolve each subdomain to IP to verify it.
#

    def resolve(self,host):
	try:
            r = requests.get('http://'+host,verify=False,timeout=10)
	    if r.status_code:
		self.newSubDomains.append(domain)
        except:
	    try:	
	        line = '='*(40-len(host))
	        print colored(host,'blue')+' '+line+'=>  '+colored(socket.gethostbyname(host),'green')
	        self.newSubDomains.append(host)

	    except:
		pass


#
#start threads calling verify() on each domain in a set() of the difference
#between self.foundDomains and self.alldomains which is list of all domains
#currently in table domains.
#	

    def verify(self):
        tpool = ThreadPoolExecutor(config.REQUESTS_THREADS)
        domainset = self.domainsToCheck.difference(self.alldomains)
	print colored('[-]Resolving subdomains...','blue')
        futures = [tpool.submit(self.resolve,domain) for domain in domainset]
	tpool.shutdown(True)


        if self.newSubDomains:
            num = len(self.newSubDomains)
            for domain in self.newSubDomains:
                self.dbs.insert('domains',[domain])
            print colored('[+]Added '+str(num)+' domains to database','green')
                
        if not self.newSubDomains:
            print colored('[!]No new subdomains found','red')
