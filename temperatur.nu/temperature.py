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

=head2 Monitoring one location per graph

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
            
=head2 Monitoring multiple locations in one graph

        Symlink this file in your plugins directory like so:

        ln -s /usr/local/share/munin/plugins/temperature.py /usr/local/etc/munin/plugins/temperature
        
        In your plugin-config.d/plugins.conf, setup locations in a comma separated list:
        
        [temperature]
            env.locations goteborg,kista,malmo,abisko 
        
        Other configuration options from the single location example above is applicable when monitoring
        multiple locations as well.

        In addition you can also provide a unique name for the graph if you wish to have more than one 
        combined graph:
        
        [temperature01]
            env.locations goteborg,kista,malmo
            env.name Cities
            
        [temperature02]
            env.locations abisko,kurravaara,lannavaara,nikkaluokta
            env.name Northern locations

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

    1.1

=head1 CHANGELOG

=head2 1.0 - 2014-05-15
 
    First release
    
=head2 1.1 - 2014-5-16

    Added support for graphing multiple locations in the same graph
  
=cut
"""
__version__ = '1.1'

import os, sys, urllib, re
from string import Template

plugin_name = list(os.path.split(sys.argv[0]))[1]
hostname = os.getenv("hostname", "")
category = os.getenv("category", "temperature")
location_list = os.getenv("locations", "")
name = os.getenv("name", "")

if name:
    graph_name = " (" + name + ")"
else:
    graph_name = ""

# Check if we're running in multi location mode or not
if len(list(plugin_name.split("_"))) == 1:
    locations = list(location_list.replace(" ", "").split(","))
    location_title = "Temperature graph" + graph_name
else:
    locations = [ plugin_name.split("_")[1] ]
    location_title = "Temperature for location " + locations[0]

if not locations:
    locations = [ "ekholmen" ]


def config():
    conf = Template("""graph_title ${location_title}
graph_vtitle Degrees Celsius
graph_args --base 1000 -l 0
graph_category ${category}""")
    print conf.safe_substitute(location_title = location_title, category = category)

    if hostname:
        print "host_name " + hostname


    if len(locations) == 1:
        print locations[0] + ".label Temp (C)"
    else:
        for location in locations:
            print location + ".label " + location

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

    for location in locations:
        url = "http://www.temperatur.nu/termo/" + location + "/temp.txt"
    
        # Fetch web page for location
        conn = urllib.urlopen(url)
        resp = conn.read()
        conn.close()

        # Remove all whitespace from response
        pattern = re.compile(r'\s+')
        value = re.sub(pattern, "", resp)
    
        print_values(location, value)

def print_values(location, value):
    # Test for numberiness and report result accordingly
    if isfloat(value):
        print location + ".value " + value
    else:
        print location + ".value U"


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
