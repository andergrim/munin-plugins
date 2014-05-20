#!/usr/local/bin/python2
# For Linux environments use #!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
: << =cut

=head1 NAME

Super

=head1 DESCRIPTION
 
    This plugin monitors the usage of words including "super" and
    checkmarks on aftonbladet.se and expressen.se
    
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

    1.1

=head1 CHANGELOG

=head2 1.0 - 2014-05-16
 
    First release

=head2 1.1 - 2014-05-20
 
    Support for multiple providers of super news

=cut
"""

__version__ = '1.1'

import os, sys, urllib, re

hostname = os.getenv("hostname", "")
category = os.getenv("category", "web")
plugin_name = list(os.path.split(sys.argv[0]))[1]

providers = [
              { "short":  "ab",
                "name":   "Aftonbladet",
                "colour": "CE181E",
                "url":    "http://www.aftonbladet.se/",
                "tags":  [ "h1", "h2", "h3", "span", "p" ],
                "check": {
                  "element": "span",
                  "attr":    "class",
                  "value":   "abSymbBo"
                }
              },
              { "short":  "ex",
                "name":   "Expressen",
                "colour": "0366A0",
                "url":    "http://www.expressen.se/",
                "tags":  [ "a", "span", "p" ] ,
                "check": {
                  "element": "",
                  "attr"   : "text",
                  "value"  : "\xe2\x9c\x93"
                }
              }
           ]


def config():
    global providers

    print "multigraph " + plugin_name + "_super"
    print "graph_title SUPER usage"
    print "graph_vtitle Occurrences"
    print "graph_args --base 1000 --lower-limit 0"
    print "graph_category " + category

    if hostname:
        print "host_name " + hostname

    for provider in providers:
      print provider["short"] + "_super.label " + provider["name"]
      print provider["short"] + "_super.draw AREASTACK"
      print provider["short"] + "_super.type GAUGE"
      print provider["short"] + "_super.colour " + provider["colour"]
      print provider["short"] + "_super.min 0"

    print "\n"

    print "multigraph " + plugin_name + "_checkmark"
    print "graph_title CHECKMARK usage" 
    print "graph_vtitle Occurrences"
    print "graph_args --base 1000 --lower-limit 0"
    print "graph_category " + category 

    if hostname:
        print "host_name " + hostname

    for provider in providers:
      print provider["short"] + "_check.label " + provider["name"]
      print provider["short"] + "_check.draw AREASTACK"
      print provider["short"] + "_check.type GAUGE"
      print provider["short"] + "_check.colour " + provider["colour"]
      print provider["short"] + "_check.min 0"

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

  num_super = { }
  num_checkmarks = { }

  for provider in providers:

    # Fetch web page
    conn = urllib.urlopen(provider["url"])
    html = conn.read()
    conn.close()

    # Load web page into bs4    
    soup = BeautifulSoup(html)

    # Count occurrences of "super" among all words
    tags = soup.find_all(provider["tags"])

    super_words = []
    for tag in tags:
      words = re.findall(r'\w+', tag.text, re.U)
      for word in words:
        if re.search('(?i)super', word, re.U):
          super_words.append(word.encode("utf-8"))

    # Remove duplicates and sum up
    super_words = list(set(super_words))
    num_super[provider["short"]] = len(super_words)

    # Count occurrences of checkmarks
    if provider["check"]["attr"] == "class":
      checkmarks = soup.find_all(provider["check"]["element"], provider["check"]["value"])
    elif provider["check"]["attr"] == "text":
      checkmarks = soup.find_all(text = provider["check"]["value"])

    num_checkmarks[provider["short"]] = len(checkmarks)

  # Print results
  print "multigraph " + plugin_name + "_super"

  for provider in providers:
    tag = provider["short"]
    if isinstance(num_super[tag], int):
      print tag + "_super.value " + str(num_super[tag])
    else:
      print tag + "_super.value U"

  print "multigraph " + plugin_name + "_checkmark"
  
  for provider in providers:
    tag = provider["short"]
    if isinstance(num_checkmarks[tag], int):
      print tag + "_check.value " + str(num_checkmarks[tag])
    else:
      print tag + "_check.value U"

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
