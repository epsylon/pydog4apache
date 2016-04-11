#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PyDog4Apache - 2016 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyDog4Apache; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import optparse

class PyDog4ApacheOptions(optparse.OptionParser):
    def __init__(self, *args):
        optparse.OptionParser.__init__(self, 
                           description='\nApache web logs sneaker - by psy',
                           prog='pydog4apache.py',
                           version='\nVersion: v0.1b\n')
        self.add_option("-u", "--update", action="store_true", dest="update", help="check for latest stable version")
        self.add_option("-v", "--verbose", action="store_true", dest="verbose", help="active verbose output")
        group1 = optparse.OptionGroup(self, "*Reporting*")
        group1.add_option("-r", action="store", dest="file", help="generate file output with 'visitants'")
        group1.add_option("-n", action="store", dest="emails", help="notify via email (foo@email.net,bar@email.org,...)")
        self.add_option_group(group1)

    def get_options(self, user_args=None):
        (options, args) = self.parse_args(user_args)
        return options
