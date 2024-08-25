# -*- coding: utf-8 -*-
"""
Created on Sat Sep 09 21:35:35 2017

@author: Dingqiu
"""
import sys
import json
from google.protobuf.json_format import MessageToJson

from datetime import datetime
from dqproto import *
###############################################################################
def save_pb_data(pb_data, name, loc):
    '''
    @args:
        1. pb_data: protobuf message
        2. name: string
        3. loc: string; full path of file destination
    @return:
        
    '''
    try:
        filename = loc + '/' 
        filename += name
        #save as bin file
        f=open(filename+'.bin', 'wb')
        f.write(pb_data.SerializeToString())
        f.close()
        #save as txt file
        with open(filename+'.txt', 'w') as outfile:
            json.dump(MessageToJson(pb_data), outfile)
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def to_datetime(date, date_format):
    '''
    args:
        1. date: string, i.e.'3M'
    return:
        datetime.date
    '''
    try:
        if date=='':
            raise Exception('to_datetime: empty date')
        return datetime.strptime(date, date_format)
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

###############################################################################
def from_datetime_to_date(date):
    '''
    args:
        1. date: string, i.e.'3M'
    return:
        datetime.date
    '''
    try:        
        return dqCreateProtoDate(date.year, date.month, date.day)    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def to_excel_date(date, date_format):
    '''
    args:
        1. src: string, i.e.'3M'
    return:
        Excel Date
    '''
    try:
        if date=='':
            raise Exception('to_excel_date: empty date')
        temp = datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
        delta = to_datetime(date, date_format) - temp
        return int(float(delta.days) + (float(delta.seconds) / 86400))
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

###############################################################################
def to_date(date, date_format):
    '''
    args:
        1. date: string, i.e.''
    return:
        dqproto.Period
    '''
    try:
        if date=='':
            raise Exception('to_date: empty date')
        tmp = to_datetime(date, date_format)
        return dqCreateProtoDate(tmp.year, tmp.month, tmp.day)
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def to_period(src):
    '''
    args:
        1. src: string, i.e.'3M'
    return:
        dqproto.Period
    '''
    try:
        if src=='':
            raise Exception('to_period: empty input')
            
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
        
###############################################################################
def to_calendar_name_list(cal_list):
    '''
    args:
        1. cal_list: list of string, i.e.['cal_cfets', 'cal_target']
    return:
        dqproto.CalendarNameList
    '''
    pb_cals = list()
    for cal in cal_list:
        if cal != '' and cal !='nan':
            pb_cals.append(CalendarName.DESCRIPTOR.values_by_name[cal.upper()].number)
    p_calendar_list = dqCreateProtoCalendarNameList(pb_cals)
    return p_calendar_list
        
###############################################################################
def to_currency_pair(ccy_pair):
    '''
    args:
        1. ccy_pair: string, i.e.'3M'
    return:
        dqproto.CurrencyPair
    '''
    try:
        left = ccy_pair[0:3]
        right = ccy_pair[3:6]
        left = dqCreateProtoCurrency(CurrencyName.DESCRIPTOR.values_by_name[left.upper()].number)
        right = dqCreateProtoCurrency(CurrencyName.DESCRIPTOR.values_by_name[right.upper()].number)
        
        return dqCreateProtoCurrencyPair(left, right)
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
#def fx_price_calculator(price_value, price_ccy, tgt_ccy):
#    '''
#    
#    '''
#    ccy_pair = price_ccy + tgt_ccy
#    if ccy_pair_manager.get_quote_type(ccy_pair) == 'primary':        
#        fx_rate = fx_mkt_data_manager.get_fx_spot_rate(as_of_date, ccy_pair)
#        fx_value = fx_rate * price
#    else:#derived:
#        if ccy_pair_manager.get_relationship(ccy_pair) == 'inverse':
#            fx_rate = fx_mkt_data_manager.get_fx_spot_rate(as_of_date, ccy_pair)
#        else:#triangle
#            primary_pairs = ccy_pair_manager.get_dependency(ccy_pair)
            