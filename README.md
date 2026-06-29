  
![c](https://03c8.net/images/pydo4apache_banner.png "Pydog4apache")

----------

#### Info:

Apache web logs sneaker - 2016/2026 - by psy [03c8.net]

  PyDog4Apache sends 'dogs' to sniff your Apache access logs and, for every
  visitor IP, it queries its WHOIS record looking for specific keywords on the
  network description (the organization that owns that IP range).

  This way you can -automagically- discover *who* is really behind your
  visitors: governments, police, military, intelligence, banks, universities,
  AI crawlers (such as: Anthropic), cloud/hosting providers, datacenters...
  by matching their WHOIS organization against the words listed on `keywords.txt`.

  You can set several folders of logs on `sources.txt` to -sneak- all your
  projects at once (compressed `.gz` logs are also analyzed). Finally you can
  generate a report with the results or send them to a list of email recipients
  like an alert.

----------

 + Web: https://pydog4apache.03c8.net 

----------

#### Installing:

  PyDog4Apache runs on many platforms. It requires Python (3.x.y) and the following libraries:

       python3-pip - Python package installer
       ipwhois (1.3.0)  - Retrieve and parse whois data for IPv4 and IPv6 addresses.

  On Debian-based systems (ex: Ubuntu), run: 

       sudo apt-get install python3-pip && pip3 install ipwhois --user

  Or to pin the tested version:

       pip3 install -r docs/requirements.txt --user

  Source libs:

       * Pypi-ipwhois: https://pypi.org/project/ipwhois/

----------

#### Configuring:

  - `sources.txt` : one folder per line with the Apache logs to analyze (default: `/var/log/apache2`).
  - `keywords.txt` : one keyword per line to look for on the WHOIS network description.

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

  To make donations use the following hashes:
  
    - Bitcoin [BTC]: 19aXfJtoYJUoXEZtjNwsah2JKN9CK5Pcjw
    - Ecoin [ECO]: EZnYs33TG87ZzBWgADrj8653s3bPUqreW9
