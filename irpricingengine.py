# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 17:10:28 2021

@author: dzhu
"""
from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_date

###############################################################################
def create_ir_mkt_data_set(as_of_date,
                           discount_curves,
                           forward_curves):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        2. discount_curves: dict, key = currency, and value = dqproto.IrYieldCurve
        4. forward_curves: dict, key = ibor index, and value = dqproto.IrYieldCurve
        5. underlying: string
    @return:
        dqproto.IrMktDataSet
    '''
    if discount_curves == '':
            raise Exception('empty discount curve')
        
    p_discount_curves = list()
    for key in discount_curves.keys():
        p_name = key
        p_curve = discount_curves[key]   
        p_curve_bin = b''
        p_discount_curves.append(dqCreateProtoIrMktDataSet_DiscountCurveMap(p_name, 
                                                                            p_curve, 
                                                                            p_curve_bin))
    p_forward_curves = list()
    for key in forward_curves.keys():
        p_name = key
        p_curve = forward_curves[key]   
        p_curve_bin = b''
        p_forward_curves.append(dqCreateProtoIrMktDataSet_ForwardCurveMap(p_name, 
                                                                          p_curve, 
                                                                          p_curve_bin))
    
    p_as_of_date = to_date(as_of_date, '%Y-%m-%d')
    p_capfloor_vol_surfs = list()
    p_swaption_vol_surfs = list()
    p_swaption_quote_cubes = list()
    p_fx_spot = FxSpotRate()
    p_use_binary = False
    p_fx_spot_bin = b''
    mds = dqCreateProtoIrMktDataSet(p_as_of_date, 
                                    p_discount_curves, 
                                      p_forward_curves, 
                                      p_capfloor_vol_surfs, 
                                      p_swaption_vol_surfs, 
                                      p_swaption_quote_cubes, 
                                      p_fx_spot, 
                                      p_use_binary, 
                                      p_fx_spot_bin)
    return mds

###############################################################################
def create_ir_risk_settings(curve_risk_type,
                            discount_curve_delta,
                            forward_curve_delta,
                            theta,
                            discount_curve_shift,
                            forward_curve_shift,
                            scaling_factor,
                            shift_method,
                            threading_mode,
                            analytical):
    '''
    @args:
        1. pricing_date: string, format='%Y-%m-%d'
        2. instrument: dqproto.VanillaBond
        3. mkt_data_set: dqproto.FiMktDataSet
        4. risk_settings: FiRiskSettings
    @return:
        dqproto.FiRiskSettings
    '''
    p_ir_curve_risk_type = IrCurveRiskType.DESCRIPTOR.values_by_name[curve_risk_type.upper()].number
    if discount_curve_delta.lower() == 't' or discount_curve_delta.lower() == 'total':
        p_calc_discount_curve_delta = True
        p_calc_bucket_discount_curve_delta = False
    elif discount_curve_delta.lower() == 'b' or discount_curve_delta.lower() == 'bucket':
        p_calc_discount_curve_delta = False
        p_calc_bucket_discount_curve_delta = True
    else:
        p_calc_discount_curve_delta = False
        p_calc_bucket_discount_curve_delta = False
    
    p_calc_discount_curve_gamma = False
    p_calc_bucket_discount_curve_gamma = False
    
    if forward_curve_delta.lower() == 't' or forward_curve_delta.lower() == 'total':
        p_calc_forward_curve_delta = True
        p_calc_bucket_forward_curve_delta = False
    elif forward_curve_delta.lower() == 'b' or forward_curve_delta.lower() == 'bucket':
        p_calc_forward_curve_delta = False
        p_calc_bucket_forward_curve_delta = True
    else:
        p_calc_forward_curve_delta = False
        p_calc_bucket_forward_curve_delta = False
        
    p_calc_forward_curve_gamma = False
    p_calc_bucket_forward_curve_gamma = False
    
    p_calc_cap_vol_vega = False
    p_calc_cap_vol_volga = False
    p_calc_swaption_vol_vega = False
    p_calc_swaption_vol_volga = False
    p_calc_bucket_cap_vol_vega = False 
    p_calc_bucket_cap_vol_volga = False 
    p_calc_bucket_swaption_vol_vega = False 
    p_calc_bucket_swaption_vol_volga = False 
    p_calc_corr_risk = False 
    p_calc_bucket_corr_risk = False 
    p_calc_quanto_discount_curve_delta = False 
    p_calc_quanto_fx_vega = False 
    p_calc_quanto_corr_risk = False 
    p_calc_bucket_quanto_discount_curve_delta = False 
    p_calc_bucket_quanto_fx_vega = False 
    p_calc_bucket_quanto_corr_risk = False 
                                              
    p_calc_theta = bool(theta) 
    
    p_discount_curve_shift = discount_curve_shift 
    p_forward_curve_shift = forward_curve_shift  
    
    p_vol_shift = 0.0
    p_theta_shift = 1
    p_correlation_shift = 0.0
    p_quanto_discount_curve_shift = 0.0 
    p_quanto_fx_vol_shift = 0.0
    p_quanto_corr_shift = 0.0
    
    p_ir_curve_scale = scaling_factor
    
    p_discount_curve_risk_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[shift_method.upper()].number    
    p_forward_curve_risk_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[shift_method.upper()].number 
    p_cap_vol_risk_method = CENTRAL_DIFFERENCE_METHOD
    p_swaption_vol_risk_method = CENTRAL_DIFFERENCE_METHOD 
    p_corr_risk_method = CENTRAL_DIFFERENCE_METHOD 
    p_quanto_discount_curve_risk_method = CENTRAL_DIFFERENCE_METHOD 
    p_quanto_fx_vol_risk_method = CENTRAL_DIFFERENCE_METHOD 
    p_quanto_corr_risk_method = CENTRAL_DIFFERENCE_METHOD
                                              
    p_threading_mode = ThreadingMode.DESCRIPTOR.values_by_name[threading_mode.upper()].number 
    p_analytical = bool(analytical)
    pb_settings = dqCreateProtoIrRiskSettings(p_ir_curve_risk_type, 
                                              p_calc_discount_curve_delta, 
                                              p_calc_discount_curve_gamma, 
                                              p_calc_forward_curve_delta, 
                                              p_calc_forward_curve_gamma, 
                                              p_calc_cap_vol_vega, 
                                              p_calc_cap_vol_volga, 
                                              p_calc_swaption_vol_vega, 
                                              p_calc_swaption_vol_volga, 
                                              p_calc_theta, 
                                              p_calc_bucket_discount_curve_delta, 
                                              p_calc_bucket_discount_curve_gamma, 
                                              p_calc_bucket_forward_curve_delta, 
                                              p_calc_bucket_forward_curve_gamma, 
                                              p_calc_bucket_cap_vol_vega, 
                                              p_calc_bucket_cap_vol_volga, 
                                              p_calc_bucket_swaption_vol_vega, 
                                              p_calc_bucket_swaption_vol_volga, 
                                              p_calc_corr_risk, 
                                              p_calc_bucket_corr_risk, 
                                              p_calc_quanto_discount_curve_delta, 
                                              p_calc_quanto_fx_vega, 
                                              p_calc_quanto_corr_risk, 
                                              p_calc_bucket_quanto_discount_curve_delta, 
                                              p_calc_bucket_quanto_fx_vega, 
                                              p_calc_bucket_quanto_corr_risk, 
                                              p_discount_curve_shift, 
                                              p_forward_curve_shift, 
                                              p_vol_shift, 
                                              p_theta_shift, 
                                              p_correlation_shift, 
                                              p_quanto_discount_curve_shift, 
                                              p_quanto_fx_vol_shift, 
                                              p_quanto_corr_shift, 
                                              p_ir_curve_scale, 
                                              p_discount_curve_risk_method, 
                                              p_forward_curve_risk_method, 
                                              p_cap_vol_risk_method, 
                                              p_swaption_vol_risk_method, 
                                              p_corr_risk_method, 
                                              p_quanto_discount_curve_risk_method, 
                                              p_quanto_fx_vol_risk_method, 
                                              p_quanto_corr_risk_method, 
                                              p_threading_mode, 
                                              p_analytical)
    return pb_settings
        
###############################################################################
def ir_vanilla_inst_pricer(pricing_date,
                           instrument,
                           mkt_data_set,
                           risk_settings):
    '''
    
    '''
    p_pricing_date = to_date(pricing_date, '%Y-%m-%d')
    p_instrument = instrument
    p_mkt_data = mkt_data_set
    p_pricing_settings = PricingSettings()
    p_risk_settings = risk_settings
    p_use_binary = False
    p_instrument_bin = b''
    p_mkt_data_bin = b''
    p_pricing_settings_bin = b''
    p_risk_settings_bin = b''           
    pb_input = dqCreateProtoIrVanillaInstrumentPricingInput(p_pricing_date, 
                                                            p_instrument, 
                                                            p_mkt_data, 
                                                            p_pricing_settings, 
                                                            p_risk_settings, 
                                                            p_use_binary, 
                                                            p_instrument_bin, 
                                                            p_mkt_data_bin, 
                                                            p_pricing_settings_bin, 
                                                            p_risk_settings_bin)
    req_name = 'IR_VANILLA_INSTRUMENT_PRICER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('IR_VANILLA_INSTRUMENT_PRICER ProcessRequest: failed!')
    pb_output = IrVanillaInstrumentPricingOutput()
    pb_output.ParseFromString(res_msg)    
    return pb_output.results
        