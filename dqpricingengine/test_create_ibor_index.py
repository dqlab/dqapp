# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 15:23:17 2021

@author: dzhu
"""

index_type = 'ibor_index'
index_name = 'fr_007'
index_tenor = '1w'
index_ccy = 'cny'
start_delay = '1d'
calendar_list = ['cal_cfets']
day_count = 'act_365_fixed'
interest_day_convention = 'modified_following'
date_roll_convention = 'invalid_date_roll_convention'
ibor_type = 'standard_ibor_index'
save = True
loc = 'staticdata/interestrate/index'

pb_data = dqCreateProtoIborIndex(InterestRateIndexType.DESCRIPTOR.values_by_name[index_type.upper()].number, 
                                 IborIndexName.DESCRIPTOR.values_by_name[index_name.upper()].number,  
                                 to_period(index_tenor), 
                                 CurrencyName.DESCRIPTOR.values_by_name[index_ccy.upper()].number, 
                                 to_period(start_delay), 
                                 to_calendar_name_list(calendar_list), 
                                 DayCountConvention.DESCRIPTOR.values_by_name[day_count.upper()].number, 
                                 BusinessDayConvention.DESCRIPTOR.values_by_name[interest_day_convention.upper()].number, 
                                 DateRollConvention.DESCRIPTOR.values_by_name[date_roll_convention.upper()].number, 
                                 IborIndexType.DESCRIPTOR.values_by_name[ibor_type.upper()].number)
        
pb_data_list = dqCreateProtoIborIndexList([pb_data])

data_type='SDT_IBOR_INDEX'

tmp_file = 'dqlib/tmp.bin'
tmp = open(tmp_file,'wb')
tmp.write(pb_data_list.SerializeToString())
tmp.close()

pb_input = dqCreateProtoCreateStaticDataInput(StaticDataType.DESCRIPTOR.values_by_name[data_type.upper()].number,
                                              tmp_file)

req_name = 'CREATE_STATIC_DATA'
res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
pb_output = CreateStaticDataOutput()
pb_output.ParseFromString(res_msg)
print(pb_output)
