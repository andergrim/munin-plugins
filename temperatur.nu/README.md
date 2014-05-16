# NAME

temperatur.nu - Munin plugin to monitor weather station temperatures on temperatur.nu

# DESCRIPTION

This plugin monitors temperature from one or more stations on the distributed weather station site temperatur.nu.

This plugin requires python and ...

# CONFIGURATION

## Monitoring one location per graph

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
            
## Monitoring multiple locations in one graph

Symlink this file in your plugins directory like so:

    ln -s /usr/local/share/munin/plugins/temperature.py /usr/local/etc/munin/plugins/temperature
        
In your plugin-config.d/plugins.conf, setup locations in a comma separated list:
        
    [temperature]
        env.locations goteborg,kista,malmo,abisko 
        
Other configuration options from the single location example above is applicable when monitoring multiple locations as well.

In addition you can also provide a unique name for the graph if you wish to have more than one combined graph:
        
    [temperature01]
        env.locations goteborg,kista,malmo
        env.name Cities
            
    [temperature02]
        env.locations abisko,kurravaara,lannavaara,nikkaluokta
        env.name Northern locations

# AUTHOR

Kristoffer Andergrim <andergrim@gmail.com>

# LICENSE

Permission to use, copy, and modify this software with or without fee
is hereby granted, provided that this entire notice is included in
all source code copies of any software which is or includes a copy or
modification of this software.

THIS SOFTWARE IS BEING PROVIDED "AS IS", WITHOUT ANY EXPRESS OR
IMPLIED WARRANTY. IN PARTICULAR, NONE OF THE AUTHORS MAKES ANY
REPRESENTATION OR WARRANTY OF ANY KIND CONCERNING THE
MERCHANTABILITY OF THIS SOFTWARE OR ITS FITNESS FOR ANY PARTICULAR
PURPOSE.

# CONTRIBUTE

find this plugin on github at https://github.com/andergrim/munin-plugins

# VERSION

    1.1

# CHANGELOG

## 1.0 - 2014-05-15
 
    First release
    
## 1.1 - 2014-5-16

    Added support for graphing multiple locations in the same graph
  