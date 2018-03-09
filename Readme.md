S2Innovation Panic alarms configuration script
==============================================

Usage
-----
Donwload Excel file from:
[ujchmura-my.sharepoint.com](https://ujchmura-my.sharepoint.com/:x:/g/personal/wojciech_kitka_uj_edu_pl/EX3O5y06qApDknmXcrPck08Buvf2Sx_n88XfBHnlDlnDOg)

Run command to apply configuration from Excel file:

```console
python read_xlsx.pl
```
Run command add PyAlarm devices to Tango DB:
```console
python add_PyAlarm_dev.py
```
Run command get configuration of *test/folder/tmp*:
```console
python get_dev_conf.py test/folder/tmp
```

Requirements
------------

- [Pandas](https://github.com/pandas-dev/pandas)
- [DSconfig](https://github.com/MaxIV-KitsControls/lib-maxiv-dsconfig.git)
- [fandango](https://github.com/tango-controls/fandango)
- [PyTango](https://github.com/tango-controls/pytango)
- [PANIC](https://github.com/tango-controls/PANIC)

```console
pip install -r requirements.txt
```