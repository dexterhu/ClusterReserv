#!/usr/bin/python

import os
import string
import sys
import re
import glob
import urllib2
import math
import random
import datetime
import zlib
import unittest
import doctest
import smtplib

from configobj import ConfigObj

# combine all authorized users for a particular cluster node. note that
# we assume that this program runs in the master node, which has home directory for
# all users, and each user has generated id_rsa.pub in his ~/.ssh folder  
def combine_files(userList, nodefn):
    f = open(nodefn, 'w')
    for user in userList:
        print 'appending id_rsa.pub for %s' % user
        f.write(open("/home/"+user+"/.ssh/id_rsa.pub").read())
    f.close()


registered_userconfig = ConfigObj("conf/userlist")
registered_user_list = userconfig['userlist']

# create the empty authorized_keys for each node
#nodelist = []
#for line in open("conf/nodelist"):
#    li=line.strip();
#    if not li.startswith("#"):
#        nodelist.append(li)
#	if not os.path.exists('sshdata/' + li):
#  		os.mkdir('sshdata/' + li)
# 		open('sshdata/'+li+'/authorized_keys', 'w').close()

#for user in userlist:
#        if not os.path.exists('sshdata/' + user):
#                os.mkdir('sshdata/' + user)


# Parse the reservation time table according to update the authorized_keys for TODAY ( the finest reservation unit is day)
rules = ConfigObj("conf/ReservationTable")
now = datetime.datetime.now().strftime('%Y%m%d')
reservation_list = rules['userlist']
print reservation_list
accessdict = {}
for user in reservation_list :
	section = rules[user]
	nodelist = section['nodelist']
	st = section['starttime']
	et = section['endtime']
	if ( now >= st and now <= et ):
		for node in nodelist:
     			if (accessdict.has_key(node)):
              	     		accessdict[node].append(user)
			else:
				accessdict[node]=[]
		    		accessdict[node].append(user)
print accessdict

# update the /etc/ssh/sshd_config of its allowed user list for sshd in a remote cluster node
for node in accessdict:
	os.system("ssh -l root " + node + " 'bash -s' < addalloweduser.sh '" + " ".join(accessdict[node]) + "'")

# TODO email users about the start or ending of his session and also the reserved nodes


# TODO setup the passwordless login for that user among his reserved machine and of course the master node
