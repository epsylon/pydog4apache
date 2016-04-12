#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PyDog4Apache - 2015 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyDog4Apache; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
from options import PyDog4ApacheOptions
from update import Updater
import os, traceback, sys, re, gzip, datetime, string, stat

try:
    from ipwhois import IPWhois
except:
    print "\n[Warning] - Error importing: ipwhois lib. \n\n On Debian based systems:\n\n $ sudo apt-get install python-pip && sudo pip install ipwhois\n"
    print "[Source] - Pypi-ipwhois: https://pypi.python.org/pypi/ipwhois/\n"
    sys.exit(2)

DEBUG = 0

class PyDog4Apache(object):
    def __init__(self):
        self.visitants = {} # visitants
        self.visitants_ips = [] # used to not repeat checks

    def set_options(self, options):
        self.options = options

    def create_options(self, args=None):
        self.optionParser = PyDog4ApacheOptions()
        self.options = self.optionParser.get_options(args)
        if not self.options:
            return False
        return self.options

    def banner(self):
        print '='*75, "\n"
        print " ____        ____              _  _     _                     _          "
        print "|  _ \ _   _|  _ \  ___   __ _| || |   / \   _ __   __ _  ___| |__   ___ "
        print "| |_) | | | | | | |/ _ \ / _` | || |_ / _ \ | '_ \ / _` |/ __| '_ \ / _ |"
        print "|  __/| |_| | |_| | (_) | (_| |__   _/ ___ \| |_) | (_| | (__| | | |  __/"
        print "|_|    \__, |____/ \___/ \__, |  |_|/_/   \_\ .__/ \__,_|\___|_| |_|\___|"
        print "       |___/             |___/              |_|                          "
        print self.optionParser.description, "\n"
        print '='*75

    def try_running(self, func, error, args=None):
        options = self.options
        args = args or []
        try:
            return func(*args)
        except Exception as e:
            print(error, "error")
            if DEBUG:
                traceback.print_exc()

    def check_root(self): # check root permissions
        if not os.geteuid()==0:
            print "[Error] - Some of your 'sources' need more rights to be accessed."
            sys.exit("\n[Info] - Try to launch it as root (ex: 'sudo ./pydog4apache')\n")

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
                print "[Error] - This source:", folder, "is not valid!. Passing..."
            if root is 0: # root needed
                check_perms = self.try_running(self.check_root, "\nInternal error checking root permissions.")

    def extract_logs(self): # extract logs from folder (ex: 'sources.txt')
        try:
            f = open('sources.txt')
            logs = f.readlines()
            logs = [ log.replace('\n','') for log in logs ]
            f.close()
            if not logs:
                print "\n[Error] - Imposible to retrieve 'sources' from file.\n"
                return
            else:
                return logs
        except:
            if os.path.exists('sources.txt') == True:
                print '\n[Error] - Cannot open:', 'sources.txt', "\n"
                sys.exit(2)
            else:
                print '\n[Error] - Cannot found:', 'sources.txt', "\n"
                sys.exit(2)

    def extract_whois(self, ip): # extract whois description
        try:
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip): # only IPs
                w = IPWhois(ip, timeout=5) # timeout 5
                res = w.lookup_whois(retry_count=2) # legacy whois / retries 2
                descr = res["nets"][0]['description']
                if self.options.verbose:
                    print"[Verbose] - Resolving:", ip
            else:
                descr = None
        except:
            descr = None
        return descr

    def is_valid_ip(self, ip): # extract visitors IP / perform whois
        if not re.match(r'^127\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) or re.match(r'^10\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) or re.match(r'^192.168\.\d{1,3}\.\d{1,3}', ip) or re.match(r'^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}', ip) or ip.startswith('localhost'): # non LAN IP
            if ip not in self.visitants_ips: # create a list with non repeated IPs
                if ip[0].isdigit(): # parse if IP starts with a number
                    self.visitants_ips.append(ip)
                    ip_found = True
                    return ip_found

    def check_visitants(self, descr): # check visitors list
        try:
            for v in self.keys:
                if v.lower() in descr.lower(): # visitant found!
                    key = v.lower()
                    return key
                else:
                    pass
        except:
            if os.path.exists('keywords.txt') == True:
                return
            else:
                print '\n[Error] - Cannot found:', 'keywords.txt', "\n"
                return

    def run(self, opts=None):
        if opts:
            options = self.create_options(opts)
            self.set_options(options)
        options = self.options
        self.banner()
        if options.update:
            try:
                print("\n[Info] - Trying to update automatically to the latest stable version.\n")
                Updater()
            except:
                print("\nSomething was wrong!. You should clone PyDog2Apache manually with:\n")
                print("$ git clone https://github.com/epsylon/pydog2apache\n")
            sys.exit(2)
        print "\n[Info] - Sending dogs to sniff logs... Please wait!\n"
        print "-"*22
        logs = self.try_running(self.extract_logs, "\nInternal error extracting logs.")
        access = self.check_access(logs)
        f = open('keywords.txt')
        self.keys = f.readlines()
        self.keys = [ self.key.replace('\n','') for self.key in self.keys ]
        f.close()
        if not self.keys:
            print "\n[Error] - Imposible to retrieve 'visitants' from file.\n"
            return
        for folder in logs:
            if not folder.endswith('/'):
                folder = folder + "/"
            try:
                listing = os.listdir(folder)
                for log in listing:
                    if self.options.verbose:
                        print "[Verbose] - Analyzing:", folder+log
                    if log.endswith('.gz'): # also read on compressed logs
                        with gzip.open(folder+log, 'rb') as f:
                            dog_sniff = f.readlines()
                    else:
                        try:
                            f = open(folder+log)
                        except:
                            return
                        dog_sniff = f.readlines()
                    sep = '-'
                    sep2= '['
                    for record in dog_sniff:
                        ip = record.split(sep, 1)[0]
                        ip = ''.join(ip.split())
                        ip_found = self.is_valid_ip(ip)
                        if ip_found is True: # extract info
                            date = [record.split(']')[0] for p in record.split('[') if ']' in p]
                            for d in date:
                                date_visit = d.split(sep2, 1)[1]
                            descr = self.extract_whois(ip)
                            if descr is not None:
                                key = self.check_visitants(descr)
                                if key:
                                    self.visitants[str(ip)] = "[" + str(key.upper()) + "]" + "|" + str(str(descr) + "|" + str(date_visit) + "|" + str(folder+log))
                    f.close()
            except:
                pass
        if self.options.verbose:
            print "-"*22
        if self.options.file: # export results to file
            namefile = str(self.options.file)
            self.report = open(namefile, 'w')
            self.report.write("# Apache web logs sneaker - GPLv3 - by psy\n")
            self.report.write("# Project: https://github.com/epsylon/pydog4apache - 03c8.net\n")
            self.report.write("# Reported at: " + str(datetime.datetime.now()) + "\n\n")
        for key,val in self.visitants.items():
            print("{} -> {}".format(key, val))
            print "-"*12
            if self.options.file: 
                self.report.write(key + " -> " + val + "\n")
                self.report.write("-"*12 + "\n")
        if not self.visitants.items():
            print "[Info] - Not any 'keyword' found on your 'visitants'.\n"
            if self.options.file:
                self.report.write("Not any 'keyword' found on your 'visitants'.\n")
        if self.options.file: # close file containter
            self.report.close()
        if self.options.emails: # send results via email
            import smtplib, socket
            from email.mime.text import MIMEText
            self.notify = open('tempmail', 'w')
            self.notify.write("# Apache web logs sneaker - GPLv3 - by psy\n")
            self.notify.write("# Project: https://github.com/epsylon/pydog4apache - 03c8.net\n")
            self.notify.write("# Reported at: " + str(datetime.datetime.now()) + "\n\n")
            for key,val in self.visitants.items():
                self.notify.write(key + " -> " + val + "\n")
                self.notify.write("-"*12 + "\n")
            if not self.visitants.items():
                self.notify.write("Not any 'keyword' found on your 'visitants'.\n")
            self.notify.close()
            self.notify = open('tempmail', 'rb')
            msg = MIMEText(self.notify.read())
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
                print "[Error] - Not any SMTP server running on: '"+str(socket.gethostname())+"'. Aborting email report...\n"
            os.remove('tempmail') # remove temporal email container

if __name__ == "__main__":
    app = PyDog4Apache()
    options = app.create_options()
    if options:
        app.set_options(options)
        app.run()
