# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:14:52 2021

@author: dzhu
"""

import sys
import pandas as pd

from dqproto import *
from irmarket import create_leg_definition
from utility import to_calendar_name_list, to_date, to_period
from utility import save_pb_data
from staticdata import create_static_data, load_src_static_data

###############################################################################
def create_fixed_cpn_bond_template(inst_name,
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
                                   loc):
    '''
    @args:
       1. inst_name: string
       1. issue_date: string
       2. settlement_days: int
       3. start_date: string
       4. maturity: string
       5. cpn_rate: double
       6. currency: string 
       7. day_count_convention: string
       8. calendar: string
       9. frequency: string
       10. interest_day_convention: string
       11. stub_policy: string
       12. broken_period_type: string
       13. pay_day_offset: string
       14. pay_day_convention: string
       15. ex_cpn_period: string
       16. ex_cpn_calendar: string
       17. ex_cpn_day_convention: string
       18. ex_cpn_eom: boolean
       19. save: boolean
       20. loc: string
    @return:
        
    ''' 
    leg_type = 'FIXED_LEG'
    ref_index = 'INVALID_IBOR_INDEX_NAME'
    payment_discount_method = 'NO_DISCOUNT'        
    interest_rate_calculation_method = 'STANDARD'
    notional_exchange = 'INITIAL_FINAL_EXCHANGE'
    spread = False
    fx_convert = False
    fx_reset = False 
    fixing_calendars = [calendar]
    fixing_freq = 'INVALID_FREQUENCY'
    fixing_day_convention = 'INVALID_BUSINESS_DAY_CONVENTION'
    fixing_mode = 'INVALID_DATE_GENERATION_MODE'
    fixing_day_offset = '0d'
           
    leg_definition = create_leg_definition(leg_type,
                                           currency,
                                           day_count_convention,
                                           ref_index,
                                           payment_discount_method,
                                           interest_rate_calculation_method,                          
                                           notional_exchange,
                                           spread,
                                           fx_convert,
                                           fx_reset,
                                           calendar,
                                           frequency,
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
    
    vanilla_bond_type = FIXED_COUPON_BOND
    pb_data = dqCreateProtoVanillaBondTemplate(inst_name,
                                               vanilla_bond_type,
                                               settlement_days,
                                               leg_definition,
                                               to_period(ex_cpn_period),
                                               to_calendar_name_list([ex_cpn_calendar]),
                                               BusinessDayConvention.DESCRIPTOR.values_by_name[ex_cpn_day_convention.upper()].number,
                                               ex_cpn_eom,
                                               to_date(issue_date, '%Y-%m-%d'),
                                               cpn_rate,
                                               0.0,
                                               to_date(maturity, '%Y-%m-%d'),
                                               to_date(start_date, '%Y-%m-%d'))
    
    pb_data_list = dqCreateProtoVanillaBondTemplateList([pb_data])
    create_static_data('SDT_VANILLA_BOND', pb_data_list)
    
    if save:
        save_pb_data(pb_data_list, inst_name, loc)

    return pb_data_list    

###############################################################################
def create_zero_cpn_bond_template(inst_name,
                                  issue_date,
                                  settlement_days,
                                  start_date,
                                  maturity,
                                  currency,
                                  day_count_convention,
                                  calendar,
                                  pay_day_convention,
                                  save,
                                  loc):
    '''
    @args:
       
    @return:
        
    '''   
    cpn_rate= 0.0                                   
    frequency='once'
    interest_day_convention = pay_day_convention
    stub_policy = ''
    broken_period_type = ''
    pay_day_offset = '0d'
    ex_cpn_period = '0d'
    ex_cpn_calendar = calendar
    ex_cpn_day_convention = 'invalid_business_day_convention'
    ex_cpn_eom = False
    
    leg_type = 'FIXED_LEG'
    ref_index = 'INVALID_IBOR_INDEX_NAME'
    payment_discount_method = 'NO_DISCOUNT'        
    interest_rate_calculation_method = 'STANDARD'
    notional_exchange = 'INITIAL_FINAL_EXCHANGE'
    spread = False
    fx_convert = False
    fx_reset = False 
    fixing_calendars = [calendar]
    fixing_freq = 'INVALID_FREQUENCY'
    fixing_day_convention = 'INVALID_BUSINESS_DAY_CONVENTION'
    fixing_mode = 'INVALID_DATE_GENERATION_MODE'
    fixing_day_offset = '0d'
           
    leg_definition = create_leg_definition(leg_type,
                                           currency,
                                           day_count_convention,
                                           ref_index,
                                           payment_discount_method,
                                           interest_rate_calculation_method,                          
                                           notional_exchange,
                                           spread,
                                           fx_convert,
                                           fx_reset,
                                           calendar,
                                           frequency,
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
    
    
    vanilla_bond_type = ZERO_COUPON_BOND
    pb_data = dqCreateProtoVanillaBondTemplate(inst_name,
                                               vanilla_bond_type,
                                               settlement_days,
                                               leg_definition,
                                               to_period(ex_cpn_period),
                                               to_calendar_name_list([ex_cpn_calendar]),
                                               BusinessDayConvention.DESCRIPTOR.values_by_name[ex_cpn_day_convention.upper()].number,
                                               ex_cpn_eom,
                                               to_date(issue_date, '%Y-%m-%d'),
                                               cpn_rate,
                                               0.0,
                                               to_date(maturity, '%Y-%m-%d'),
                                               to_date(start_date, '%Y-%m-%d'))
    
    pb_data_list = dqCreateProtoVanillaBondTemplateList([pb_data])
    create_static_data('SDT_VANILLA_BOND', pb_data_list)
    
    if save:
        save_pb_data(pb_data_list, inst_name, loc)

    return pb_data_list       
###############################################################################
def create_benchmark_fixed_cpn_bond_template(inst_name,
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
                                             loc):
    '''
    @args:
        1. inst_name: string
       1. issue_date: string
       2. settlement_days: int
       3. start_date: string
       4. maturity: string
       5. cpn_rate: double
       6. currency: string 
       7. day_count_convention: string
       8. calendar: string
       9. frequency: string
       10. interest_day_convention: string
       11. stub_policy: string
       12. broken_period_type: string
       13. pay_day_offset: int
       14. pay_day_convention: string
       15. ex_cpn_period: string
       16. ex_cpn_calendar: string
       17. ex_cpn_day_convention: string
       18. ex_cpn_eom: boolean
       19. save: boolean
       20. loc: string
    @return:
        
    ''' 
    try:
        return create_fixed_cpn_bond_template(inst_name,
                                              '1899-12-30',
                                              settlement_days,
                                              '1899-12-30',
                                              '1899-12-30',
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
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
###############################################################################        
def create_benchmark_zero_cpn_bond_template(inst_name,
                                            settlement_days,
                                            currency,
                                            day_count_convention,
                                            calendar,
                                            pay_day_convention,
                                            save,
                                            loc):
    '''
    @args:
       
    @return:
        
    '''   
    try:    
        return create_zero_cpn_bond_template(inst_name,
                                             '1899-12-30',
                                             settlement_days,
                                             '1899-12-30',
                                             '1899-12-30',
                                             currency,
                                             day_count_convention,
                                             calendar,
                                             pay_day_convention,
                                             save,
                                             loc)
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))  
###############################################################################    
def create_vanilla_bond_template_data(save,
                                      loc):
    '''
    @args:
       
    @return:
        
    '''
    data = load_src_static_data('fixedincome/bond', 'vanilla_bond')
    for i in range(len(data)):       
        bond_type = data.iloc[i]['bond_type']        
        bond_name = data.iloc[i]['bond_name']
        issue_date = data.iloc[i]['issue_date']
        settlement_days = data.iloc[i]['settlement_days']
        start_date = data.iloc[i]['start_date']
        maturity = data.iloc[i]['maturity']        
        currency = data.iloc[i]['currency']
        day_count_convention = data.iloc[i]['day_count_convention']
        calendar = data.iloc[i]['calendar']        
        pay_day_convention = data.iloc[i]['pay_day_convention']        
                
        bond_type = bond_type.lower()
        if bond_type == 'zero_coupon_bond':
            create_zero_cpn_bond_template(bond_name,
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
        else:
            frequency = data.iloc[i]['frequency']            
            interest_day_convention = data.iloc[i]['interest_day_convention']
            pay_day_offset = data.iloc[i]['pay_day_offset']
            stub_policy = data.iloc[i]['stub_policy']
            broken_period_type = data.iloc[i]['broken_period_type']      
            ex_cpn_period = data.iloc[i]['excoupon_period']
            ex_cpn_calendar = data.iloc[i]['excoupon_calendar']
            ex_cpn_day_convention = data.iloc[i]['excoupon_day_convention']
            ex_cpn_eom = data.iloc[i]['excoupon_eom']
        
            if bond_type == 'fixed_coupon_bond':
                cpn_rate = data.iloc[i]['coupon_rate']
                create_fixed_cpn_bond_template(bond_name,
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
            else: #floating coupon bond
                print('create_floating_cpn_bond_template')
                
    return True
###############################################################################
def create_benchmark_vanilla_bond_template_data(save,
                                                loc):
    '''
    @args:
       
    @return:
        
    '''
    data = load_src_static_data('fixedincome/instrument/vanilla_bond', 'benchmark_bond')
    data.columns = data.columns.str.lower()
    for i in range(len(data)):       
        bond_type = data.iloc[i]['bond_type']        
        bond_id = data.iloc[i]['bond_id']
        settlement_days = data.iloc[i]['settlement_days']
        currency = data.iloc[i]['currency']
        day_count_convention = data.iloc[i]['day_count_convention']
        calendar = data.iloc[i]['calendar']        
        pay_day_convention = data.iloc[i]['pay_day_convention']        
        
        bond_type = bond_type.lower()
        if bond_type == 'zero_coupon_bond':
            create_benchmark_zero_cpn_bond_template(bond_id,                                          
                                                    settlement_days,
                                                    currency,
                                                    day_count_convention,
                                                    calendar,
                                                    pay_day_convention,
                                                    save,
                                                    loc)
        else:
            frequency = data.iloc[i]['frequency']  
            interest_day_convention = data.iloc[i]['interest_day_convention']
            pay_day_offset = data.iloc[i]['pay_day_offset']
            stub_policy = data.iloc[i]['stub_policy']
            broken_period_type = data.iloc[i]['broken_period_type']      
            ex_cpn_period = data.iloc[i]['excoupon_period']
            ex_cpn_calendar = data.iloc[i]['excoupon_calendar']
            ex_cpn_day_convention = data.iloc[i]['excoupon_day_convention']
            ex_cpn_eom = data.iloc[i]['excoupon_eom']
        
            if bond_type == 'fixed_coupon_bond':
                cpn_rate = data.iloc[i]['coupon_rate']
                create_benchmark_fixed_cpn_bond_template(bond_id,
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
            else:#floating coupon bond
                print('create_benchmark_floating_cpn_bond_template')
    
    return True    

###############################################################################
class VanillaBondTemplateManager:
    def __init__(self):
        self.vanilla_bond = load_src_static_data('fixedincome/instrument/vanilla_bond', 'vanilla_bond')
        self.vanilla_bond.columns = self.vanilla_bond.columns.str.lower()
        self.vanilla_bond = self.vanilla_bond.set_index('bond_id')    
            
    def get_discount_curve(self, bond_name):    
        return str(self.vanilla_bond.loc[bond_name]['discount_curve'])
    
    def get_sprd_curve(self, bond_name):    
        return str(self.vanilla_bond.loc[bond_name]['spread_curve'])

    def get_forward_curve(self, bond_name):    
        return str(self.vanilla_bond.loc[bond_name]['forward_curve'])

    def get_bond_type(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['bond_type'])
        if value == 'nan':
            value = ''
        return value
    
    def get_currency(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['currency'])
        if value == 'nan':
            value = ''
        return value
    
    def get_issue_date(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['issue_date'])
        if value == 'nan':
            value = ''
        return value
    
    def get_settlement_days(self, bond_name):
        return self.vanilla_bond.loc[bond_name]['settlement_days']
        
    def get_maturity(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['maturity'])
        if value == 'nan':
            value = ''
        return value

    def get_coupon_rate(self, bond_name):
        return self.vanilla_bond.loc[bond_name]['coupon_rate']
    
    def get_day_count_convention(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['day_count_convention'])
        if value == 'nan':
            value = ''
        return value
 
    def get_frequency(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['frequency'])
        if value == 'nan':
            value = ''
        return value
  
    def get_calendar(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['calendar'])
        if value == 'nan':
            value = ''
        return value
    
    def get_interest_day_convention(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['interest_day_convention'])
        if value == 'nan':
            value = ''
        return value
    
    def get_stub_policy(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['stub_policy'])
        if value == 'nan':
            value = ''
        return value
    
    def get_broken_period_type(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['broken_period_type'])
        if value == 'nan':
            value = ''
        return value
    
    def get_pay_day_convention(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['pay_day_convention'])
        if value == 'nan':
            value = ''
        return value
    
    def get_excoupon_period(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['excoupon_period'])
        if value == 'nan':
            value = ''
        return value
            
    def get_excoupon_calendar(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['excoupon_calendar'])
        if value == 'nan':
            value = ''
        return value
    
    def get_excoupon_day_convention(self, bond_name):
        value = str(self.vanilla_bond.loc[bond_name]['excoupon_day_convention'])
        if value == 'nan':
            value = ''
        return value
    
    def get_excoupon_eom(self, bond_name):
        return bool(self.vanilla_bond.loc[bond_name]['excoupon_eom'])
        
###############################################################################
class BenchmarkBondTemplateManager:
    def __init__(self):
        self.benchmark_bond = load_src_static_data('fixedincome/instrument/vanilla_bond', 'benchmark_bond')
        self.benchmark_bond.columns = self.benchmark_bond.columns.str.lower()
        self.benchmark_bond = self.benchmark_bond.set_index('bond_id')    
        #load benchmark bond definition into engine cache:
        create_benchmark_vanilla_bond_template_data(False, '')
    
    def get_discount_curve(self, bond_name):    
        return str(self.benchmark_bond.loc[bond_name]['discount_curve'])
    
    def get_sprd_curve(self, bond_name):    
        return str(self.benchmark_bond.loc[bond_name]['spread_curve'])

    def get_forward_curve(self, bond_name):    
        return str(self.benchmark_bond.loc[bond_name]['forward_curve'])

    def get_bond_type(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['bond_type'])
        if value == 'nan':
            value = ''
        return value
    
    def get_currency(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['currency'])
        if value == 'nan':
            value = ''
        return value
    
    def get_settlement_days(self, bond_name):
        return self.benchmark_bond.loc[bond_name]['settlement_days']
            
    def get_coupon_rate(self, bond_name):
        return self.benchmark_bond.loc[bond_name]['coupon_rate']
    
    def get_day_count_convention(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['day_count_convention'])
        if value == 'nan':
            value = ''
        return value
 
    def get_frequency(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['frequency'])
        if value == 'nan':
            value = ''
        return value
  
    def get_calendar(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['calendar'])
        if value == 'nan':
            value = ''
        return value
    
    def get_interest_day_convention(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['interest_day_convention'])
        if value == 'nan':
            value = ''
        return value
    
    def get_stub_policy(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['stub_policy'])
        if value == 'nan':
            value = ''
        return value
    
    def get_broken_period_type(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['broken_period_type'])
        if value == 'nan':
            value = ''
        return value
    
    def get_pay_day_convention(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['pay_day_convention'])
        if value == 'nan':
            value = ''
        return value
    
    def get_excoupon_period(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['excoupon_period'])
        if value == 'nan':
            value = ''
        return value
            
    def get_excoupon_calendar(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['excoupon_calendar'])
        if value == 'nan':
            value = ''
        return value
    
    def get_excoupon_day_convention(self, bond_name):
        value = str(self.benchmark_bond.loc[bond_name]['excoupon_day_convention'])
        if value == 'nan':
            value = ''
        return value
    
    def get_excoupon_eom(self, bond_name):
        return bool(self.benchmark_bond.loc[bond_name]['excoupon_eom'])
        
###############################################################################
if __name__ == "__main__":
    vanilla_bond_template_manager = VanillaBondTemplateManager()
    print('vanilla bond:', vanilla_bond_template_manager.vanilla_bond)
    
    bench_bond_template_manager = BenchmarkBondTemplateManager()
    print('benchmark bond:', bench_bond_template_manager.benchmark_bond)
