from dbsMgr import DbsMgr
import requests
from time import sleep
import config
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

class Domains():
    def __init__(self,domainsToCheck):
        ##config variable define in main when done
        self.dbs = DbsMgr(config.DATABASE_FILE)
        self.domainsToCheck = domainsToCheck
        self.alldomains = self.dbs.select(['domain'],'domains')
        self.count = 0
        self.newSubDomains = []
        self.diasbleSSL = requests.packages.urllib3.disable_warnings()
        
#
#verify each domain making sure it returns anything but a 404 or error.
#called by threads of Verifydomains().
#
    def request(self,domain):
        try:
            r = requests.get('http://'+domain,verify=False,timeout=10)
            if r.status_code != 404:
                self.newSubDomains.append(domain)
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
        futures = [tpool.submit(self.request,domain) for domain in domainset]
	print '[+]Verifying subdomains...'
	tpool.shutdown(True)


        if self.newSubDomains:
            num = len(self.newSubDomains)
            print '[+]added following new domains:'
            for domain in self.newSubDomains:
                self.dbs.insert('domains',[domain])
                print domain
            print '[+]Added '+str(num)+' domains to database'
                
        if not self.newSubDomains:
            print '[-]No new subdomains found'
