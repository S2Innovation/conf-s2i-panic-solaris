#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import pandas as pd
    import traceback
    import logging
    import panic
    import argparse
except Exception as e:
    logging.error('Missing dependencies', traceback.format_exc())

parser = argparse.ArgumentParser()
parser.add_argument("--test", help='Run the script in test mode - create alarms in a test device.', action="store_true")
args = parser.parse_args()

if args.test:
    logging.info("Running in test mode")


alarms = panic.api() 

try:
    df = pd.read_excel('PANIC-Solaris-138.xlsx', sheetname='PANIC-S2I')
    tag = df['tag'].apply(lambda x: str(x).replace(' ', '_').replace('-', '_').replace('\\', '_').replace('/', '_').replace('__', '_').upper().strip())
except Exception as e:
    logging.error(traceback.format_exc())

# count number of updated alarms
_up = 0

ELOG_DEVICE = 'alarm/ctl/elogsnd1/create_entry'

ALARM_TEST_DEVICE = "alarm/vm/alarm1"

LOGBOOK_MATCH = {
    '_default':'Storage Ring',
    'I': 'Injector',
    'R1': 'Storage Ring',
    'BL': 'Storage Ring'
}

for i in df.index:

    try:
        _update = df['update'][i].encode('utf-8').strip().lower()
        _tag = tag[i]
        _formula = df['formula'][i]
        # _device_tmp = 'alarm/com/alarm02'
        _device = df['alarm_device'][i]
        _description = df['description'][i].encode('utf-8').strip()
        _sms = str(df['sms'][i]).replace(' ', '').strip().replace('+', '')
        _rece = df['receivers'][i].encode('utf-8').strip()
        #    _file = 'panic_' + df['system'][i].encode('utf-8').strip() + '_' + df['podsystem'][i].encode('utf-8').strip() + '.log'
        _receivers = (_rece.split(',')[1].encode('utf-8').strip() if (',' in _rece) else _rece) +  ',SMS:' + _sms # ',file:/common/PANIC/'+_file
        _severity = df['severity'][i].encode('utf-8').strip()

        # update receivers with elog integration
        _elog_subsystem = df['podsystem'][i].encode('utf-8').strip()

        _elog_level = 'Report'
        if _severity.upper() == 'ALARM':
            _elog_level = 'Problem'

        _system = df['system'][i].encode('ascii').strip()
        _elog_logbook = LOGBOOK_MATCH.get(_system, LOGBOOK_MATCH['_default'])

        _receivers += ',ACTION(alarm:command,' + ELOG_DEVICE + ',$REPORT,$NAME,$DESCRIPTION'
        _receivers += ",'%s'" % _elog_subsystem
        _receivers += ",'%s'" % _elog_level
        _receivers += ",'Operation'"
        _receivers += ",'%s'" % _elog_logbook
        _receivers += ")"

        if 'tak' in _update:
            _overwrite=True
            _up += 1
            print('%s: %s updated'%(_up, _tag))
        else:
            _overwrite=False

        if args.test:
            _device = ALARM_TEST_DEVICE

    #	alarms.check_tag(_tag ,raise_=True)
        alarms.add(tag=_tag ,formula=_formula, device=_device, description=_description, receivers=_receivers, severity=_severity, overwrite=_overwrite)
        print('Dev: %s'%(_device))
    except Exception as e: 
        logging.warning(e)
    finally:
        pass

print ('#'*80)
print('Total number of alarms %s, updated: %s'%(i+1, _up))
print ('#'*80)
