#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
import sys
import pprint

try:
    import PyTango
except Exception as e:
    logging.error('Missing dependencies', traceback.format_exc())

db = PyTango.Database()
pp = pprint.PrettyPrinter(indent=4)


print('This is the name of the script: %s', sys.argv[0])
#print "Number of arguments: ", len(sys.argv)

device_name = str(sys.argv[1:][0])
print('The arguments are: %s'%device_name)
pyalarm02 = PyTango.DeviceProxy(device_name)
# print attribute list
print('%s attributes:'%device_name)
_attr = pyalarm02.get_attribute_list()
pp.pprint(_attr)
# print property list
print('%s properties:'%device_name)
_prop = pyalarm02.get_property_list('*')
pp.pprint(pyalarm02.get_property(_prop))
print ('#'*80)