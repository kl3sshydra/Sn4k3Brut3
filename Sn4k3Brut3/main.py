from bs4 import BeautifulSoup
import requests
from colorama import *
import argparse
import datetime
import requests
import sys
import urllib3
import os
urllib3.disable_warnings()
init(autoreset=True)

version = "1.0"
author = "kl3sshydra"

parser = argparse.ArgumentParser(description=f'Recursive directory bruter by {author} v{version}')
parser.add_argument('-u','--url', help='Your url', required=False)
parser.add_argument('-w','--wordlist', help='Your wordlist', required=False)
parser.add_argument('-v','--verbosity', help='Verbosity [y/n]', required=False)
parser.add_argument('-i','--interactive', help='Interactive mode [y/n]', required=True)
parser.add_argument('-rs','--responsesize', help='Filter by response size', required=False)
parser.add_argument('-rw','--responsewords', help='Filter by response word counter', required=False)
parser.add_argument('-th','--threads', help='Number of threads', required=True)
args = vars(parser.parse_args())

class snakebrute:
    def listFD(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        return [node.get('href') for node in soup.find_all('a') if node.get('href')]

    def start(self):
        print(f"""{Fore.BLUE}
.d8888. d8b   db   j88D  db   dD d8888b. d8888b. d8888b. db    db d888888b d8888b. 
88'  YP 888o  88  j8~88  88 ,8P' VP  `8D 88  `8D 88  `8D 88    88 `~~88~~' VP  `8D 
`8bo.   88V8o 88 j8' 88  88,8P     oooY' 88oooY' 88oobY' 88    88    88      oooY' 
  `Y8b. 88 V8o88 V88888D 88`8b {Style.BRIGHT}{Fore.RED}{version}{Style.RESET_ALL}{Fore.BLUE} ~~~b. 88~~~b. 88`8b   88{Style.BRIGHT}{Fore.RED} by {Style.RESET_ALL}{Fore.BLUE}88    88      ~~~b. {Style.BRIGHT}{Fore.RED}{author}{Fore.BLUE}
{Fore.WHITE}db   8D 88  V888     88  88 `88. db   8D 88   8D 88 `88. 88b  d88    88    db   8D 
`8888Y' VP   V8P     VP  YP   YD Y8888P' Y8888P' 88   YD ~Y8888P'    YP    Y8888P' 

{Style.BRIGHT}{Fore.RED}URL {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['url']}'
{Style.BRIGHT}{Fore.RED}WORDLIST {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['wordlist']}'
{Style.BRIGHT}{Fore.RED}VERBOSITY {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['verbosity'].upper()}'
{Style.BRIGHT}{Fore.RED}FILTERSIZE {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['responsesize'].upper()}'
{Style.BRIGHT}{Fore.RED}FILTERWORDS {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['responsewords'].upper()}'
{Style.BRIGHT}{Fore.RED}THREADS {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['threads'].upper()}'
""")
        if args['verbosity'] == None or args['wordlist'] == None or args['url'] == None:
            snakebrute.printinfo("Missing some required arguments, quitting")
            exit()
        else:
            snakebrute.printinfo("Starting...")
            if args['threads'] == '1':
                for line in open(args['wordlist'], 'r'):
                    line = line.strip()
                    snakebrute.getrequest(url+"/"+line)
            else:
                snakebrute.printinfo("Single threading is disabled. Please wait while i load the wordlist")
                try:
                    os.remove("temp")
                except:
                    pass
                try:
                    os.mkdir("temp")
                except FileExistsError:
                    pass
                    

    def getrequest(self, completeurl):
        if args['verbosity'].lower() == "y":
            snakebrute.printverboseinfo(f"Trying to get {completeurl}")
        r = requests.get(completeurl, verify=False)
        if r.status_code != 404:
            snakebrute.printinfo(f"{completeurl} : status code {str(r.status_code)}")

    def printverboseinfo(self, text):
        sys.stdout.write("\033[K")
        print(f"{Style.BRIGHT}{Fore.BLUE}[{Style.RESET_ALL}{Fore.WHITE}VERBOSE-{str(datetime.datetime.now().minute)}:{str(datetime.datetime.now().second)}{Style.BRIGHT}{Fore.BLUE}]{Style.BRIGHT}{Fore.WHITE} {text}")
        sys.stdout.write("\033[F")
        
    def printinfo(self, text):
        print(f"{Style.BRIGHT}{Fore.BLUE}[{Style.RESET_ALL}{Fore.WHITE}INFO-{str(datetime.datetime.now().minute)}:{str(datetime.datetime.now().second)}{Style.BRIGHT}{Fore.BLUE}]{Style.BRIGHT}{Fore.WHITE} {text}")

    def custominput(self, text):
        return input(f"{Style.BRIGHT}{Fore.RED}[{Style.RESET_ALL}{Fore.WHITE}INPUT{Style.BRIGHT}{Fore.RED}]{Style.BRIGHT}{Fore.BLUE} {text}: ")
        
    def directorylisting(self):
        for file in snakebrute.listFD(url):
            if "/" in file or "." in file:
                print(file)

    def main(self, mode):
        if mode == "interactive":
            snakebrute.printinfo("Started interactive mode")
            args['url'] = snakebrute.custominput("Insert url")
            args['wordlist'] = snakebrute.custominput("Insert wordlist path")
            args['verbosity'] = snakebrute.custominput("Insert verbosity [y/n]")
        if args['verbosity'].lower() != "y":
            args['verbosity'] = "n"

        snakebrute.start()


snakebrute = snakebrute()
interactive = "n"
try:
    if args['interactive'].lower() == "y":
        interactive = "y"
except:
    pass
if interactive == "n":
    url = args['url']
    wordlist = args['wordlist']
    verbosity = "n"
    if args['verbosity'] == None:
        args['verbosity'] = "n"
    try:
        if args['verbosity'].lower() == "y":
            verbosity = "y"
    except:
        pass

    if args['responsesize'] == None:
        args['responsesize'] = "n"
    responsesize = "n"
    try:
        if args['responsesize'].lower() == "y":
            responsesize = "y"
    except:
        pass

    if args['responsewords'] == None:
        args['responsewords'] = "n"
    responsewords = "n"
    try:
        if args['responsewords'].lower() == "y":
            responsewords = "y"
    except:
        pass
    snakebrute.main("non-interactive")
else:
    snakebrute.main("interactive")
