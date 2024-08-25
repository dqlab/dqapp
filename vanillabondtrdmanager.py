# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:15:55 2021

@author: dzhu
"""
import sys
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_date, to_calendar_name_list, to_period
from utility import save_pb_data
###############################################################################
def build_fixed_cpn_bond(currency,
                         issue_date, 
                         settlement_days, 
                         maturity_date, 
                         coupon_rate, 
                         day_count_convention, 
                         nominal, 
                         frequency, 
                         calendars, 
                         interest_day_convention, 
                         stub_policy, 
                         broken_period_type, 
                         pay_day_convention, 
                         excoupon_period, 
                         excoupon_calendars, 
                         excoupon_day_convention, 
                         excoupon_end_of_month, 
                         name):    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        p_currency =  CurrencyName.DESCRIPTOR.values_by_name[currency.upper()].number
        p_issue_date = to_date(issue_date, '%d/%m/%Y')
        p_settlement_days = settlement_days
        p_maturity_date = to_date(maturity_date, '%d/%m/%Y')
        p_pay_receive = RECEIVE 
        p_coupon_rate = coupon_rate 
        p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[day_count_convention.upper()].number
        p_nominal =  nominal
        p_frequency = Frequency.DESCRIPTOR.values_by_name[frequency.upper()].number 
        p_calendars = to_calendar_name_list([calendars]) 
        p_interest_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[interest_day_convention.upper()].number 
        p_stub_policy = StubPolicy.DESCRIPTOR.values_by_name[stub_policy.upper()].number 
        p_broken_period_type = BrokenPeriodType.DESCRIPTOR.values_by_name[broken_period_type.upper()].number 
        p_pay_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[pay_day_convention.upper()].number 
        p_excoupon_period = to_period(excoupon_period) 
        p_excoupon_calendars = to_calendar_name_list([calendars])  
        p_excoupon_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[excoupon_day_convention.upper()].number  
        p_excoupon_end_of_month = bool(excoupon_end_of_month) 
        p_name = name.upper()
        pb_input = dqCreateProtoCreateFixedCouponBondInput(p_currency, 
                                                           p_issue_date, 
                                                           p_settlement_days, 
                                                           p_maturity_date, 
                                                           p_pay_receive, 
                                                           p_coupon_rate, 
                                                           p_day_count_convention, 
                                                           p_nominal, 
                                                           p_frequency, 
                                                           p_calendars, 
                                                           p_interest_day_convention, 
                                                           p_stub_policy, 
                                                           p_broken_period_type, 
                                                           p_pay_day_convention, 
                                                           p_excoupon_period, 
                                                           p_excoupon_calendars, 
                                                           p_excoupon_day_convention, 
                                                           p_excoupon_end_of_month, 
                                                           p_name)
           
        req_name = 'CREATE_FIXED_COUPON_BOND'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = CreateFixedCouponBondOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.fixed_coupon_bond
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))        

###############################################################################
def build_zero_cpn_bond(currency, 
                        issue_date, 
                        settlement_days, 
                        maturity_date, 
                        day_count_convention, 
                        nominal, 
                        calendars, 
                        pay_day_convention, 
                        name):    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        p_currency =  CurrencyName.DESCRIPTOR.values_by_name[currency.upper()].number
        p_issue_date = to_date(issue_date, '%d/%m/%Y')
        p_settlement_days = settlement_days
        p_maturity_date = to_date(maturity_date, '%d/%m/%Y')
        p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[day_count_convention.upper()].number
        p_nominal =  nominal
        p_calendars = to_calendar_name_list([calendars]) 
        p_pay_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[pay_day_convention.upper()].number 
        p_interest_day_convention = p_pay_day_convention
        p_issue_price = 100
        p_name = name.upper()
        p_pay_receive = RECEIVE 
        pb_input = dqCreateProtoCreateZeroCouponBondInput(p_currency, 
                                                          p_issue_date, 
                                                          p_settlement_days, 
                                                          p_maturity_date, 
                                                          p_pay_receive, 
                                                          p_day_count_convention, 
                                                          p_nominal, 
                                                          p_calendars, 
                                                          p_interest_day_convention, 
                                                          p_pay_day_convention, 
                                                          p_issue_price, 
                                                          p_name)
    
        req_name = 'CREATE_ZERO_COUPON_BOND'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = CreateZeroCouponBondOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.zero_coupon_bond
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))  

###############################################################################
def build_vanilla_bond(bond_type,
                       currency,
                       issue_date, 
                       settlement_days, 
                       maturity_date, 
                       coupon_rate, 
                       day_count_convention, 
                       nominal, 
                       frequency, 
                       calendars, 
                       interest_day_convention, 
                       stub_policy, 
                       broken_period_type, 
                       pay_day_convention, 
                       excoupon_period, 
                       excoupon_calendars, 
                       excoupon_day_convention, 
                       excoupon_end_of_month, 
                       name):
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        if bond_type.lower() == 'fixed_coupon_bond':
            return build_fixed_cpn_bond(currency,
                                        issue_date, 
                                        settlement_days, 
                                        maturity_date, 
                                        coupon_rate, 
                                        day_count_convention, 
                                        nominal, 
                                        frequency, 
                                        calendars, 
                                        interest_day_convention, 
                                        stub_policy, 
                                        broken_period_type, 
                                        pay_day_convention, 
                                        excoupon_period, 
                                        excoupon_calendars, 
                                        excoupon_day_convention, 
                                        excoupon_end_of_month, 
                                        name)
        elif bond_type.lower() == 'zero_coupon_bond':
            return build_zero_cpn_bond(currency, 
                                       issue_date, 
                                       settlement_days, 
                                       maturity_date, 
                                       day_count_convention, 
                                       nominal, 
                                       calendars, 
                                       pay_day_convention, 
                                       name)
        else:
            raise Exception(bond_type + ' is not supported yet!')
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))  
       
        
###############################################################################
class VanillaBondTrdDataManager:
    def __init__(self, bond_sd_manager, trd_data_manager):
        self.trd_data = pd.read_csv('trddata/fixedincome/bond/vanilla_bond.csv')  
        self.trd_data.columns = self.trd_data.columns.str.lower()
        self.trd_data = self.trd_data.set_index('trade_id')
        
        pb_trades = list()
        discount_curves = list()
        sprd_curves = list()
        fwd_curves = list()
        for i in range(len(self.trd_data)):
            trd_id = self.trd_data.index[i]
            bond_id = trd_data_manager.get_inst_name(trd_id)
            nominal = trd_data_manager.get_nominal(trd_id)
            
            discount_curve = str(self.trd_data.iloc[i]['discount_curve'])
            if discount_curve == '' or discount_curve == 'nan':
                discount_curve = bond_sd_manager.get_discount_curve(bond_id)
                        
            sprd_curve  = str(self.trd_data.iloc[i]['spread_curve'])
            if sprd_curve == '' or sprd_curve == 'nan':
                sprd_curve = bond_sd_manager.get_sprd_curve(bond_id)
                        
            fwd_curve  = str(self.trd_data.iloc[i]['forward_curve'])
            if fwd_curve == '' or fwd_curve == 'nan':
                fwd_curve = bond_sd_manager.get_forward_curve(bond_id)
                       
            bond_type = bond_sd_manager.get_bond_type(bond_id)
            currency = bond_sd_manager.get_currency(bond_id)
            issue_date = bond_sd_manager.get_issue_date(bond_id) 
            settlement_days = bond_sd_manager.get_settlement_days(bond_id) 
            maturity_date = bond_sd_manager.get_maturity(bond_id) 
            coupon_rate = bond_sd_manager.get_coupon_rate(bond_id) 
            day_count_convention = bond_sd_manager.get_day_count_convention(bond_id)
            frequency = bond_sd_manager.get_frequency(bond_id) 
            calendars = bond_sd_manager.get_calendar(bond_id) 
            interest_day_convention = bond_sd_manager.get_interest_day_convention(bond_id) 
            stub_policy = bond_sd_manager.get_stub_policy(bond_id) 
            broken_period_type = bond_sd_manager.get_broken_period_type(bond_id) 
            pay_day_convention = bond_sd_manager.get_pay_day_convention(bond_id) 
            excoupon_period = bond_sd_manager.get_excoupon_period(bond_id) 
            excoupon_calendars = bond_sd_manager.get_excoupon_calendar(bond_id) 
            excoupon_day_convention = bond_sd_manager.get_excoupon_day_convention(bond_id) 
            excoupon_end_of_month = bond_sd_manager.get_excoupon_eom(bond_id) 
            
            trd = build_vanilla_bond(bond_type,
                                     currency,
                                     issue_date, 
                                     settlement_days, 
                                     maturity_date, 
                                     coupon_rate, 
                                     day_count_convention, 
                                     nominal, 
                                     frequency, 
                                     calendars, 
                                     interest_day_convention, 
                                     stub_policy, 
                                     broken_period_type, 
                                     pay_day_convention, 
                                     excoupon_period, 
                                     excoupon_calendars, 
                                     excoupon_day_convention, 
                                     excoupon_end_of_month, 
                                     bond_id)
            
            #save_pb_data(trd, trd_id, 'trddata/fixedincome/bond')
            discount_curves.append(discount_curve)
            sprd_curves.append(sprd_curve)
            fwd_curves.append(fwd_curve)
            pb_trades.append(trd)        
        
        self.trd_data['data'] = pb_trades
        self.trd_data['discount_curve'] = discount_curves
        self.trd_data['sprd_curve'] = sprd_curves
        self.trd_data['fwd_curve'] = fwd_curves
            
    def get_discount_curve(self, trd_id):
        return str(self.trd_data.loc[trd_id]['discount_curve'])
    
    def get_sprd_curve(self, trd_id):
        return str(self.trd_data.loc[trd_id]['sprd_curve'])
    
    def get_fwd_curve(self, trd_id):
        return str(self.trd_data.loc[trd_id]['fwd_curve'])
    
    def get_trade(self, trd_id):
        return self.trd_data.loc[trd_id]['data']

###############################################################################
if __name__ == "__main__":
    from calendarmanager import CalendarManager

    from vanillabondtemplatemanager import VanillaBondTemplateManager 
    from trddata import TrdDataManager
    
    calendar_manager = CalendarManager()
    vanilla_bond_template_manager = VanillaBondTemplateManager()
    
    trd_data_manager = TrdDataManager()
    vanilla_bond_trd_data_manager = VanillaBondTrdDataManager(vanilla_bond_template_manager, trd_data_manager)
    print('bond trades:',  vanilla_bond_trd_data_manager.trd_data)