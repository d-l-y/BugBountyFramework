#!/usr/bin/env python
# coding: utf-8
# Sublist3r v1.0p (Plazmaz's Fork)
# By Ahmed Aboul-Ela - https://www.twitter.com/aboul3la
# Rewritten by Dylan Katz - https://www.twitter.com/Plazmaz

import argparse
# modules in standard library
import sys

# external modules
from scan_flags import ScanParams
# Python 2.x and 3.x compatiablity
from subscann3r import SubScann3r

# In case you cannot install some of the required development packages
# there's also an option to disable the SSL warning:
from util.util import Util
logger = Util.get_logger()

try:
    import requests.packages.urllib3

    requests.packages.urllib3.disable_warnings()
except:
    pass


def parser_error(errmsg):
    logger.banner()
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print(logger.R + "Error: " + errmsg + logger.W)
    sys.exit()


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumerate it's subdomains", required=True)
    parser.add_argument('-b', '--bruteforce', help='Enable the subbrute bruteforce module', nargs='?', default=False)
    parser.add_argument('-p', '--ports', help='Scan the found subdomains against specified tcp ports')
    parser.add_argument('-v', '--verbose', help='Enable Verbosity and display results in realtime', nargs='?',
                        default=False)
    parser.add_argument('-t', '--threads', help='Number of threads to use for subbrute bruteforce', type=int,
                        default=30)
    parser.add_argument('-to', '--takeover-scan', help='Scan for subdomain takeover issues', nargs='?', default=False)
    parser.add_argument('-e', '--engines', help='Specify a comma-separated list of search engines')
    parser.add_argument('-o', '--output', help='Save the results to text file')
    return parser.parse_args()


def main(domain, threads, savefile, ports, silent, verbose, enable_bruteforce, takeover_check, engines):
    logger.is_verbose = verbose
    options = ScanParams(silent=silent, verbose=verbose, brute_force=enable_bruteforce, takeover_check=takeover_check,
                         thread_count=threads, engines=engines, ports=ports, savefile=savefile)
    scanner = SubScann3r(domain, logger, options)
    return scanner.scan()


if __name__ == "__main__":
    args = parse_args()
    domain = args.domain
    threads = args.threads
    savefile = args.output
    ports = args.ports
    enable_bruteforce = args.bruteforce
    verbose = args.verbose
    engines = args.engines
    takeover_check = args.takeover_scan
    if verbose or verbose is None:
        verbose = True
    if takeover_check or takeover_check is None:
        takeover_check = True
    logger.banner()
    res = main(domain, threads, savefile, ports, silent=False, verbose=verbose, enable_bruteforce=enable_bruteforce,
               takeover_check=takeover_check, engines=engines)
