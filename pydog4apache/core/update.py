#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
PyDog4Apache - 2016/2022 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyDog4Apache; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import os
from subprocess import PIPE
from subprocess import Popen as execute
        
class Updater(object):     
    def __init__(self):
        GIT_REPOSITORY = "https://code.03c8.net/epsylon/pydog4apache"
        GIT_REPOSITORY2 = "https://github.com/epsylon/pydog4apache"
        rootDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', ''))
        if not os.path.exists(os.path.join(rootDir, ".git")):
            print("-"*22)
            print("\n[Info] Not any .git repository found!")
            print("\nTo have working this feature, you should clone pydgo4apache with:\n")
            print("$ git clone %s" % GIT_REPOSITORY)
            print("\nAlso you can try this other mirror:\n")
            print("$ git clone %s" % GIT_REPOSITORY2 + "\n")
        else:
            checkout = execute("git checkout . && git pull", shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
            print(checkout)
            if not "Already up-to-date" in checkout:
                print("Congratulations!! pydog4apache has been updated... ;-)\n")
            else:
                print("Your pydog4apache doesn't need to be updated... ;-)\n")
