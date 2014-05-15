#!/usr/local/bin/python
# For Linux environments use #!/usr/bin/python 

"""
: << =cut

=head1 NAME

temperatur.nu - Munin plugin to monitor weather station temperatures on temperatur.nu

=head1 DESCRIPTION

This plugin monitors temperature from one or more stations on 
    the distributed weather station site temperatur.nu.

This plugin requires python and ...

=head1 CONFIGURATION

	Symlink this file in your plugins directory 
	like so:

	ln -s /usr/local/share/munin/plugins/temperature.py /usr/local/etc/munin/plugins/temperature_partille
	ln -s /usr/local/share/munin/plugins/temperature.py /usr/local/etc/munin/plugins/temperature_sodra_savedalen

	The hostname will default to "temperatures" if not configured in plugin-config.d/plugins.conf

	Example:

	[temperature*]
	    env.hostname weather.misc.

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

=head2 1.0 - 2014/05/15
 
    first release
  
=cut
"""
__version__ = '1.2'

import os, sys
from string import Template

plugin_name = list(os.path.split(sys.argv[0]))[1]

print plugin_name