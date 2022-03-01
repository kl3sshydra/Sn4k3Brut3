from bs4 import BeautifulSoup
import requests
from colorama import *
import argparse
import datetime
import threading
import requests
import urllib3
import time
urllib3.disable_warnings()
init(autoreset=True)

version = "1.0"
author = "kl3sshydra"

parser = argparse.ArgumentParser(description=f'Recursive directory bruter by {author} v{version}')
parser.add_argument('-u','--url', help='Your url', required=False)
parser.add_argument('-w','--wordlist', help='Your wordlist', required=False)
parser.add_argument('-v','--verbosity', help='Verbosity [y/n]', required=False)
parser.add_argument('-i','--interactive', help='Interactive mode [y/n]', required=True)
parser.add_argument('-rcs','--recursive', help='Recursive mode [y/n]', required=False)
parser.add_argument('-rs','--responsesize', help='Filter by response size', required=False)
parser.add_argument('-rw','--responsewords', help='Filter by response word counter', required=False)
parser.add_argument('-rc','--responsecode', help='Filter by response status code', required=False)
parser.add_argument('-log','--logfile', help='Log file', required=False)
parser.add_argument('-tm','--timeout', help='Requests timeout (seconds)', required=False)
parser.add_argument('-th','--threads', help='Number of threads', required=False)
args = vars(parser.parse_args())


