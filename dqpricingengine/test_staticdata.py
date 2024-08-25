# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 17:39:30 2021

@author: dzhu
"""

from staticdata import *

def test_load_src_static_data():
    res = load_src_static_data('calendar', 'cal_cfets')
    test = True
    print(test)

###############################################################################
def test_create_calendar():
    data = load_src_static_data('calendar', 'cal_cfets')
    res = create_calendar('cal_cfets', 
                          list(data['cal_cfets']), 
                          True, 
                          'staticdata/calendar')
    
    expected = b'\n\x85\x06\x08+\x12\x80\x06\xbb\xc2\x02\xbc\xc2\x02\xbd\xc2\x02\xe4\xc2\x02\xe5\xc2\x02\xe6\xc2\x02\xe7\xc2\x02\xe8\xc2\x02\x98\xc3\x02\x99\xc3\x02\xb1\xc3\x02\xb2\xc3\x02\xb3\xc3\x02\xdb\xc3\x02\xdc\xc3\x02\xdd\xc3\x02\xc0\xc4\x02\xc1\xc4\x02\xcc\xc4\x02\xcd\xc4\x02\xce\xc4\x02\xcf\xc4\x02\xd2\xc4\x02\xa8\xc5\x02\xc6\xc5\x02\xc9\xc5\x02\xca\xc5\x02\xcb\xc5\x02\xcc\xc5\x02\x88\xc6\x02\xa0\xc6\x02\xa1\xc6\x02\xc0\xc6\x02\xa2\xc7\x02\xb9\xc7\x02\xba\xc7\x02\xbb\xc7\x02\xbe\xc7\x02\xbf\xc7\x02\x95\xc8\x02\x96\xc8\x02\xc5\xc8\x02\xc6\xc8\x02\xc7\xc8\x02\xca\xc8\x02\xcb\xc8\x02\xf4\xc8\x02\x8d\xc9\x02\xc1\xc9\x02\x8a\xca\x02\x8b\xca\x02\xa6\xca\x02\xa7\xca\x02\xaa\xca\x02\xab\xca\x02\xac\xca\x02\x82\xcb\x02\xa8\xcb\x02\xa9\xcb\x02\xaa\xcb\x02\xab\xcb\x02\xac\xcb\x02\xe0\xcb\x02\xfc\xcb\x02\xa2\xcc\x02\xa3\xcc\x02\x84\xcd\x02\x85\xcd\x02\x96\xcd\x02\x97\xcd\x02\x98\xcd\x02\x99\xcd\x02\x9a\xcd\x02\xf1\xcd\x02\x8a\xce\x02\x8d\xce\x02\x8e\xce\x02\x8f\xce\x02\x90\xce\x02\xcc\xce\x02\xcd\xce\x02\xe8\xce\x02\x84\xcf\x02\x85\xcf\x02\x82\xd0\x02\x83\xd0\x02\x84\xd0\x02\x85\xd0\x02\x86\xd0\x02\xdd\xd0\x02\x8a\xd1\x02\x8b\xd1\x02\x8e\xd1\x02\x8f\xd1\x02\x90\xd1\x02\xbb\xd1\x02\xbc\xd1\x02\xd4\xd1\x02\xd5\xd1\x02\x85\xd2\x02\xe7\xd2\x02\xee\xd2\x02\xef\xd2\x02\xf0\xd2\x02\xf1\xd2\x02\xf2\xd2\x02\xca\xd3\x02\xec\xd3\x02\xed\xd3\x02\xee\xd3\x02\xef\xd3\x02\xf0\xd3\x02\xf1\xd3\x02\xf2\xd3\x02\xa8\xd4\x02\xc2\xd4\x02\xc3\xd4\x02\xc4\xd4\x02\xe7\xd4\x02\xc9\xd5\x02\xdb\xd5\x02\xdc\xd5\x02\xdd\xd5\x02\xde\xd5\x02\xdf\xd5\x02\xe0\xd5\x02\xe1\xd5\x02\xb7\xd6\x02\xce\xd6\x02\xcf\xd6\x02\xd0\xd6\x02\xd1\xd6\x02\xd2\xd6\x02\xd3\xd6\x02\xd4\xd6\x02\x95\xd7\x02\x96\xd7\x02\x97\xd7\x02\xb0\xd7\x02\xb1\xd7\x02\xb2\xd7\x02\xb3\xd7\x02\xe7\xd7\x02\xe8\xd7\x02\xe9\xd7\x02\xc9\xd8\x02\xca\xd8\x02\xcb\xd8\x02\xcc\xd8\x02\xcd\xd8\x02\xce\xd8\x02\xcf\xd8\x02\xd0\xd8\x02\xa5\xd9\x02\xce\xd9\x02\xcf\xd9\x02\xd0\xd9\x02\xd1\xd9\x02\xd2\xd9\x02\xd3\xd9\x02\xd4\xd9\x02\x82\xda\x02\x9d\xda\x02\xc9\xda\x02\xac\xdb\x02\xb6\xdb\x02\xb7\xdb\x02\xb8\xdb\x02\xb9\xdb\x02\xba\xdb\x02\xbb\xdb\x02\xbc\xdb\x02\x92\xdc\x02\xb1\xdc\x02\xb2\xdc\x02\xb3\xdc\x02\xb4\xdc\x02\xb5\xdc\x02\xb6\xdc\x02\xb7\xdc\x02\xf0\xdc\x02\x8a\xdd\x02\xab\xdd\x02\x8e\xde\x02\xa3\xde\x02\xa4\xde\x02\xa5\xde\x02\xa6\xde\x02\xa7\xde\x02\xa8\xde\x02\xa9\xde\x02\xff\xde\x02\x93\xdf\x02\x94\xdf\x02\x95\xdf\x02\x96\xdf\x02\x97\xdf\x02\x98\xdf\x02\x99\xdf\x02\xdb\xdf\x02\xdc\xdf\x02\xdd\xdf\x02\xf7\xdf\x02\xab\xe0\x02\xac\xe0\x02\xad\xe0\x02\x8e\xe1\x02\x90\xe1\x02\x91\xe1\x02\x92\xe1\x02\x93\xe1\x02\x94\xe1\x02\x95\xe1\x02\x96\xe1\x02\xec\xe1\x02\x93\xe2\x02\x94\xe2\x02\x95\xe2\x02\x96\xe2\x02\x97\xe2\x02\x98\xe2\x02\x99\xe2\x02\xca\xe2\x02\xcb\xe2\x02\xe3\xe2\x02\xe4\xe2\x02\xe5\xe2\x02\x8d\xe3\x02\xf0\xe3\x02\xf1\xe3\x02\xfe\xe3\x02\xff\xe3\x02\x80\xe4\x02\x81\xe4\x02\x82\xe4\x02\x83\xe4\x02\x84\xe4\x02\xda\xe4\x02\xf6\xe4\x02\xf7\xe4\x02\xf8\xe4\x02\xf9\xe4\x02\xfa\xe4\x02\xfb\xe4\x02\xfc\xe4\x02\xb7\xe5\x02\xd2\xe5\x02\xf0\xe5\x02\xeb\xe6\x02\xec\xe6\x02\xed\xe6\x02\xee\xe6\x02\xef\xe6\x02\xf0\xe6\x02\xf1\xe6\x02\xf2\xe6\x02'
    test = (res.SerializeToString() == expected)
    print(test)

###############################################################################    
def test_create_calendar_data():
    res = create_calendar_data(['cal_cfets'],
                               True, 
                               'staticdata/calendar')
    print(res)

###############################################################################    
def test_create_ibor_index():
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
    res = create_ibor_index(index_type,
                            index_name,
                            index_tenor,
                            index_ccy,
                            start_delay,
                            calendar_list,
                            day_count,
                            interest_day_convention,
                            date_roll_convention,
                            ibor_type,
                            save,
                            loc)
    
    expected = b'\n\x1d\x08\x02\x10\xcd\x01\x1a\x04\x08\x01\x10\x07 \x9c\x01*\x04\x08\x01\x10\x012\x03\n\x01+8\x02@\x02'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################    
def test_create_ibor_index_data():
    res = create_ibor_index_data(True,
                                 'staticdata/interestrate/index')
    print(res)
   
############################################################################### 
def test_create_leg_definition():
    leg_type = 'fixed_leg'
    currency='cny'
    day_count='act_365_fixed'
    ref_index = 'invalid_ibor_index_name'
    payment_discount_method = 'no_discount'
    rate_calc_method = 'standard'                          
    notional_exchange = 'initial_final_exchange'
    spread = False
    fx_convert = False
    fx_reset = False
    calendar ='cal_cfets'
    freq = 'annual'
    interest_day_convention ='modified_following'
    stub_policy = 'initial'
    broken_period_type = 'long'
    pay_day_offset = '0d'
    pay_day_convention = 'modified_following'
    fixing_calendars = ['cal_cfets']
    fixing_freq = 'invalid_frequency'
    fixing_day_convention = 'invalid_business_day_convention'
    fixing_mode = 'invalid_date_generation_mode'
    fixing_day_offset = '0d'
    res = create_leg_definition(leg_type,
                                currency,
                                day_count,
                                ref_index,
                                payment_discount_method,
                                rate_calc_method,                          
                                notional_exchange,
                                spread,
                                fx_convert,
                                fx_reset,
                                calendar,
                                freq,
                                interest_day_convention,
                                stub_policy,
                                broken_period_type,
                                pay_day_offset,
                                pay_day_convention,
                                fixing_calendars,
                                fixing_freq,
                                fixing_day_convention,
                                fixing_mode,
                                fixing_day_offset)
    
    expected = b'\x08\x01\x10\x9c\x01\x18\x02(\x010\x018\x01@\x01H\x05j7\n\x0f\x08\x01\x1a\x03\n\x01+ \x01(\x020\x018\x02\x12\x17\x08\x03\x10\x01\x1a\x03\n\x01+ \x01(\x020\x028\x01B\x02\x10\x01H\x02\x1a\x0b\x1a\x03\n\x01+8\x01B\x02\x10\x01'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################    
def test_create_fixed_cpn_bond_template():
    inst_name = 'CNY_TREAS_20_CPN_07'
    issue_date = '2020-05-22'
    settlement_days = 1
    start_date = '2020-05-25'
    maturity = '2070-05-25'
    cpn_rate = 3.73e-2
    currency = 'CNY'
    day_count_convention = 'ACT_365_FIXED'
    calendar = 'cal_cfets'
    frequency = 'SEMIANNUAL'
    interest_day_convention = 'FOLLOWING'
    stub_policy = 'INITIAL'
    broken_period_type = 'LONG'
    pay_day_offset = '0d'
    pay_day_convention = 'FOLLOWING'
    ex_cpn_period = '0d'
    ex_cpn_calendar = 'cal_cfets'
    ex_cpn_day_convention = 'FOLLOWING'
    ex_cpn_eom = False
    save = True
    loc = 'staticdata/fixedincome/bond'
                                   
    res = create_fixed_cpn_bond_template(inst_name,
                                         issue_date,
                                         settlement_days,
                                         start_date,
                                         maturity,
                                         cpn_rate,
                                         currency,
                                         day_count_convention,
                                         calendar,
                                         frequency,
                                         interest_day_convention,
                                         stub_policy,
                                         broken_period_type,
                                         pay_day_offset,
                                         pay_day_convention,
                                         ex_cpn_period,
                                         ex_cpn_calendar,
                                         ex_cpn_day_convention,
                                         ex_cpn_eom,
                                         save,
                                         loc)
    expected = b'\n\x92\x01\n\x13CNY_TREAS_20_CPN_07\x18\x01"J\x08\x01\x10\x9c\x01\x18\x02(\x010\x018\x01@\x01H\x05j7\n\x0f\x08\x01\x1a\x03\n\x01+ \x02(\x010\x018\x02\x12\x17\x08\x03\x10\x01\x1a\x03\n\x01+ \x02(\x010\x028\x01B\x02\x10\x01H\x02\x1a\x0b\x1a\x03\n\x01+8\x01B\x02\x10\x01*\x02\x10\x012\x03\n\x01+8\x01J\x07\x08\xe4\x0f\x10\x05\x18\x16Q\xf0\x16HP\xfc\x18\xa3?b\x07\x08\x96\x10\x10\x05\x18\x19j\x07\x08\xe4\x0f\x10\x05\x18\x19'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################   
def test_create_zero_cpn_bond_template():
    inst_name = 'CNY_TREAS_21_DSCNT_23'
    issue_date = '2021-05-21'
    settlement_days = 1
    start_date = '2021-05-24'
    maturity = '2021-08-23'
    currency = 'CNY'
    day_count_convention = 'ACT_365_FIXED'
    calendar = 'cal_cfets'
    pay_day_convention = 'FOLLOWING'
    save = True
    loc = 'staticdata/fixedincome/bond'                         
    
    res = create_zero_cpn_bond_template(inst_name,
                                        issue_date,
                                        settlement_days,
                                        start_date,
                                        maturity,
                                        currency,
                                        day_count_convention,
                                        calendar,
                                        pay_day_convention,
                                        save,
                                        loc)
    expected = b'\n\x87\x01\n\x15CNY_TREAS_21_DSCNT_23\x18\x01"H\x08\x01\x10\x9c\x01\x18\x02(\x010\x018\x01@\x01H\x05j5\n\x0c\x08\x01\x1a\x03\n\x01+ \xe7\x07(\x01\x12\x18\x08\x03\x10\x01\x1a\x03\n\x01+ \xe7\x07(\x010\x028\x01B\x02\x10\x01H\x02\x1a\x0b\x1a\x03\n\x01+8\x01B\x02\x10\x01*\x02\x10\x012\x03\n\x01+J\x07\x08\xe5\x0f\x10\x05\x18\x15b\x07\x08\xe5\x0f\x10\x08\x18\x17j\x07\x08\xe5\x0f\x10\x05\x18\x18'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_benchmark_fixed_cpn_bond_template():
    inst_name = 'CNY_TREAS_CPN_SA_30Y'
    settlement_days = 1
    cpn_rate = 3.73e-2
    currency = 'CNY'
    day_count_convention = 'ACT_365_FIXED'
    calendar = 'cal_cfets'
    frequency = 'SEMIANNUAL'
    interest_day_convention = 'FOLLOWING'
    stub_policy = 'INITIAL'
    broken_period_type = 'LONG'
    pay_day_offset = '0d'
    pay_day_convention = 'FOLLOWING'
    ex_cpn_period = '0d'
    ex_cpn_calendar = 'cal_cfets'
    ex_cpn_day_convention = 'FOLLOWING'
    ex_cpn_eom = False
    save = True
    loc = 'staticdata/fixedincome/bond'
                                   
    res = create_benchmark_fixed_cpn_bond_template(inst_name,
                                                   settlement_days,
                                                   cpn_rate,
                                                   currency,
                                                   day_count_convention,
                                                   calendar,
                                                   frequency,
                                                   interest_day_convention,
                                                   stub_policy,
                                                   broken_period_type,
                                                   pay_day_offset,
                                                   pay_day_convention,
                                                   ex_cpn_period,
                                                   ex_cpn_calendar,
                                                   ex_cpn_day_convention,
                                                   ex_cpn_eom,
                                                   save,
                                                   loc)
    expected = b'\n\x93\x01\n\x14CNY_TREAS_CPN_SA_30Y\x18\x01"J\x08\x01\x10\x9c\x01\x18\x02(\x010\x018\x01@\x01H\x05j7\n\x0f\x08\x01\x1a\x03\n\x01+ \x02(\x010\x018\x02\x12\x17\x08\x03\x10\x01\x1a\x03\n\x01+ \x02(\x010\x028\x01B\x02\x10\x01H\x02\x1a\x0b\x1a\x03\n\x01+8\x01B\x02\x10\x01*\x02\x10\x012\x03\n\x01+8\x01J\x07\x08\xeb\x0e\x10\x0c\x18\x1eQ\xf0\x16HP\xfc\x18\xa3?b\x07\x08\xeb\x0e\x10\x0c\x18\x1ej\x07\x08\xeb\x0e\x10\x0c\x18\x1e'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_benchmark_zero_cpn_bond_template():
    inst_name = 'CNY_TREAS_ZERO_1M'
    settlement_days = 1
    currency = 'CNY'
    day_count_convention = 'ACT_365_FIXED'
    calendar = 'cal_cfets'
    pay_day_convention = 'FOLLOWING'
    save = True
    loc = 'staticdata/fixedincome/bond'                         
    
    res = create_benchmark_zero_cpn_bond_template(inst_name,
                                                  settlement_days,
                                                  currency,
                                                  day_count_convention,
                                                  calendar,
                                                  pay_day_convention,
                                                  save,
                                                  loc)
    expected = b'\n\x83\x01\n\x11CNY_TREAS_ZERO_1M\x18\x01"H\x08\x01\x10\x9c\x01\x18\x02(\x010\x018\x01@\x01H\x05j5\n\x0c\x08\x01\x1a\x03\n\x01+ \xe7\x07(\x01\x12\x18\x08\x03\x10\x01\x1a\x03\n\x01+ \xe7\x07(\x010\x028\x01B\x02\x10\x01H\x02\x1a\x0b\x1a\x03\n\x01+8\x01B\x02\x10\x01*\x02\x10\x012\x03\n\x01+J\x07\x08\xeb\x0e\x10\x0c\x18\x1eb\x07\x08\xeb\x0e\x10\x0c\x18\x1ej\x07\x08\xeb\x0e\x10\x0c\x18\x1e'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_vanilla_bond_template_data():
    save = True
    loc = 'staticdata/fixedincome/bond'    
    res =create_vanilla_bond_template_data(save, loc)
    print(res)
    
###############################################################################
def test_create_benchmark_vanilla_bond_template_data():
    save = True
    loc = 'staticdata/fixedincome/bond'    
    res =create_benchmark_vanilla_bond_template_data(save, loc)
    print(res)
    
###############################################################################
def test_create_deposit_template():
    inst_name = 'CNY_FR_007'
    start_delay = '1D'
    currency = 'CNY'
    day_count_convention = 'ACT_365_FIXED'
    calendar = 'cal_cfets'
    interest_day_convention = 'MODIFIED_FOLLOWING'
    pay_day_offset='0d'
    pay_day_convention = 'MODIFIED_FOLLOWING'
    inst_start_convention= 'SPOT_START'
    save = True
    loc = 'staticdata/interestrate/instrument/deposit'      
    res = create_deposit_template(inst_name,
                                  start_delay,
                                  currency,
                                  day_count_convention,
                                  calendar,
                                  interest_day_convention,
                                  pay_day_offset,
                                  pay_day_convention, 
                                  inst_start_convention,
                                  save,
                                  loc)
    expected = b'\ne\x08\xe9\x07\x12\nCNY_FR_007\x1a\x04\x08\x01\x10\x01"L\x08\x01\x10\x9c\x01\x18\x02(\x010\x018\x01@\x01H\x05j9\n\x10\x08\x01\x1a\x03\n\x01+ \xe7\x07(\x020\x018\x02\x12\x18\x08\x03\x10\x01\x1a\x03\n\x01+ \xe7\x07(\x020\x028\x01B\x02\x10\x01H\x02\x1a\x0b\x1a\x03\n\x01+8\x01B\x02\x10\x01(\x01'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_deposit_template_data():
    save = True
    loc = 'staticdata/interestrate/instrument/deposit'      
    res =create_deposit_template_data(save, loc)
    print(res)
    
###############################################################################
def test_create_ir_vanilla_swap_template():
    inst_name = 'cny_fr_007'
    start_delay = '1d'
    currency = 'cny'
    leg1_type = 'fixed_leg'
    leg1_day_count = 'act_365_fixed'
    leg1_ref_index = 'invalid_ibor_index_name'
    leg1_rate_calc_method = 'standard'
    leg1_spread = False
    leg1_calendar = 'cal_cfets'
    leg1_freq = 'quarterly'
    leg1_interest_day_convention = 'modified_following'
    leg1_stub_policy = 'initial'
    leg1_broken_period_type = 'long'
    leg1_pay_day_offset = '0d'
    leg1_pay_day_convention = 'modified_following'
    leg1_fixing_calendars = ['invalid_calendar_name']
    leg1_fixing_freq = 'invalid_frequency'
    leg1_fixing_day_convention = 'invalid_business_day_convention'
    leg1_fixing_mode = 'invalid_date_generation_mode'
    leg1_fixing_day_offset = '0d'
    leg2_type = 'floating_leg'
    leg2_day_count = 'act_365_fixed'
    leg2_ref_index = 'fr_007'
    leg2_rate_calc_method = 'compound_average'
    leg2_spread = False
    leg2_calendar = 'cal_cfets'
    leg2_freq = 'quarterly'
    leg2_interest_day_convention = 'modified_following'
    leg2_stub_policy = 'initial'
    leg2_broken_period_type = 'long'
    leg2_pay_day_offset = '0d'
    leg2_pay_day_convention = 'modified_following'
    leg2_fixing_calendars = ['cal_cfets']
    leg2_fixing_freq = 'weekly'
    leg2_fixing_day_convention = 'modified_preceding'
    leg2_fixing_mode = 'in_advance'
    leg2_fixing_day_offset = '-1d'
    start_convention = 'spot_start'
    save = True
    loc = 'staticdata/interestrate/instrument/ir_vanilla_swap'      
    res = create_ir_vanilla_swap_template(inst_name,
                                          start_delay,
                                          currency,
                                          leg1_type,
                                          leg1_day_count,
                                          leg1_ref_index,
                                          leg1_rate_calc_method,
                                          leg1_spread,
                                          leg1_calendar,
                                          leg1_freq,
                                          leg1_interest_day_convention,
                                          leg1_stub_policy,
                                          leg1_broken_period_type,
                                          leg1_pay_day_offset,
                                          leg1_pay_day_convention,
                                          leg1_fixing_calendars,
                                          leg1_fixing_freq,
                                          leg1_fixing_day_convention,
                                          leg1_fixing_mode,
                                          leg1_fixing_day_offset,
                                          leg2_type,
                                          leg2_day_count,
                                          leg2_ref_index,
                                          leg2_rate_calc_method,
                                          leg2_spread,
                                          leg2_calendar,
                                          leg2_freq,
                                          leg2_interest_day_convention,
                                          leg2_stub_policy,
                                          leg2_broken_period_type,
                                          leg2_pay_day_offset,
                                          leg2_pay_day_convention,
                                          leg2_fixing_calendars,
                                          leg2_fixing_freq,
                                          leg2_fixing_day_convention,
                                          leg2_fixing_mode,
                                          leg2_fixing_day_offset,
                                          start_convention,
                                          save,
                                          loc)
    expected = b'\n\xbf\x01\x08\xd2\x0f\x12\ncny_fr_007\x1a\x04\x08\x01\x10\x01"H\x08\x01\x10\x9c\x01\x18\x02(\x010\x018\x01@\x01j7\n\x0f\x08\x01\x1a\x03\n\x01+ \x04(\x020\x018\x02\x12\x17\x08\x03\x10\x01\x1a\x03\n\x01+ \x04(\x020\x028\x01B\x02\x10\x01H\x02\x1a\x0b\x1a\x03\n\x01\x008\x01B\x02\x10\x01"\\\x08\x02\x10\x9c\x01\x18\x02 \xcd\x01(\x010\x018\x02@\x01jH\n\x0f\x08\x01\x1a\x03\n\x01+ \x04(\x020\x018\x02\x12\x17\x08\x03\x10\x01\x1a\x03\n\x01+ \x04(\x020\x028\x01B\x02\x10\x01H\x02\x1a\x1c\x1a\x03\n\x01+ 4(\x040\x018\x01B\r\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x01(\x01'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_ir_vanilla_swap_template_data():
    save = True
    loc = 'staticdata/interestrate/instrument/ir_vanilla_swap'      
    res = create_ir_vanilla_swap_template_data(save, loc)
    print(res)
   
###############################################################################
def test_create_fx_spot_template():
    inst_name='usdcny'
    currency_pair='usdcny'
    spot_day_convention='following'
    calendars=['cal_cfets']
    spot_delay='1d'
    save = True
    loc = 'staticdata/foreignexchange/instrument/fx_spot'      
    res = create_fx_spot_template(inst_name,
                                  currency_pair,
                                  spot_day_convention,
                                  calendars,
                                  spot_delay,
                                  save,
                                  loc)
    expected = b'\n$\x08\xb9\x17\x12\x06usdcny\x1a\n\n\x03\x08\xc8\x06\x12\x03\x08\x9c\x01 \x01*\x03\n\x01+2\x04\x08\x01\x10\x01'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_fx_spot_template_data():
    save = True
    loc = 'staticdata/foreignexchange/instrument/fx_spot'       
    res = create_fx_spot_template_data(save, loc)
    print(res)
    
###############################################################################
def test_create_fx_forward_template():
    inst_name='usdcny'
    currency_pair='usdcny'
    delivery_day_convention='following'
    calendars=['cal_cfets']
    fixing_offset='-1d'
    fixing_day_convention='preceding'
    save = True
    loc = 'staticdata/foreignexchange/instrument/fx_forward'      
    res = create_fx_forward_template(inst_name,
                                     currency_pair,
                                     delivery_day_convention,
                                     fixing_offset,
                                     fixing_day_convention,
                                     calendars,
                                     save,
                                     loc)
    expected = b'\n/\x08\xba\x17\x12\x06usdcny\x1a\r\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x01"\n\n\x03\x08\xc8\x06\x12\x03\x08\x9c\x01(\x010\x03:\x03\n\x01+'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_fx_forward_template_data():
    save = True
    loc = 'staticdata/foreignexchange/instrument/fx_forward'       
    res = create_fx_forward_template_data(save, loc)
    print(res)
   
###############################################################################
def test_create_fx_swap_template():
    inst_name='usdcny'
    currency_pair='usdcny'
    start_day_convention='following'
    end_day_convention='following'
    calendars=['cal_cfets']
    fixing_offset='-1d'
    fixing_day_convention='preceding'
    start_convention = 'SPOT_START'
    save = True
    loc = 'staticdata/foreignexchange/instrument/fx_swap'      
    res = create_fx_swap_template(inst_name,
                                  currency_pair,
                                  start_day_convention,
                                  end_day_convention,
                                  fixing_offset,
                                  fixing_day_convention,
                                  calendars,
                                  start_convention,
                                  save,
                                  loc)
    expected = b'\n3\x08\xbc\x17\x12\x06usdcny\x18\x01"\n\n\x03\x08\xc8\x06\x12\x03\x08\x9c\x01*\x03\n\x01+0\x018\x01B\r\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x01H\x03'
    test = (res.SerializeToString() == expected)    
    print(test)

###############################################################################
def test_create_fx_swap_template_data():
    save = True
    loc = 'staticdata/foreignexchange/instrument/fx_swap'       
    res = create_fx_swap_template_data(save, loc)
    print(res)

###############################################################################
#
print('test_load_src_static_data:')
test_load_src_static_data()
#
print('test_create_calendar:')
test_create_calendar()
#
print('test_create_calendar_data:')
test_create_calendar_data()
#
print('test_create_ibor_index:')
test_create_ibor_index()
#
print('test_create_ibor_index_data:')
test_create_ibor_index_data()
#
print('test_create_leg_definition:')
test_create_leg_definition()
#
print('test_create_fixed_cpn_bond_template:')
test_create_fixed_cpn_bond_template()
#
print('test_create_zero_cpn_bond_template:')
test_create_zero_cpn_bond_template()
#
print('test_create_benchmark_fixed_cpn_bond_template:')
test_create_benchmark_fixed_cpn_bond_template()
#
print('test_create_benchmark_zero_cpn_bond_template:')
test_create_benchmark_zero_cpn_bond_template()
#
print('test_create_vanilla_bond_template_data:')
test_create_vanilla_bond_template_data()
#
print('test_create_benchmark_vanilla_bond_template_data:')
test_create_benchmark_vanilla_bond_template_data()
#
print('test_create_deposit_template:')
test_create_deposit_template()
#
print('test_create_deposit_template_data:')
test_create_deposit_template_data()
#
print('test_create_ir_vanilla_swap_template:')
test_create_ir_vanilla_swap_template()
#
print('test_create_ir_vanilla_swap_template_data:')
test_create_ir_vanilla_swap_template_data()
#
print('test_create_fx_spot_template:')
test_create_fx_spot_template()
#
print('test_create_fx_spot_template_data:')
test_create_fx_spot_template_data()
#
print('test_create_fx_forward_template:')
test_create_fx_forward_template()
#
print('test_create_fx_forward_template_data:')
test_create_fx_forward_template_data()
#
print('test_create_fx_swap_template:')
test_create_fx_swap_template()
#
print('test_create_fx_swap_template_data:')
test_create_fx_swap_template_data()