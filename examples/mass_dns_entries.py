#!/usr/bin/env python

# Usage: ./dns_entries.py [add|remove] [filename.txt]
# This script is used for doing mass DNS entry/deletion operations into Netdot.
# Created by : Kapil Agrawal 
# Network Engineer
# National Center for Supercomputing Applications


'''
To add DNS entries within the file, the format should be as follows :
~ Example :
test-entry1.ncsa.illinois.edu 141.142.0.10
test-entry2.ncsa.illinosi.edi 141.142.0.11

then run : ./dns_entries.py add [filename.txt]

To remove DNS entries specified within the file, the format should be as follows:
~ Example:
test-entry1.ncsa.illinois.edu
test-entry2.ncsa.illinois.edu 

then run : ./dns_entries.py remove [filename.txt]
'''

import sys
from netdot import Client
import re
import urllib3
urllib3.disable_warnings()

if len(sys.argv)!=3:
    print "Usage: ./dns_entries.py [add|remove] [filename.txt]"
    print "For more details please refer NetEng Wiki"
    exit()

option=sys.argv[1]
filename=sys.argv[2]

########## Connection Information - Do not Change ###########
user = 'username'
password = 'password'
server = "https://enter.netdot.url.here/netdot"
debug = 0
dot = Client.Connect(user, password, server, debug)
#############################################################
def dns_creator(filename):
    try:
        with open(filename) as fileobj:
            l=[items.rstrip() for items in fileobj.readlines()]
            for name_ip in l:
                print name_ip
                entry = name_ip.split(' ')
                #Push entry via REST API entry[0] -> entry[1]
                host = {
                        'name': entry[0],
                        'address': entry[1],
                        'info': 'Activated by import script'
                        }
                response = dot.create_host(host)
                print "%s => %s was added\n" %(entry[0],entry[1])

    except Exception as e:
        print e


def dns_deleter(filename):
    not_deleted = dict()
    hostnames = [line.strip() for line in open(filename)]
    for hostname in hostnames:
        try:
            r = dot.get_host_by_name(hostname)
            #regex the output of finding the host to get the RR ID
            #regex_rrid = re.compile(r'\'RR\':\s{\'(\d{6,10})\'',re.I)
            regex_rrid = re.compile(r'\'(\d{6})\':',re.I)
            #search the dot.get output for the regex above
            rrid_result = regex_rrid.findall(str(r))
            #print str(r)
            #If we find an RRID in the output, assign a variable and use it
            #in the delete method of netdot-client-python
            if rrid_result:
                #print rrid_result
                for item in rrid_result:
                    rrid = item
                    #print rrid
                    #delete from netdot
                    delete1 = dot.delete_host_by_rrid(rrid)
                print hostname+' was deleted'
        except Exception as e:
            not_deleted[ hostname ] = e

    if len(not_deleted) > 0:
            for hostname, error in not_deleted.items():
                    print "%s\t%s" % (hostname, error)

if option=='add':
    dns_creator(filename)

elif option=='remove':
    dns_deleter(filename)

else:
    print sys.argv[1]+" was an incorrect option.\n"
    print "Usage: ./dns_entries.py [add|remove] [filename.txt]"
