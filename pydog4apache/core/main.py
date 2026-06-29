#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
PyDog4Apache - 2016/2026 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyDog4Apache; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import os, traceback, sys, re, gzip, datetime, string, stat, json
from .options import PyDog4ApacheOptions
from .update import Updater

try:
    from ipwhois import IPWhois
except:
    print("\n[Warning] - Error importing: ipwhois lib. \n\n On Debian based systems:\n\n $ sudo apt-get install python3-pip && sudo pip3 install ipwhois\n")
    print("[Source] - Pypi-ipwhois: https://pypi.python.org/pypi/ipwhois/\n")
    sys.exit(2)

DEBUG = 0

class PyDog4Apache(object):
    def __init__(self):
        self.visitants = {} # visitants
        self.visitants_ips = set() # used to not repeat checks (per run)
        self.whois_cache = {} # persisted ip -> whois description (across runs)
        self.cache_file = 'whois_cache.json'
        self.analyzed_logs = [] # logs read on this run

    def set_options(self, options):
        self.options = options

    def create_options(self, args=None):
        self.optionParser = PyDog4ApacheOptions()
        self.options = self.optionParser.get_options(args)
        if not self.options:
            return False
        return self.options

    def banner(self):
        print('='*75, "\n")
        print(r" ____        ____              _  _     _                     _          ")
        print(r"|  _ \ _   _|  _ \  ___   __ _| || |   / \   _ __   __ _  ___| |__   ___ ")
        print(r"| |_) | | | | | | |/ _ \ / _` | || |_ / _ \ | '_ \ / _` |/ __| '_ \ / _ |")
        print(r"|  __/| |_| | |_| | (_) | (_| |__   _/ ___ \| |_) | (_| | (__| | | |  __/")
        print(r"|_|    \__, |____/ \___/ \__, |  |_|/_/   \_\ .__/ \__,_|\___|_| |_|\___|")
        print(r"       |___/             |___/              |_|                          ")
        print(self.optionParser.description, "\n")
        print('='*75)

    def try_running(self, func, error, args=None):
        options = self.options
        args = args or []
        try:
            return func(*args)
        except Exception as e:
            print((error, "error"))
            if DEBUG != 0:
                traceback.print_exc()

    def check_root(self): # check root permissions
        if not os.geteuid()==0:
            sys.exit("[Info] You need to launch it as root (ex: 'sudo python3 pydog4apache')...\n")

    def is_readable(self, folder): # check if logs are readable without root permissions
        try:
            st = os.stat(folder)
            root = st.st_uid
        except:
            root = None 
        return root

    def check_access(self, logs): # check if logs required root
        for folder in logs:
            root = self.is_readable(folder)
            if root == None: # wrong folder
                print("\n[Error] This source: [", folder, "] is not valid... [Passing!]")
            if root == 0: # root needed
                check_perms = self.try_running(self.check_root, "\n[Error] Internal error checking root permissions.")

    def extract_logs(self): # extract logs from folder (ex: 'sources.txt')
        try:
            f = open('sources.txt')
            logs = f.readlines()
            logs = [ log.replace('\n','') for log in logs ]
            f.close()
            if not logs:
                print("\n[Error] Imposible to retrieve 'sources' from file... [Aborting!]\n")
                return
            else:
                return logs
        except:
            if os.path.exists('sources.txt') == True:
                print('\n[Error] Cannot open:', 'sources.txt', "[Aborting!]\n")
                sys.exit(2)
            else:
                print('\n[Error] Cannot found:', 'sources.txt', "[Aborting!]\n")
                sys.exit(2)

    def load_cache(self): # load persisted whois results (avoid re-querying known IPs)
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file) as f:
                    self.whois_cache = json.load(f)
        except:
            self.whois_cache = {}

    def save_cache(self): # persist whois results atomically
        try:
            tmp = self.cache_file + '.tmp'
            with open(tmp, 'w') as f:
                json.dump(self.whois_cache, f)
            os.replace(tmp, self.cache_file)
        except:
            pass

    def extract_whois(self, ip): # extract whois description ("" = no descr, None = lookup failed)
        try:
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip): # only IPs
                w = IPWhois(ip, timeout=5) # timeout 5
                res = w.lookup_whois(retry_count=2) # legacy whois / retries 2
                descr = res["nets"][0]['description']
                if descr is None:
                    descr = ""
            else:
                descr = ""
        except:
            descr = None
        return descr

    def is_valid_ip(self, ip): # extract visitors IP / perform whois
        if not ip or not ip[0].isdigit(): # parse only if IP starts with a number
            return
        if (re.match(r'^127\.', ip) or re.match(r'^10\.', ip) or re.match(r'^192\.168\.', ip) or re.match(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.', ip) or ip.startswith('localhost')): # skip LAN / localhost
            return
        if ip in self.visitants_ips: # do not repeat IPs on this run
            return
        self.visitants_ips.add(ip)
        return True

    def check_visitants(self, descr): # check visitors list
        try:
            for v in self.keys:
                v = v.rstrip()
                if v.lower() in descr.lower(): # visitant found!
                    key = v.lower()
                    return key
                else:
                    pass
        except:
            if os.path.exists('keywords.txt') == True:
                return
            else:
                print('\n[Error] Cannot found:', 'keywords.txt', "[Aborting!]\n")
                return

    def run(self, opts=None):
        if opts:
            options = self.create_options(opts)
            self.set_options(options)
        options = self.options
        self.banner()
        if options.update: # auto-update tool
            print("\n[Info] Trying to update automatically to the latest stable version...\n")
            Updater()
            sys.exit()
        print("\n[Info] Sending 'dogs' to sniff 'logs'... [Waiting!]")
        if self.options.verbose:
            print("\n"+"="*40+"\n")
        logs = self.try_running(self.extract_logs, "\nInternal error extracting logs.")
        access = self.check_access(logs)
        f = open('keywords.txt')
        self.keys = f.readlines()
        f.close()
        if not self.keys:
            print("\n[Error] Imposible to retrieve 'visitants' from file... [Aborting!]\n")
            return
        if self.options.flush: # forget known IPs -> re-query whois of all of them
            try:
                if os.path.exists(self.cache_file):
                    os.remove(self.cache_file)
                    print("\n[Info] WHOIS cache flushed... [Re-querying all IPs!]")
            except:
                print("\n[Error] Cannot flush WHOIS cache:", self.cache_file, "[Passing!]")
        self.load_cache() # reuse known whois results, only query new IPs
        for folder in logs:
            if not folder.endswith('/'):
                folder = folder + "/"
            try:
                listing = os.listdir(folder)
            except:
                continue
            sep = '-'
            sep2= '['
            for log in listing:
                path = folder + log
                if self.options.verbose:
                    print("[Info] Analyzing:", path)
                self.analyzed_logs.append(path)
                try:
                    if log.endswith('.gz'): # also read on compressed logs
                        f = gzip.open(path, 'rt', errors='replace')
                    else:
                        f = open(path, errors='replace')
                except:
                    continue
                try:
                    for record in f: # stream line by line (do not load whole file)
                        ip = record.split(sep, 1)[0]
                        ip = ''.join(ip.split())
                        if self.is_valid_ip(ip) is not True:
                            continue
                        if self.options.verbose:
                            print("    |-> IP Found:", ip)
                        date_visit = ""
                        date = [record.split(']')[0] for p in record.split('[') if ']' in p]
                        for d in date:
                            date_visit = d.split(sep2, 1)[1]
                        if ip in self.whois_cache: # cached -> no whois query
                            descr = self.whois_cache[ip]
                        else: # new IP -> query whois and cache the result
                            descr = self.extract_whois(ip)
                            if descr is not None: # do not cache failed lookups (retry next run)
                                self.whois_cache[ip] = descr
                        if descr:
                            if self.options.verbose:
                                print("    |-> WHOIS Description:", descr)
                            key = self.check_visitants(descr)
                            if key:
                                self.visitants[str(ip)] = "[ " + str(key.upper()) + " ]" + " | " + str(str(descr) + " | " + str(date_visit) + " | " + str(path))
                finally:
                    f.close()
        self.save_cache() # persist whois results for next run (cron)
        print("\n"+"="*40+"\n")
        if self.options.file: # export results to file
            namefile = str(self.options.file)
            self.report = open(namefile, 'w')
            self.report.write("# Apache web logs sneaker - 2016/2026 - by psy (https://03c8.net)\n")
            self.report.write("# Project: https://code.03c8.net/epsylon/pydog4apache\n")
            self.report.write("# Reported at: " + str(datetime.datetime.now()) + "\n\n")
            self.report.write("Logs Analyzed:\n\n")
            for log in self.analyzed_logs:
                self.report.write(" -"+log+"\n")
            self.report.write("\nResults:\n\n")
        for key,val in list(self.visitants.items()):
            print(("{} -> {}".format(key, val))+"\n")
            if self.options.file:
                self.report.write(key + " -> " + val + "\n")
        if not list(self.visitants.items()):
            print("[Info] Not any 'keyword' found on your 'visitants'... [Exiting!]\n")
            if self.options.file:
                self.report.write(" -Not any 'keyword' found on your 'visitants'...\n")
        if self.options.file: # close file containter
            self.report.close()
        if self.options.emails: # send results via email
            print("-"*22+"\n")
            import smtplib, socket
            from email.mime.text import MIMEText
            self.notify = open('tempmail', 'w')
            self.notify.write("# Apache web logs sneaker - 2016/2026 - by psy (https://03c8.net)\n")
            self.notify.write("# Project: https://code.03c8.net/epsylon/pydog4apache\n")
            self.notify.write("# Reported at: " + str(datetime.datetime.now()) + "\n\n")
            self.notify.write("Logs Analyzed:\n\n")
            for log in self.analyzed_logs:
                self.notify.write(" -"+log+"\n")
            self.notify.write("\nResults:\n\n")
            for key,val in list(self.visitants.items()):
                self.notify.write(key + " -> " + val + "\n")
            if not list(self.visitants.items()):
                self.notify.write("Not any 'keyword' found on your 'visitants'...\n")
            self.notify.close()
            self.notify = open('tempmail', 'rb')
            msg = MIMEText(self.notify.read().decode('utf-8'))
            self.notify.close()
            doggy = 'pydog4apache@'+str(socket.gethostname())
            herd = self.options.emails
            herd = herd.split(',')
            msg['Subject'] = '[pydog4apache] You have interesting visitants...'
            msg['From'] = doggy
            msg['To'] = ", ".join(herd)
            msg.preamble = 'You have a report with visitants...'
            try:
                s = smtplib.SMTP('localhost')
                s.sendmail(doggy, herd, msg.as_string())
                s.quit()
            except:
                print("[Error] Not any SMTP (email) server running on: '"+str(socket.gethostname())+"'... [Passing!]\n")
            os.remove('tempmail') # remove temporal email container

if __name__ == "__main__":
    app = PyDog4Apache()
    options = app.create_options()
    if options:
        app.set_options(options)
        app.run()
