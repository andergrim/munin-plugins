#!/usr/local/bin/python2
# For Linux environments use #!/usr/bin/env python 

"""
: << =cut

=head1 NAME

temperatur.nu - Munin plugin to monitor weather station temperatures on temperatur.nu

=head1 DESCRIPTION

This plugin monitors temperature from one or more stations on 
    the distributed weather station site temperatur.nu.

This plugin requires python and ...

=head1 CONFIGURATION

	Symlink this file in your plugins directory like so:

	ln -s /usr/local/share/munin/plugins/temperature.py /usr/local/etc/munin/plugins/temperature_partille
	ln -s /usr/local/share/munin/plugins/temperature.py /usr/local/etc/munin/plugins/temperature_sodra_savedalen

	hostname will default to whatever node the plugin is run on.
        Graph category defaults to "temperature"
	
	Both values might be configured in plugin-config.d/plugins.conf

	Example:

	[temperature*]
	    env.hostname weather.misc.
	    env.category sensors
	    
        If hostname is set you will need to configure the check in your main munin.conf:
        
        [weather.misc.]
            address 127.0.0.1
            use_node_name no
            
        

=head1 AUTHOR

Kristoffer Andergrim <andergrim@gmail.com>

=head1 LICENSE

Permission to use, copy, and modify this software with or without fee
is hereby granted, provided that this entire notice is included in
all source code copies of any software which is or includes a copy or
modification of this software.

THIS SOFTWARE IS BEING PROVIDED "AS IS", WITHOUT ANY EXPRESS OR
IMPLIED WARRANTY. IN PARTICULAR, NONE OF THE AUTHORS MAKES ANY
REPRESENTATION OR WARRANTY OF ANY KIND CONCERNING THE
MERCHANTABILITY OF THIS SOFTWARE OR ITS FITNESS FOR ANY PARTICULAR
PURPOSE.

=head1 CONTRIBUTE

find this plugin on github at https://github.com/andergrim/munin-plugins

=head1 MAGIC MARKERS

 #%# family=auto contrib
 #%# capabilities=autoconf

=head1 VERSION

    1.0

=head1 CHANGELOG

=head2 1.0 - 2014-05-16
 
    first release
  
=cut
"""
__version__ = '1.0'

import os, sys, urllib, re
from string import Template

plugin_name = list(os.path.split(sys.argv[0]))[1]
location = plugin_name.split("_")[1]
hostname = os.getenv("hostname", "")
category = os.getenv("category", "temperature")

if location == "":
    location = "ekholmen"

def config():
    conf = Template("""graph_title Temperature for location ${location}
graph_vtitle Degrees Celsius
graph_args --base 1000 -l 0
graph_category ${category}
temp.label Temp (C)""")

    print conf.safe_substitute(location = location, category = category, hostname = hostname)

    if hostname:
        print "host_name " + hostname

    sys.exit(0)
   
def autoconf():
    print "yes"
    sys.exit(0)
    
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

    
def fetch():
    url = "http://www.temperatur.nu/termo/" + location + "/temp.txt"
    
    # Fetch web page for location
    conn = urllib.urlopen(url)
    resp = conn.read()
    conn.close()

    # Remove all whitespace from response
    pattern = re.compile(r'\s+')
    value = re.sub(pattern, "", resp)
    
    print_values(value)


def print_values(value):
    # Test for numberiness and report result accordingly
    if isfloat(value):
        print "temp.value " + value
    else:
        print "temp.value U"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            config()
        elif sys.argv[1] == "autoconf":
            autoconf()
        else:
            raise ValueError, "Unknown parameter '%s'" % sys.argv[1]

fetch()
sys.exit(0)
