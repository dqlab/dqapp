# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:53:30 2021

@author: dzhu
"""
import sys
import pandas as pd
import numpy as np

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_excel_date, to_date, to_period, save_pb_data
###############################################################################
def create_bond_par_curve(as_of_date,
                          currency,
                          pillar_data,
                          mat_type,
                          quote_type,
                          curve_name):
    '''
    @args:
        3. pillar_data: pandas.DataFrame, columns=['bond_id','maturity','quote','coupon','issue_date']
        4. mat_type: string, {'date', 'period'}
    @return:
        dqproto.BondParCurve
    '''
    ref_date = to_excel_date(as_of_date, '%Y-%m-%d')
    p_pillars = list()
    for i in range(len(pillar_data)):
        p_instrument_name = pillar_data.iloc[i]['bond_id']
        p_maturity = pillar_data.iloc[i]['bond_term']
        if mat_type.lower() == 'date':
            mat = to_excel_date(p_maturity, '%Y-%m-%d')
            num_days = mat - ref_date
            p_maturity = dqCreateProtoPeriod(num_days, DAYS)
        else:#period
            p_maturity = to_period(p_maturity)
        p_quote = pillar_data.iloc[i]['quote']
        p_coupon = pillar_data.iloc[i]['coupon']
        p_issue_date = pillar_data.iloc[i]['issue_date']
        p_issue_date = to_date(p_issue_date, '%Y-%m-%d')
        p_instrument_type = INVALID_INSTRUMENT_TYPE
        pb_pillar = dqCreateProtoCreateBondParCurveInput_Pillar(p_instrument_name, 
                                                                p_instrument_type, 
                                                                p_issue_date, 
                                                                p_maturity, 
                                                                p_quote, 
                                                                p_coupon)
        p_pillars.append(pb_pillar)
    
    p_reference_date = to_date(as_of_date, '%Y-%m-%d')
    p_currency = CurrencyName.DESCRIPTOR.values_by_name[currency.upper()].number
    p_quote_type = BondQuoteType.DESCRIPTOR.values_by_name[quote_type.upper()].number
    p_name = curve_name.upper()
    pb_input = dqCreateProtoCreateBondParCurveInput(p_reference_date, 
                                                    p_currency, 
                                                    p_pillars, 
                                                    p_quote_type, 
                                                    p_name)
    
    req_name = 'CREATE_BOND_PAR_CURVE'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = CreateBondParCurveOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.bond_par_curve
        
###############################################################################
def create_bond_curve_build_settings(curve_name,
                                     curve_type,
                                     interp_method,
                                     extrap_method,
                                     discount_curve_settings,
                                     fwd_curve_settings):
    '''
    @args:
        3. 
        4. discount_curve_settings: list of 2 string elements, where [0]: currency; [1]: curve name
        5. fwd_curve_settings: list of 2 string elements, where [0]: reference index; [1]: curve name
    @return:
        dqproto.BondYieldCurveBuildSettings
    '''
    p_currency_name = CurrencyName.DESCRIPTOR.values_by_name[discount_curve_settings[0].upper()].number
    p_discnt_curve_name = discount_curve_settings[1].lower()
    pb_dscnt_curve_settings = dqCreateProtoBondYieldCurveBuildSettings_DiscountCurveInfo(p_currency_name, 
                                                                                         p_discnt_curve_name)
    p_discount_curve_info = [pb_dscnt_curve_settings]

    p_sprd_index_name = ''
    p_sprd_curve_name = ''
    pb_sprd_curve_settings = dqCreateProtoBondYieldCurveBuildSettings_SpreadCurveInfo(p_sprd_index_name, p_sprd_curve_name)
    p_spread_curve_info = [pb_sprd_curve_settings]
    
    p_ref_index_name = fwd_curve_settings[0].lower()
    p_fwd_curve_name = fwd_curve_settings[1].lower()
    pb_fwd_curve_settings = dqCreateProtoBondYieldCurveBuildSettings_ForwardCurveInfo(p_ref_index_name, 
                                                                                      p_fwd_curve_name)
    p_forward_curve_info = [pb_fwd_curve_settings]
    
    p_curve_name = curve_name.lower()
    p_curve_type = IrYieldCurveType.DESCRIPTOR.values_by_name[curve_type.upper()].number
    p_interp_method = InterpMethod.DESCRIPTOR.values_by_name[interp_method.upper()].number
    p_extrap_method = ExtrapMethod.DESCRIPTOR.values_by_name[extrap_method.upper()].number
    pb_build_settings = dqCreateProtoBondYieldCurveBuildSettings(p_curve_name, 
                                                                 p_curve_type, 
                                                                 p_interp_method, 
                                                                 p_extrap_method, 
                                                                 p_discount_curve_info, 
                                                                 p_spread_curve_info, 
                                                                 p_forward_curve_info)
    
    return pb_build_settings    

###############################################################################        
def build_bond_yield_curve(as_of_date,
                           curve_name,
                           build_settings,
                           par_curve,
                           day_count,
                           compounding_type,
                           freq,
                           to_settlement,
                           other_curves,
                           build_method,
                           calc_jacobian):
    '''
    @args:
        3. build_settings: dqproto.BondYieldCurveBuildSettings
        4. par_curve: dqproto.BondParCurve
        5. day_count: string
        9. other_curves: list of dqproto.IrYieldCurve
    @return:
        dqproto.IrYieldCurve
    '''
    p_target_curve_name = curve_name.lower()
    p_bond_yield_curve_build_settings = build_settings
    p_par_curve = par_curve
    p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[day_count.upper()].number
    p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[compounding_type.upper()].number
    p_frequency = Frequency.DESCRIPTOR.values_by_name[freq.upper()].number
    p_to_settlement = bool(to_settlement)
    pb_settings_container = dqCreateProtoBondYieldCurveBuildSettingsContainer(p_target_curve_name, 
                                                                              p_bond_yield_curve_build_settings, 
                                                                              p_par_curve, 
                                                                              p_day_count_convention, 
                                                                              p_compounding_type, 
                                                                              p_frequency, 
                                                                              p_to_settlement)     

    p_build_settings =[pb_settings_container]
    
    p_reference_date = to_date(as_of_date, '%Y-%m-%d')
    p_other_curves = other_curves        
    p_curve_building_method = IrYieldCurveBuildingMethod.DESCRIPTOR.values_by_name[build_method.upper()].number
    p_calc_jacobian = bool(calc_jacobian)
    pb_input = dqCreateProtoBondYieldCurveBuildingInput(p_reference_date, 
                                                        p_build_settings, 
                                                        p_other_curves, 
                                                        p_curve_building_method, 
                                                        p_calc_jacobian)
    
    req_name = 'BOND_YIELD_CURVE_BUILDER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('BOND_YIELD_CURVE_BUILDER ProcessRequest: failed!')
    pb_output = BondYieldCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.ir_yield_curve
    
###############################################################################    
def build_bond_sprd_curve(as_of_date,
                          tgt_curve_name,
                          build_settings,
                          par_curve,
                          day_count,
                          compounding_type,
                          freq,
                          to_settlement,
                          base_curve,
                          build_method,
                          calc_jacobian):
    '''
    @args:
        3. build_settings: dqproto.BondYieldCurveBuildSettings
        4. par_curve: dqproto.BondParCurve
        5. day_count: string
        9. base_curve: dqproto.IrYieldCurve
    @return:
        dqproto.IrYieldCurve
    '''
    p_target_curve_name = tgt_curve_name.lower()
    p_bond_yield_curve_build_settings = build_settings
    p_par_curve = par_curve
    p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[day_count.upper()].number
    p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[compounding_type.upper()].number
    p_frequency = Frequency.DESCRIPTOR.values_by_name[freq.upper()].number
    p_to_settlement = bool(to_settlement)
    pb_settings_container = dqCreateProtoBondYieldCurveBuildSettingsContainer(p_target_curve_name, 
                                                                              p_bond_yield_curve_build_settings, 
                                                                              p_par_curve, 
                                                                              p_day_count_convention, 
                                                                              p_compounding_type, 
                                                                              p_frequency, 
                                                                              p_to_settlement)
    
    p_build_settings = [pb_settings_container]
    p_reference_date = to_date(as_of_date, '%Y-%m-%d')
    p_base_curve = base_curve        
    p_curve_building_method = IrYieldCurveBuildingMethod.DESCRIPTOR.values_by_name[build_method.upper()].number
    p_calc_jacobian = bool(calc_jacobian)
    pb_input = dqCreateProtoBondCreditSpreadCurveBuildingInput(p_reference_date, 
                                                               p_build_settings, 
                                                               p_base_curve, 
                                                               p_curve_building_method, 
                                                               p_calc_jacobian)        
    
    req_name = 'BOND_CREDIT_SPREAD_CURVE_BUILDER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('BOND_CREDIT_SPREAD_CURVE_BUILDER ProcessRequest: failed!')
    pb_output = BondCreditSpreadCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.ir_yield_curve
 