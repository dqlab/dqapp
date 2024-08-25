# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 17:46:48 2021

@author: dzhu
"""
import sys

from dqproto import *
from utility import to_calendar_name_list, to_date, to_period

###############################################################################
def create_leg_definition(leg_type,
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
                          fixing_day_offset):
    '''
    @args:
        
    @return:
    '''
    
    if leg_type == '':
        raise Exception('create_leg_definition: empty leg_type')
        
    if currency == '':
        raise Exception('create_leg_definition: empty currency')
    
    if day_count == '':
        raise Exception('create_leg_definition: empty day_count')
        
    pb_cal_list = to_calendar_name_list([calendar])
        
    if freq in ['', 'nan']:
        pb_freq = ANNUAL
    else:
        pb_freq = Frequency.DESCRIPTOR.values_by_name[freq.upper()].number
    
    if interest_day_convention in ['', 'nan']:
        pb_interest_day_convention = FOLLOWING
    else: 
        pb_interest_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[interest_day_convention.upper()].number
    
    if stub_policy in ['', 'nan']:
        pb_stub_policy = INITIAL
    else:
        pb_stub_policy = StubPolicy.DESCRIPTOR.values_by_name[stub_policy.upper()].number
    
    if broken_period_type in ['', 'nan']:
        pb_broken_period_type = LONG
    else:
        pb_broken_period_type = BrokenPeriodType.DESCRIPTOR.values_by_name[broken_period_type.upper()].number
    
    if pay_day_offset in ['', 'nan']:
        pb_pay_day_offset = to_period('0d')
    else:
        pb_pay_day_offset = to_period(pay_day_offset)
        
    if pay_day_convention in ['', 'nan']:
        pay_day_convention = FOLLOWING
    else:
        pb_pay_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[pay_day_convention.upper()].number
    
    pb_fixing_calendars = to_calendar_name_list(fixing_calendars)
    
    if fixing_freq in ['', 'nan']:
        pb_fixing_freq = ANNUAL
    else:
        pb_fixing_freq = Frequency.DESCRIPTOR.values_by_name[fixing_freq.upper()].number
    
    if fixing_day_convention in ['', 'nan']:
        pb_fixing_day_convention = PRECEDING
    else:
        pb_fixing_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[fixing_day_convention.upper()].number
    
    if fixing_mode in ['', 'nan']:
        pb_fixing_mode = IN_ADVANCE
    else:
        pb_fixing_mode = DateGenerationMode.DESCRIPTOR.values_by_name[fixing_mode.upper()].number
    
    if fixing_day_offset in ['', 'nan']:
        pb_fixing_day_offset = to_period('0d')
    else:
        pb_fixing_day_offset = to_period(fixing_day_offset)
    
    interest_calculation_schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition_InterestCaculationScheduleDefinition(ABSOLUTE_NORMAL,
                                                                                                                                   INVALID_INTEREST_SCHEDULE_TYPE,
                                                                                                                                   pb_cal_list,
                                                                                                                                   pb_freq,
                                                                                                                                   pb_interest_day_convention,
                                                                                                                                   pb_stub_policy,
                                                                                                                                   pb_broken_period_type,
                                                                                                                                   INVALID_DATE_ROLL_CONVENTION,
                                                                                                                                   INVALID_RELATIVE_SCHEDULE_GENERATION_MODE)
    
    interest_payment_schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition_InterestPaymentScheduleDefinition(RELATIVE_TO_SCHEDULE,
                                                                                                                            INTEREST_CALCULATION_SCHEDULE,
                                                                                                                            pb_cal_list,
                                                                                                                            pb_freq,
                                                                                                                            pb_pay_day_convention,
                                                                                                                            IN_ARREAR,
                                                                                                                            1,                                                                                                                                
                                                                                                                            pb_pay_day_offset,                                                                                                                                
                                                                                                                            BACKWARD_WITHOUT_BROKEN)
    
    interest_rate_fixing_schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition_InterestRateFixingScheduleDefinition(RELATIVE_TO_SCHEDULE,
                                                                                                                                   INTEREST_CALCULATION_SCHEDULE,
                                                                                                                                   pb_fixing_calendars,
                                                                                                                                   pb_fixing_freq,
                                                                                                                                   pb_fixing_day_convention,
                                                                                                                                   pb_fixing_mode,
                                                                                                                                   1,
                                                                                                                                   pb_fixing_day_offset,
                                                                                                                                   BACKWARD_WITHOUT_BROKEN)
    
    schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition(interest_calculation_schedule_definition,
                                                                         interest_payment_schedule_definition,
                                                                         interest_rate_fixing_schedule_definition)
    
    pb_leg_type = InterestRateLegType.DESCRIPTOR.values_by_name[leg_type.upper()].number
    pb_currency = CurrencyName.DESCRIPTOR.values_by_name[currency.upper()].number
    pb_day_count = DayCountConvention.DESCRIPTOR.values_by_name[day_count.upper()].number
    
    if ref_index in ['', 'nan']:
        pb_ref_index = INVALID_IBOR_INDEX_NAME
    else:
        pb_ref_index = IborIndexName.DESCRIPTOR.values_by_name[ref_index.upper()].number
    
    if payment_discount_method in ['', 'nan']:
        pb_payment_discount_method = NO_DISCOUNT
    else:
        pb_payment_discount_method = PaymentDiscountMethod.DESCRIPTOR.values_by_name[payment_discount_method.upper()].number
    
    if rate_calc_method in ['', 'nan']:
        pb_rate_calc_method = STANDARD
    else:            
        pb_rate_calc_method = InterestRateCalculationMethod.DESCRIPTOR.values_by_name[rate_calc_method.upper()].number
    
    if notional_exchange in ['', 'nan']:
        pb_notional_exchange = INVALID_NOTIONAL_EXCHANGE
    else:
        pb_notional_exchange = NotionalExchange.DESCRIPTOR.values_by_name[notional_exchange.upper()].number
    
    pb_interest_calculation_method = SIMPLE        
    pb_broken_rate_calculation_method = CURRENT 
    
    leg_definition = dqCreateProtoInterestRateLegDefinition(pb_leg_type,
                                                            pb_currency,
                                                            pb_day_count,
                                                            pb_ref_index,
                                                            pb_payment_discount_method,
                                                            pb_interest_calculation_method,
                                                            pb_rate_calc_method,
                                                            pb_broken_rate_calculation_method,
                                                            pb_notional_exchange,
                                                            spread,
                                                            fx_convert,
                                                            fx_reset,
                                                            schedule_definition)
    
    return leg_definition
   