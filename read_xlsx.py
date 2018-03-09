#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import pandas as pd
    import traceback
    import logging
    import panic
except Exception as e:
    logging.error('Missing dependencies', traceback.format_exc())

alarms = panic.api() 

try:
    df = pd.read_excel('PANIC-Solaris-138.xlsx', sheetname='PANIC-S2I')
    tag = df['tag'].apply(lambda x: str(x).replace(' ', '_').replace('-', '_').replace('\\', '_').replace('/', '_').replace('__', '_').upper().strip())
except Exception as e:
    logging.error(traceback.format_exc())

# count number of updated alarms
_up = 0

for j, i in df.index:

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

        if 'tak' in _update:
            _overwrite=True
            _up += 1
            print('%s: %s updated'%(_up, _tag))
        else:
            _overwrite=False

    #	alarms.check_tag(_tag ,raise_=True)
        alarms.add(tag=_tag ,formula=_formula, device=_device, description=_description, receivers=_receivers, severity=_severity, overwrite=_overwrite)
        print('Dev: %s'%(_device))
    except Exception as e: 
        logging.warning(e)
    finally:
        pass

print ('#'*80)
print('Total number of alarms %s, updated: %s'%(j+1, _up))
print ('#'*80)
