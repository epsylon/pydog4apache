===========================================================================

 ____        ____              _  _     _                     _
|  _ \ _   _|  _ \  ___   __ _| || |   / \   _ __   __ _  ___| |__   ___
| |_) | | | | | | |/ _ \ / _` | || |_ / _ \ | '_ \ / _` |/ __| '_ \ / _ |
|  __/| |_| | |_| | (_) | (_| |__   _/ ___ \| |_) | (_| | (__| | | |  __/
|_|    \__, |____/ \___/ \__, |  |_|/_/   \_\ .__/ \__,_|\___|_| |_|\___|
       |___/             |___/              |_|

Apache web logs sneaker - 2016/2026 - by psy

===========================================================================

###############################
# Project info
###############################

  Web: https://pydog4apache.03c8.net/ [https://03c8.net]

###############################
# Summary
###############################

  PyDog4Apache is an Apache web logs sneaker.

  It sends 'dogs' to sniff your Apache access logs and, for every visitor IP,
  it queries its WHOIS record looking for specific keywords on the network
  description (the organization that owns that IP range).

  This way you can -automagically- discover *who* is really behind your
  visitors: governments, police, military, intelligence, banks, universities,
  AI crawlers (such as: Anthropic), cloud/hosting providers, datacenters... by
  matching their WHOIS organization against the words listed on 'keywords.txt'.

  You can set several folders of logs on 'sources.txt' to -sneak- all your
  projects at once (compressed '.gz' logs are also analyzed).

  Finally you can generate a report with the results or send them to a list of
  email recipients like an alert.

###############################
# Installing
###############################

  PyDog4Apache runs on many platforms. It requires Python (3.x.y) and the
  following libraries:

      python3-pip - Python package installer
      ipwhois (1.3.0)  - Retrieve and parse whois data for IPv4 and IPv6 addresses.

  On Debian-based systems (ex: Ubuntu), run:

      sudo apt-get install python3-pip && pip3 install ipwhois --user

  Or to pin the tested version:

      pip3 install -r docs/requirements.txt --user

  Source libs:

      * Pypi-ipwhois: https://pypi.org/project/ipwhois/

###############################
# Configuring
###############################

  - sources.txt  : one folder per line with the Apache logs to analyze
                   (default: /var/log/apache2)

  - keywords.txt : one keyword per line to look for on the WHOIS network
                   description. Matching is case-insensitive and by substring.

  - whois_cache.json : auto-generated cache of WHOIS results (ip -> network
                       description). It lets later runs query the WHOIS of only
                       *new* IPs, so it is safe (and fast) to run from a crontab.
                       Delete it (or use --flush-cache) to re-query everything.

###############################
# HowTo
###############################

  Usage: pydog4apache.py [options]

  Options:
    --version          show program's version number and exit
    -h, --help         show this help message and exit
    -u, --update       check for latest stable version
    -v, --verbose      active verbose output
    -f, --flush-cache  delete whois cache (re-query all IPs)

    *Reporting*:
      -r FILE          generate file output with 'visitants'
      -n EMAILS        notify via email (foo@email.net,bar@email.org,...)

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

  Re-query the WHOIS of every IP (ignore the cache):

    python3 pydog4apache --flush-cache

  Run periodically from a crontab (only *new* IPs are queried). Note the 'cd':
  'sources.txt', 'keywords.txt' and 'whois_cache.json' live on the working dir:

    */30 * * * * cd /path/to/pydog4apache && python3 pydog4apache -n 'root@localhost'

###############################
# Updating
###############################

  PyDog4Apache implements an option to update the tool to the latest stable
  version.

  This feature can be used only if you have cloned it from the Git repository.

  To update your copy you should launch:

    python3 pydog4apache --update

###############################
# Timelog
###############################

--------------------------
  29.06.2026 : v.0.3
--------------------------
  08.01.2020 : v.0.2
--------------------------
  11.04.2016 : v.0.1b
--------------------------

###############################
# Contribute
###############################

 To make donations use the following hashes:

  - Bitcoin [BTC]: 19aXfJtoYJUoXEZtjNwsah2JKN9CK5Pcjw
  - Ecoin [ECO]: EZnYs33TG87ZzBWgADrj8653s3bPUqreW9

############
