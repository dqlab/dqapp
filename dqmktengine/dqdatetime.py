import sys
from datetime import datetime
from dqproto import *

'''###############################To DateTime###############################'''
def to_datetime(date, date_format):
    '''
    args:
        1. date: string, i.e.'3M'
    return:
        dqproto.Period
    '''
    try:
        return datetime.strptime(date, date_format)
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
'''###############################To Excel Date#############################'''
def to_excel_date(date, date_format):
    '''
    args:
        1. src: string, i.e.'3M'
    return:
        dqproto.Period
    '''
    try:
    
        temp = datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
        delta = to_datetime(date, date_format) - temp
        return int(float(delta.days) + (float(delta.seconds) / 86400))
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

'''###############################To DateTime###############################'''
def to_date(date, date_format):
    '''
    args:
        1. date: string, i.e.''
    return:
        dqproto.Period
    '''
    try:
        tmp = to_datetime(date, date_format)
        return dqCreateProtoDate(tmp.year, tmp.month, tmp.day)
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
'''###############################To Preiod#################################'''
# Proto Period
def to_period(src):
    '''
    args:
        1. src: string, i.e.'3M'
    return:
        dqproto.Period
    '''
    try:
        term = Period()
        if src.lower() == 'on':
            term.length = 1
            term.units = DAYS
            term.special_name = ON
        elif src.lower() == 'tn':
            term.length = 1
            term.units = DAYS
            term.special_name = TN
        else:
            term.special_name = INVALID_SPECIAL_PERIOD
            term.length = int(src[0:len(src) - 1])
            if src[len(src) - 1].lower() == 'd':
                term.units = DAYS
            elif src[len(src) - 1].lower() == 'w':
                term.units = WEEKS
            elif src[len(src) - 1].lower() == 'm':
                term.units = MONTHS
            elif src[len(src) - 1].lower() == 'y':
                term.units = YEARS
        return term
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
'''###############################To Calendar Name List#####################'''
# Proto CalendarNameList
def to_calendar_name_list(cal_list):
    '''
    args:
        1. cal_list: list of string, i.e.['cal_cfets', 'cal_target']
    return:
        dqproto.CalendarNameList
    '''
    try:
        pb_cals = list()
        for cal in cal_list:
            pb_cals.append(CalendarName.DESCRIPTOR.values_by_name[cal.upper()].number)
        p_calendar_list = dqCreateProtoCalendarNameList(pb_cals)
        return p_calendar_list
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
