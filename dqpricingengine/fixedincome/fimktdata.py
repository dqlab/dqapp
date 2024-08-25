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
    try:
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
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
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
    try:
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
        
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))

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
    try:
       
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
            
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
    
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
    try:
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
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################            
class BondYieldCurveMktDataManager:
    def __init__(self, as_of_date, bond_yield_curve_sd_manager, bond_hist_data_manager, vanilla_bond_static_data_manager):
        self.yield_curves = dict()
        for curve_name in bond_yield_curve_sd_manager.curve_names:
            currency, day_count, curve_type, interp_method, extrap_method, compounding_type, frequuency, to_settlement, quote_type = bond_yield_curve_sd_manager.get_definition(curve_name)
            build_method, calc_jacobian, floating_index, fwd_curve = bond_yield_curve_sd_manager.get_build_settings(curve_name)
            build_settings = create_bond_curve_build_settings(curve_name, curve_type, interp_method, extrap_method,
                                                              [currency, curve_name],
                                                              [floating_index, fwd_curve])
            pillar_data = bond_yield_curve_sd_manager.get_term_structure(curve_name)
            pillar_data['issue_date'] = [as_of_date] * len(pillar_data)
            bond_names=list(pillar_data['bond_id'])
            pillar_data['quote'] = np.array(bond_hist_data_manager.get_hist_data(bond_names, as_of_date, as_of_date))*0.01
            cpn_rates = list()
            for bond_name in bond_names: 
                cpn_rates.append(vanilla_bond_static_data_manager.get_coupon_rate(bond_name))
            pillar_data['coupon'] = cpn_rates    
            mat_type = 'period'            
            par_curve = create_bond_par_curve(as_of_date,
                                              currency,
                                              pillar_data,
                                              mat_type,
                                              quote_type,
                                              curve_name)
            other_curves=[]
            yield_curve = build_bond_yield_curve(as_of_date,
                                                 curve_name,
                                                 build_settings,
                                                 par_curve,
                                                 day_count,
                                                 compounding_type,
                                                 frequuency,
                                                 to_settlement,
                                                 other_curves,
                                                 build_method,
                                                 calc_jacobian)
            
            self.yield_curves[curve_name] = yield_curve
            save_pb_data(yield_curve, curve_name+'_'+as_of_date, 'mktdata/fixedincome/bond')
            
    def get_yield_curve(self, curve_name):
        return self.yield_curves[curve_name]
       
###############################################################################            
class BondSprdCurveMktDataManager:
    def __init__(self, as_of_date, bond_sprd_curve_sd_manager, bond_hist_data_manager, vanilla_bond_static_data_manager, bond_yield_curve_mkt_data_manager):
        self.sprd_curves = dict()            
        for curve_name in bond_sprd_curve_sd_manager.curve_names:
            base_curve_name, currency, day_count, curve_type, interp_method, extrap_method, compounding_type, frequuency, to_settlement, quote_type = bond_sprd_curve_sd_manager.get_definition(curve_name)
            build_method, calc_jacobian, floating_index, fwd_curve = bond_sprd_curve_sd_manager.get_build_settings(curve_name)
            build_settings = create_bond_curve_build_settings(curve_name,
                                                              curve_type,
                                                              interp_method,
                                                              extrap_method,
                                                              [currency, curve_name],
                                                              [floating_index, fwd_curve])
            pillar_data = bond_sprd_curve_sd_manager.get_term_structure(curve_name)
            pillar_data['issue_date'] = [as_of_date] * len(pillar_data)
            bond_names=list(pillar_data['bond_id'])
            pillar_data['quote'] = np.array(bond_hist_data_manager.get_hist_data(bond_names, as_of_date, as_of_date))*0.01
            cpn_rates = list()
            for bond_name in bond_names: 
                cpn_rates.append(vanilla_bond_static_data_manager.get_coupon_rate(bond_name))
            pillar_data['coupon'] = cpn_rates  
            mat_type = 'period'            
            par_curve = create_bond_par_curve(as_of_date,
                                              currency,
                                              pillar_data,
                                              mat_type,
                                              quote_type,
                                              curve_name)
            
            base_curve = bond_yield_curve_mkt_data_manager.get_yield_curve(base_curve_name)
            sprd_curve = build_bond_sprd_curve(as_of_date,
                                               curve_name,
                                               build_settings,
                                               par_curve,
                                               day_count,
                                               compounding_type,
                                               frequuency,
                                               to_settlement,
                                               base_curve,
                                               build_method,
                                               calc_jacobian)
            self.sprd_curves[curve_name] = sprd_curve     
            save_pb_data(sprd_curve, curve_name+'_'+as_of_date, 'mktdata/fixedincome/bond')            
    
    def get_sprd_curve(self, curve_name):
        return self.sprd_curves[curve_name]
    
