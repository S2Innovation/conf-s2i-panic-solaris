#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import traceback

try:
    import PyTango
    import json
    from dsconfig import dump
    import fandango.tango as ft
except Exception as e:
    logging.error('Missing dependencies', traceback.format_exc())

######### dump Server PyTango #########
db = PyTango.Database()
timestr = time.strftime("%Y-%m-%d_%H%M%S")
l=list()


KLASS = 'PyAlarm'

l.append('server:%s/*'%KLASS)
BACKUP_NAME = ('PyAlarm_dump_' + timestr)
dbdata = dump.get_db_data(db, l)
with open(BACKUP_NAME, 'w') as outfile:
    json.dump(dbdata, outfile, ensure_ascii=False, indent=4, sort_keys=True)
print(dbdata)

######### Create device #########
dev_list = {
        # 'CTL_I_01' : 'ALARM/CTL/I_CTL_PYALARM01',
        # 'CTL_R1_01' : 'ALARM/CTL/R1_CTL_PYALARM02',
        # 'DIA_I_01' : 'ALARM/DIA/I_DIA_PYALARM01',
        # 'DIA_R1_01' : 'ALARM/DIA/R1_DIA_PYALARM02',
        # 'MAG_I_01' : 'ALARM/MAG/I_MAG_PYALARM01',
        # 'MAG_R1_01' : 'ALARM/MAG/R1_MAG_PYALARM02',
        # 'PLC_I_01' : 'ALARM/PLC/I_PLC_PYALARM01',
        # 'PLC_R1_01' : 'ALARM/PLC/R1_PLC_PYALARM02',
        # 'PSS_I_01' : 'ALARM/PSS/I_PSS_PYALARM01',
        # 'PSS_R1_01' : 'ALARM/PSS/R1_PSS_PYALARM02',
        # 'RAD_I_01' : 'ALARM/RAD/I_RAD_PYALARM01',
        # 'RAD_R1_01' : 'ALARM/RAD/R1_RAD_PYALARM02',
        # 'RF_I_01' : 'ALARM/RF/I_RF_PYALARM01',
        # 'RF_R1_01' : 'ALARM/RF/R1_RF_PYALARM02',
        # 'VAC_I_01' : 'ALARM/VAC/I_VAC_PYALARM01',
        'VAC_R1_01' : 'ALARM/VAC/R1_VAC_PYALARM02'
}

######### Add property #########
device_properties = {'EvalTimeout': ['1000'],
        'MaxMessagesPerAlarm': ['3'],
        'PollingPeriod': ['10.0'],
        'HtmlFolder': ['/tmp/htmlreports'],
        'StartupDelay': ['30'],
        'Enabled': ['True'],
        'AlarmThreshold': ['0'],
        'RethrowState': ['False'],
        'VersionNumber': ['6.3.2'],
        'CreateNewContexts': ['True']
        }

def add_new_panic_dev(_server, _klass, _device, _prop_dict):
    ft.add_new_device(_server, _klass, _device)
    ft.put_device_property(_device, _prop_dict)
    ft.Astor(_device).start_servers()

for l in dev_list.keys():
    # print('PyAlarm/%s, PyAlarm, %s'%(l, dev_list[l]))
    add_new_panic_dev("/".join([KLASS, l]), KLASS, dev_list[l], device_properties)