class snakebrute:
    def listFD(self, url):
        page = requests.get(url, verify=False, timeout=int(args['timeout'])).text
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
{Style.BRIGHT}{Fore.RED}FILTERCODE {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['responsecode'].upper()}'
{Style.BRIGHT}{Fore.RED}INTERACTIVE {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['interactive'].upper()}'
{Style.BRIGHT}{Fore.RED}RECURSIVE {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['recursive'].upper()}'
{Style.BRIGHT}{Fore.RED}THREADS {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['threads'].upper()}'
{Style.BRIGHT}{Fore.RED}TIMEOUT {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['timeout'].upper()}'
{Style.BRIGHT}{Fore.RED}LOGFILE {Fore.WHITE}-> {Style.RESET_ALL}{Fore.BLUE}'{args['logfile']}'
""")
        wrdlist = str(args['wordlist'])
        url = args['url']
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
                threadsnumber = int(args['threads'])
                linenumber = 0
                for x in open(wrdlist,'r').readlines():
                    linenumber += 1
                linesperthread = int(linenumber/threadsnumber)
                snakebrute.printverboseinfo(f"Starting in 3 seconds with {str(threadsnumber)} threads of {str(linesperthread)} lines each", vanish=False)
                time.sleep(3)
                fp = open(wrdlist)
                linecounter = 0
                for i, line in enumerate(fp):
                    line = line.strip()
                    linecounter += 1
                    if linecounter > linesperthread:
                        linecounter = 0
                    else:
                        threading.Thread(target=snakebrute.getrequest, args=(url+"/"+line,)).start()
                fp.close()
                

    def getrequest(self, completeurl):
        snakebrute.printverboseinfo(f"Trying to get {completeurl}", vanish=True)
        try:
            r = requests.get(completeurl, verify=False, timeout=int(args['timeout']))
            responsesize = str(len(r.content))
            numberofwords = str(len(r.text.split(" ")))
            if r.status_code != 404:
               
               sizecolor = Fore.WHITE
               wordcolor = Fore.WHITE
               codecolor = Fore.WHITE

               if args['responsesize'] != 'n':
                   if args['responsesize'] == responsesize:
                       sizecolor = Fore.RED
                
               if args['responsewords'] != 'n':
                   if args['responsewords'] == numberofwords:
                       wordcolor = Fore.RED

               if args['responsecode'] != 'n':
                   if args['responsecode'] == str(r.status_code):
                       codecolor = Fore.RED

               snakebrute.printinfo(f"{completeurl} : status code {codecolor}{str(r.status_code)}{Fore.WHITE} : size {sizecolor}{responsesize}{Fore.WHITE} : words {wordcolor}{numberofwords}{Fore.WHITE}")
               if args['recursive'].lower() == "y":
                   threading.Thread(target=snakebrute.directorylisting, args=(completeurl,)).start()
        except:
            pass
    
    def printverboseinfo(self, text, vanish):
        if args['verbosity'].lower() == "y":
            if vanish == True:
                print(f"\n{Style.BRIGHT}{Fore.BLUE}[{Style.RESET_ALL}{Fore.RED}VERBOSE-{str(datetime.datetime.now().minute)}:{str(datetime.datetime.now().second)}{Style.BRIGHT}{Fore.BLUE}]{Style.BRIGHT}{Fore.WHITE} {text}", end='\r\x1b[2K')
            else:
                print(f"{Style.BRIGHT}{Fore.BLUE}[{Style.RESET_ALL}{Fore.WHITE}VERBOSE-{str(datetime.datetime.now().minute)}:{str(datetime.datetime.now().second)}{Style.BRIGHT}{Fore.BLUE}]{Style.BRIGHT}{Fore.WHITE} {text}")
            
    def printinfo(self, text):
        content = f"{Style.BRIGHT}{Fore.BLUE}[{Style.RESET_ALL}{Fore.WHITE}INFO-{str(datetime.datetime.now().minute)}:{str(datetime.datetime.now().second)}{Style.BRIGHT}{Fore.BLUE}]{Style.BRIGHT}{Fore.WHITE} {text}"
        if args['logfile'] != 'N':
            f = open(args['logfile'], 'a')
            f.write(content+"\n")
            f.close()
        print(content)

    def custominput(self, text):
        return input(f"{Style.BRIGHT}{Fore.RED}[{Style.RESET_ALL}{Fore.WHITE}INPUT{Style.BRIGHT}{Fore.RED}]{Style.BRIGHT}{Fore.BLUE} {text}: ")
        
    def directorylisting(self, url):
        filescounter = 0
        filelist = snakebrute.listFD(url)
        for file in filelist:
            if "/" in file or "." in file:
                filescounter += 1
        if filescounter != 0:
            print("\n")
            for file in filelist:
                if "/" in file or "." in file:
                    snakebrute.printinfo(f"{Style.BRIGHT}{Fore.RED}{url} {Style.RESET_ALL}{Fore.WHITE}directory index : {Style.BRIGHT}{Fore.BLUE}{file}")
                    if file.endswith("/") and file != "/":
                        completeurl = url+"/"+file
                        #print(completeurl)
                        threading.Thread(target=snakebrute.directorylisting, args=(completeurl,)).start()

    def main(self, mode):
        if mode == "interactive":
            snakebrute.printinfo("Started interactive mode")
            args['url'] = snakebrute.custominput("Insert url")
            args['wordlist'] = snakebrute.custominput("Insert wordlist path")
            args['verbosity'] = snakebrute.custominput("Insert verbosity [y/n]")
            args['recursive'] = snakebrute.custominput("Insert recursive [y/n]")
            args['responsesize'] = snakebrute.custominput("Insert filter size")
            args['responsewords'] = snakebrute.custominput("Insert response words")
            args['logfile'] = snakebrute.custominput("Insert log file")
            args['threads'] = snakebrute.custominput("Insert threads")
            args['timeout'] = snakebrute.custominput("Insert timeout")
        if args['verbosity'].lower() != "y":
            args['verbosity'] = "n"

        snakebrute.start()


snakebrute = snakebrute()
interactive = args['interactive'].lower()
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
    if args['timeout'] == None:
        args['timeout'] = "10"
    if args['responsecode'] == None:
        args['responsecode'] = "n"
    if args['recursive'] == None:
        args['recursive'] = 'n'
    if args['logfile'] == None:
        args['logfile'] = 'N'
    if args['threads'] == None:
        args['threads'] = '1'
    snakebrute.main("non-interactive")
else:
    snakebrute.main("interactive")
