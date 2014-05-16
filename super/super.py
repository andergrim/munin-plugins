#!/usr/local/bin/python2
# For Linux environments use #!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
: << =cut

=head1 NAME

Super

=head1 DESCRIPTION
 
    This plugin monitors the usage of words including "super" and
    checkmarks on aftonbladet.se
    
    This plugin requires python and Beautiful Soup
    
=head1 CONFIGURATION
    
    Symlink this file in your plugins directory like so:
        
    ln -s /usr/local/share/munin/plugins/super.py /usr/local/etc/munin/plugins/super

    hostname will default to whatever node the plugin is run on.
    Graph category defaults to "web"
    
    Both values might be configured in plugin-config.d/plugins.conf

    Example:

    [super]
        env.hostname web.misc.
        env.category web

   If hostname is set you will need to configure the check in your main munin.conf:
      
   [web.misc.]
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
 
    First release

=cut
"""

__version__ = '1.0'

import os, sys, urllib, re

hostname = os.getenv("hostname", "")
category = os.getenv("category", "web")
plugin_name = list(os.path.split(sys.argv[0]))[1]

def config():
    print "multigraph " + plugin_name + "_super"
    print "graph_title Aftonbladet SUPER usage"
    print "graph_vtitle Occurrences"
    print "graph_args --base 1000 --lower-limit 0"
    print "graph_category " + category
    if hostname:
        print "host_name " + hostname
    print "super.label Super"
    print "super.draw AREA"
    print "super.type GAUGE"
    print "super.min 0"
    print "\n"

    print "multigraph " + plugin_name + "_checkmark"
    print "graph_title Aftonbladet CHECK usage" 
    print "graph_vtitle Occurrences"
    print "graph_args --base 1000 --lower-limit 0"
    print "graph_category " + category 
    if hostname:
        print "host_name " + hostname
        print "check.label Check"
    print "check.draw AREA"
    print "check.type GAUGE"
    print "check.min 0"

    sys.exit(0)

def autoconf():
    try:
        from bs4 import BeautifulSoup
        print "yes"
    except ImportError:
        print "no (Missing python module BeautifulSoup 4)"

    sys.exit(0)


def fetch():
    from bs4 import BeautifulSoup

    # Fetch web page
    url = "http://www.aftonbladet.se/"
    conn = urllib.urlopen(url)
    html = conn.read()
    conn.close()

    # Load web page into bs4    
    soup = BeautifulSoup(html)

    # Count occurrences of "super" among all words
    tags = soup.find_all([ "h1", "h2", "h3", "span", "p" ])

    super_sentences = []
    super_words = []
    for tag in tags:
        words = re.findall(r'\w+', tag.text, re.U)
        for word in words:
            if re.search('(?i)super', word, re.U):
                super_words.append(word.encode("utf-8"))
                super_sentences.append(tag.text.encode("utf-8"))

    num_super = len(super_words)

    # Count occurrences of checkmarks
    checkmarks = soup.find_all("span", "abSymbBo")
    num_checkmarks = len(checkmarks)

    print "multigraph " + plugin_name + "_super"
    if isinstance(num_super, int):
        print "super.value " + str(num_super)
    else:
        print "super.value U"

    print "multigraph " + plugin_name + "_checkmark"
    if isinstance(num_checkmarks, int):
        print "check.value " + str(num_checkmarks)
    else:
        print "check.value U"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            config()
        elif sys.argv[1] == "autoconf":
            autoconf()
        else:
            raise ValueError, "Unknown parameter '%s'" % sys.argv[1]
            sys.exit(1)

fetch()
sys.exit(0)
