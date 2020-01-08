=========================================================================== 

 ____        ____              _  _     _                     _          
|  _ \ _   _|  _ \  ___   __ _| || |   / \   _ __   __ _  ___| |__   ___ 
| |_) | | | | | | |/ _ \ / _` | || |_ / _ \ | '_ \ / _` |/ __| '_ \ / _ |
|  __/| |_| | |_| | (_) | (_| |__   _/ ___ \| |_) | (_| | (__| | | |  __/
|_|    \__, |____/ \___/ \__, |  |_|/_/   \_\ .__/ \__,_|\___|_| |_|\___|
       |___/             |___/              |_|                          

Apache web logs sneaker - 2016/2020 - by psy 

===========================================================================

###############################
# Project info
###############################

  Web: https://pydog4apache.03c8.net/ [https://03c8.net]

###############################
# Summary
###############################

  PyDog4Apache is an Apache web logs sneaker.

  With this tool you can search for specific keywords (such as: government, police...) 
  on Whois description of the IPs of your website visitors by -automagically- analyzing 
  Apache logs provided (you can set folders of logs to manage all your projects).

  Also you can generate a report with results or send them to a list of email recipients
  like an alert.

###############################
# Installing
###############################

  PyDog4Apache runs on many platforms. It requires Python (3.x.y) and the following libraries:

      python3-pip - Python package installer
      ipwhois (0.10.3)  - Retrieve and parse whois data for IPv4 and IPv6 addresses.

  On Debian-based systems (ex: Ubuntu), run: 

      sudo apt-get install python3-pip && pip3 install ipwhois==0.10.3 --user

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
# Examples
###############################

  Verbose:

    python3 pydog4apache -v

  Generate report file:

    python3 pydog4apache -r 'visitants.txt'

  Notify results via email to some recipients:

    python3 pydog4apache -n='root@localhost,foo@email.org,bar@email.net'

  Combine options:

    python3 pydog4apache -v -r 'visitants.txt' -n 'epsylon@riseup.net'

  Launch it as daemon (notify via email when finish):

    python3 pydog4apache -n 'epsylon@riseup.net' &

###############################
# Updating
###############################

  PyDog4Apache implements an option to update the tool to the latest stable version.

  This feature can be used only if you have cloned it from GitHub respository.

  To check your version you should launch:

    python3 pydog4apache --update

  This will update the tool automatically removing all files from old package.

###############################
# Timelog
###############################

--------------------------
  08.01.2020 : v.0.2
--------------------------
  11.04.2016 : v.0.1b
--------------------------

###############################
# Contribute
###############################

 To make donations use the following hash:
  
  - Bitcoin: 19aXfJtoYJUoXEZtjNwsah2JKN9CK5Pcjw

############
