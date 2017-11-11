import re
import subprocess
import config
from concurrent.futures import ThreadPoolExecutor,as_completed
from dbsMgr import DbsMgr
from termcolor import colored

class dirb():
	def __init__(self):
		self.wordlist = config.FILE_LIST
		self.urls = []
		self.dbs = DbsMgr(config.DATABASE_FILE)
	#
	#start dirb
	#
	def start(self,domain):

		print colored('[-] Testing '+domain,'blue')
#
#try all options if http fails try https if that fails try "fine tune" https
#
		output = subprocess.check_output('dirb http://'+domain+' \"'+self.wordlist+'\" -S -a config.USER_AGENT_STRING', shell=True)
		if re.findall(r'[not stable]', output):
			output = subprocess.check_output('dirb https://'+domain+' \"'+self.wordlist+'\" -S -a config.USER_AGENT_STRING', shell=True)
			if re.findall(r'[not stable]', output):
				output = subprocess.check_output('dirb https://'+domain+' \"'+self.wordlist+'\" -f -S -a config.USER_AGENT_STRING', shell=True)
		if re.findall(r'[FATAL]', output):
			print colored('[!] FATAL error connecting to '+domain,'red')
		for i in re.findall(r'\+ (.*?)\n',output):
			print colored('[+] Found: '+i,'green')
			for u in re.findall(r'^(.*?) (C',i):
				self.urls.append(unicode(u))
	#
	#run threads for dirb
	#
	def run(self,domains):
                print colored('[-]Running dirb with wordlist: '+config.FILE_LIST,'blue')
		tpool = ThreadPoolExecutor(config.DIRB_THREADS)
		futures = [tpool.submit(self.start,d) for d in domains]
		#
		#wait for threads to finish up
		#
		tpool.shutdown(True)

		#
		#insert found urls into database
		#

		if self.urls:
			source = 'dirb'
			print colored('[-]Adding following URLs to database:','blue')
			for u in self.urls:
				self.dbs.insert('urls',[u,source,'NULL'])
				print u
			print colored('[+]Added '+str(len(self.urls))+' URLs to database.','green')
		if not self.urls:
			print colored('[!]No directories found','red')
