import sublist3r
from Domain import Domains

class Sublist():
    '''Handle running sublist3r on list of domains and pass discovered domains
        into Domains.verify().
    '''

#
#initialize variables for sublist3r
#
    def __init__(self):
        self.no_threads = 40
        self.savefile = False
        self.ports = None
        self.silent = True
        self.verbose = False
        self.enable_bruteforce = False
        self.engines = None
        self.foundDomains = []

#
#run sublist3r on each domain and append found subdomains to self.foundDomains
#cast foundDomains as set() call Domains.verify()
#
    def run(self,domains):
        if domains:
            scopelist = []
            nonwild = []
            for domain in domains:
                if '*' in domain:
                    scopelist.append(domain.strip('*.'))
            for domain in scopelist:
                print '[+]Currently Running sublist3r on: '+domain
                subdomains = sublist3r.main(domain, self.no_threads, self.savefile,
                                    self.ports, self.silent, self.verbose, self.enable_bruteforce,
                                    self.engines)
                self.foundDomains += subdomains
            self.foundDomains = set(self.foundDomains)
            Domains(self.foundDomains).verify()
