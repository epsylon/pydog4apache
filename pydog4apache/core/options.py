#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
PyDog4Apache - 2016/2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyDog4Apache; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import optparse

class PyDog4ApacheOptions(optparse.OptionParser):
    def __init__(self, *args):
        optparse.OptionParser.__init__(self, 
                           description='\nApache web logs sneaker - 2016/2020 - by psy (https://03c8.net)',
                           prog='pydog4apache.py',
                           version='\nVersion: v0.2 (2020) - https://pydog4apache.03c8.net\n')
        self.add_option("-u", "--update", action="store_true", dest="update", help="check for latest stable version")
        self.add_option("-v", "--verbose", action="store_true", dest="verbose", help="active verbose output")
        group1 = optparse.OptionGroup(self, "*Reporting*")
        group1.add_option("-r", action="store", dest="file", help="generate file with results (ex: -r 'visitants.txt')")
        group1.add_option("-n", action="store", dest="emails", help="notify via email (foo@email.net,bar@email.org,...)")
        self.add_option_group(group1)

    def get_options(self, user_args=None):
        (options, args) = self.parse_args(user_args)
        return options
