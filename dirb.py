import re
import subprocess
import config
from concurrent.futures import ThreadPoolExecutor,as_completed
from dbsMgr import dbsMgr
from handleUrl import HandleUrl

class dirb():
	def __init__(self):
		self.wordlist = config.FILE_LIST
		self.urls = []
		self.dbs = DbsMgr(config.DATABASE_FILE)
	#
	#start dirb
	#
	def start(self,domain):
		output = subprocess.check_output('dirb http://'+domain+' \"'+self.wordlist+'\" -S', shell=True)
		for i in re.findall(r'\+ (.*?) \(C',output):
			self.urls.append(i)
	#
	#run threads for dirb
	#
	def run(self,domains):
                print '[+]Running dirb with wordlist: '+config.FILE_LIST
		tpool = ThreadPoolExecutor(config.DIRB_THREADS)
		futures = [tpool.submit(self.start,d) for d in domains]
        #
        #wait for threads to finish up
        #
        tpool.shutdown(True)

        #
        #insert found urls into databse
        #TODO fix
        #
        print '[+]Adding following URLs to database:'
        source = 'dirb'
        for u in self.urls:
                print u
                self.dbs.insert('urls',[u,source])
        print '[+]Added '+str(len(self.urls))+' URLs to database.'
