=========================================================================== 

 ____        ____              _  _     _                     _          
|  _ \ _   _|  _ \  ___   __ _| || |   / \   _ __   __ _  ___| |__   ___ 
| |_) | | | | | | |/ _ \ / _` | || |_ / _ \ | '_ \ / _` |/ __| '_ \ / _ |
|  __/| |_| | |_| | (_) | (_| |__   _/ ___ \| |_) | (_| | (__| | | |  __/
|_|    \__, |____/ \___/ \__, |  |_|/_/   \_\ .__/ \__,_|\___|_| |_|\___|
       |___/             |___/              |_|                          

Apache web logs sneaker - by psy 

===========================================================================

###############################
# Project info
###############################

  Web: https://github.com/epsylon/pydog2apache [http://03c8.net]

###############################
# Summary
###############################

  PyDog4Apache is an Apache web logs sneaker.

  With this tool you can search for specific keywords (such as: government, police...) 
  on Whois description of the IPs of your website visitors by -automagically- analyzing 
  Apache logs provided (you can set folders of logs to manage all your projects).

  Also you can generate a report with results or send them to a list of email recipients.

###############################
# Installing
###############################

  PyDog4Apache runs on many platforms.  It requires Python (2.x.y) and the following libraries:

     python-pip - alternative Python package installer

  On Debian-based systems (ex: Ubuntu), run: 

     sudo apt-get install python-pip && sudo pip install ipwhois

  Source libs:

     * Pypi-ipwhois: https://pypi.python.org/pypi/ipwhois/

###############################
# HowTo
###############################

  Usage: pydog4apache.py [options]

  Options:
    --version      show program's version number and exit
    -h, --help     show this help message and exit
    -u, --update   check for latest stable version
    -v, --verbose  active verbose output

    *Reporting*:
      -r FILE      generate file output with 'visitants'
      -n EMAILS    notify via email (foo@email.net,bar@email.org,...)

###############################
# Usage
###############################

  Verbose:

    ./pydog4apache -v 

  Generate report file:

    ./pydog4apache -r my_visitants.txt

  Notify results via email to some recipients:

    ./pydog4apache -n='root@localhost,foo@email.org,bar@email.net'

  Combine options:

    ./pydog4apache -v -r my_visitants.txt -n epsylon@riseup.net

  Launch it as daemon (notify via email when finish):

    ./pydog4apache -n epsylon@riseup.net &

###############################
# Updating
###############################

  PyDog4Apache implements an option to update the tool to the latest stable version.

  This feature can be used only if you have cloned it from GitHub respository.

  To check your version you should launch:

    ./pydog4apache --update

  This will update the tool automatically removing all files from old package.

###############################
# Timelog
###############################

--------------------------
  11.04.2016 : v.0.1b
--------------------------

############
