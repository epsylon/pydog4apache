  
![c](https://03c8.net/images/pydo4apache_banner.png "Pydog4apache")

----------

#### Info:

Apache web logs sneaker - 2016/2020 - by psy [03c8.net]

  With this tool you can search for specific keywords (such as: government, police...) 
  on Whois description of the IPs of your website visitors by -automagically- analyzing 
  Apache logs provided (you can set folders of logs to -sneak- all your projects).

  Also you can generate a report with results or send them to a list of email recipients
  like an alert.

----------

 + Web: https://pydog4apache.03c8.net 

----------

#### Installing:

  PyDog4Apache runs on many platforms. It requires Python (3.x.y) and the following libraries:

       python3-pip - Python package installer
       ipwhois (0.10.3)  - Retrieve and parse whois data for IPv4 and IPv6 addresses.

  On Debian-based systems (ex: Ubuntu), run: 

       sudo apt-get install python3-pip && sudo pip3 install ipwhois

  Or:

       sudo apt-get install python3-pip && pip3 install ipwhois==0.10.3 --user

  Source libs:

       * Pypi-ipwhois: https://pypi.python.org/pypi/ipwhois/

----------

#### Examples:

  Verbose:

    python3 pydog4apache -v 

  Update:

    python3 pydog4apache --update

  Generate report file:

    python3 pydog4apache -r my_visitants.txt

  Notify results via email to some recipients:

    python3 pydog4apache -n='root@localhost,foo@email.org,bar@email.net'

  Combine options:

    python3 pydog4apache -v -r my_visitants.txt -n epsylon@riseup.net

  Launch it as daemon (notify via email when finish):

    python3 pydog4apache -n epsylon@riseup.net &

----------

#### License:

  Pydog4apache is released under the GPLv3.

#### Contact:

    - psy (epsylon@riseup.net)

#### Contribute: 

  To make donations use the following hash:
  
    - Bitcoin: 19aXfJtoYJUoXEZtjNwsah2JKN9CK5Pcjw

