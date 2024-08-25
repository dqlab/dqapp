# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 16:04:57 2021

@author: dzhu
"""
from datetime import datetime
from dqdatetime import *

####################################################
def test_to_datetime():
    res = to_datetime('2021-07-22', '%Y-%m-%d')
    test = (res == datetime(2021,7,22))
    res = to_datetime('20210722', '%Y%m%d')
    test = test and (res == datetime(2021,7,22))
    print(test)
    return test

####################################################
def test_to_excel_date():
    res = to_excel_date('2021-07-22', '%Y-%m-%d')
    print(res)
    test = (res == 44399)
    res = to_excel_date('20210722', '%Y%m%d')
    print(res)
    test = test and (res == 44399)
    return test

####################################################
def test_to_date():
    res = to_date('2021-07-22', '%Y-%m-%d')
    print(res)
    test = (res.year == 2021) and (res.month == 7) and (res.day == 22)     
    return test

####################################################
def test_to_period():
    res = to_period('3m')
    print(res)
    test = (res.length==3) and (res.units==MONTHS)
    return test

###################################################
def test_to_calendar_name_list():
    res = to_calendar_name_list(['cal_cfets', 'target'])
    print(res)
    test = (res.calendar_name[0] == CAL_CFETS) and (res.calendar_name[1] == TARGET)   
    return test

###############################################################################
test_to_datetime()
test_to_excel_date()
test_to_date()
test_to_period()
test_to_calendar_name_list()
        