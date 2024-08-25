# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 17:11:48 2021

@author: dzhu
"""
import sys

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from iryieldcurvemanager import create_flat_ir_yield_curve
from utility import to_date

###############################################################################
def create_fi_mkt_data_set(as_of_date,
                           discount_curve,
                           spread_curve,
                           forward_curve,
                           underlying):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        2. discount_curve: dqproto.IrYieldCurve
        3. spread_curve: dqproto.IrYieldCurve
        4. forward_curve: dqproto.IrYieldCurve
        5. underlying: string
    @return:
        dqproto.FiMktDataSet
    '''
    try: 
        p_as_of_date = to_date(as_of_date, '%Y-%m-%d')
        
        if discount_curve == '':
            raise Exception('empty discount curve')            
        p_discount_curve = discount_curve
        
        if spread_curve == '':
            p_spread_curve = create_flat_ir_yield_curve(as_of_date,
                                                        CurrencyName.DESCRIPTOR.values_by_number[p_discount_curve.currency].name,
                                                        0.0,
                                                        '')
        else:
            p_spread_curve = spread_curve
        
        if forward_curve !='':
            p_forward_curve = forward_curve
        else:
            p_forward_curve = create_flat_ir_yield_curve(as_of_date,
                                                         CurrencyName.DESCRIPTOR.values_by_number[p_discount_curve.currency].name,
                                                         0.0,
                                                         '')
        
        p_bond = underlying
        p_use_binary = False
        p_discount_curve_bin = b''
        p_spread_curve_bin = b''
        p_forward_curve_bin = b''
        mds = dqCreateProtoFiMktDataSet(p_as_of_date, 
                                        p_discount_curve, 
                                        p_spread_curve, 
                                        p_forward_curve, 
                                        p_bond, 
                                        p_use_binary, 
                                        p_discount_curve_bin, 
                                        p_spread_curve_bin, 
                                        p_forward_curve_bin)
        return mds
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))


###############################################################################
def create_fi_risk_settings(curve_risk_type,
                            discount_curve_delta,
                            credit_sprd_curve_delta,
                            forward_curve_delta,
                            theta,
                            discount_curve_shift,
                            sprd_curve_shift,
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
    try:   
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
        
        if credit_sprd_curve_delta.lower() == 't' or credit_sprd_curve_delta.lower() == 'total':
            p_calc_spread_curve_delta = True
            p_calc_bucket_spread_curve_delta = False
        elif credit_sprd_curve_delta.lower() == 'b' or credit_sprd_curve_delta.lower() == 'bucket':
            p_calc_spread_curve_delta = False
            p_calc_bucket_spread_curve_delta = True
        else:
            p_calc_spread_curve_delta = False
            p_calc_bucket_spread_curve_delta = False
            
        p_calc_spread_curve_gamma = False
        p_calc_bucket_spread_curve_gamma = False
        
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
        
        p_calc_theta = bool(theta) 
        
        p_discount_curve_shift = discount_curve_shift 
        p_spread_curve_shift = sprd_curve_shift  
        p_forward_curve_shift = forward_curve_shift  
        p_theta_shift = 1 
        p_ir_curve_scale = scaling_factor
        p_discount_curve_risk_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[shift_method.upper()].number
        p_spread_curve_risk_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[shift_method.upper()].number 
        p_forward_curve_risk_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[shift_method.upper()].number 
        p_threading_mode = ThreadingMode.DESCRIPTOR.values_by_name[threading_mode.upper()].number 
        p_analytical = bool(analytical)
        pb_settings = dqCreateProtoFiRiskSettings(p_ir_curve_risk_type, 
                                                  p_calc_discount_curve_delta, 
                                                  p_calc_discount_curve_gamma, 
                                                  p_calc_spread_curve_delta, 
                                                  p_calc_spread_curve_gamma, 
                                                  p_calc_forward_curve_delta, 
                                                  p_calc_forward_curve_gamma, 
                                                  p_calc_theta, 
                                                  p_calc_bucket_discount_curve_delta, 
                                                  p_calc_bucket_discount_curve_gamma, 
                                                  p_calc_bucket_spread_curve_delta, 
                                                  p_calc_bucket_spread_curve_gamma, 
                                                  p_calc_bucket_forward_curve_delta, 
                                                  p_calc_bucket_forward_curve_gamma, 
                                                  p_discount_curve_shift, 
                                                  p_spread_curve_shift, 
                                                  p_forward_curve_shift, 
                                                  p_theta_shift, 
                                                  p_ir_curve_scale, 
                                                  p_discount_curve_risk_method, 
                                                  p_spread_curve_risk_method, 
                                                  p_forward_curve_risk_method, 
                                                  p_threading_mode, 
                                                  p_analytical)
        return pb_settings
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################        
def fixed_cpn_bond_pricer(pricing_date,
                          instrument,
                          mkt_data_set,
                          risk_settings):
    '''
    @args:
        1. pricing_date: string, format='%Y-%m-%d'
        2. instrument: dqproto.VanillaBond
        3. mkt_data_set: dqproto.FiMktDataSet
        4. risk_settings: FiRiskSettings
    @return:
        dqproto.IrPricingResults
    '''
    try:     
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
        p_name = ''
        pb_input = dqCreateProtoFixedCouponBondPricingInput(p_pricing_date, 
                                                            p_instrument, 
                                                            p_mkt_data, 
                                                            p_pricing_settings, 
                                                            p_risk_settings, 
                                                            p_use_binary, 
                                                            p_instrument_bin, 
                                                            p_mkt_data_bin, 
                                                            p_pricing_settings_bin, 
                                                            p_risk_settings_bin, 
                                                            p_name)
        req_name = 'FIXED_COUPON_BOND_PRICER'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        if res_msg == None:
            raise Exception('FIXED_COUPON_BOND_PRICER ProcessRequest: failed!')
        pb_output = FixedCouponBondPricingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.results
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def fixed_cpn_bond_calcualtor(as_of_date,
                              instrument,
                              compounding_type,
                              yield_to_maturity):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        2. instrument: dqproto.VanillaBond
       
    @return:
        dqproto.BondPricingResults
    '''
    try:     
        p_calculation_date = to_date(as_of_date, '%Y-%m-%d')
        p_bond = instrument
        p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[compounding_type.upper()].number
        p_yield_rate = yield_rate        
        p_name = ''
        pb_input = dqCreateProtoFixedCouponBondCalculationInput(p_calculation_date, 
                                                                p_compounding_type, 
                                                                p_bond, 
                                                                p_yield_rate, 
                                                                p_name)
        req_name = 'FIXED_COUPON_BOND_CALCULATOR'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = FixedCouponBondCalculationOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.result
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################        
def zero_cpn_bond_pricer(pricing_date,
                         instrument,
                         mkt_data_set,
                         risk_settings):
    '''
    @args:
        1. pricing_date: string, format='%Y-%m-%d'
        2. instrument: dqproto.VanillaBond
        3. mkt_data_set: dqproto.FiMktDataSet
        4. risk_settings: FiRiskSettings
    @return:
        dqproto.IrPricingResults
    '''
    try:     
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
        p_name = ''
        pb_input = dqCreateProtoZeroCouponBondPricingInput(p_pricing_date, 
                                                           p_instrument, 
                                                           p_mkt_data, 
                                                           p_pricing_settings, 
                                                           p_risk_settings, 
                                                           p_use_binary, 
                                                           p_instrument_bin, 
                                                           p_mkt_data_bin, 
                                                           p_pricing_settings_bin, 
                                                           p_risk_settings_bin, 
                                                           p_name)
        req_name = 'ZERO_COUPON_BOND_PRICER'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        if res_msg == None:
            raise Exception('ZERO_COUPON_BOND_PRICER ProcessRequest: failed!')
        
        pb_output = ZeroCouponBondPricingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.results
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def zero_cpn_bond_calcualtor(as_of_date,
                             instrument,
                             compounding_type,
                             yield_to_maturity):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        2. instrument: dqproto.VanillaBond
       
    @return:
        dqproto.BondPricingResults
    '''
    try:     
        p_calculation_date = to_date(as_of_date, '%Y-%m-%d')
        p_bond = instrument
        p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[compounding_type.upper()].number
        p_yield_rate = yield_rate        
        p_name = ''
        pb_input = dqCreateProtoZeroCouponBondCalculationInput(p_calculation_date, 
                                                               p_compounding_type, 
                                                               p_bond, 
                                                               p_yield_rate, 
                                                               p_name)
        req_name = 'ZERO_COUPON_BOND_CALCULATOR'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = ZeroCouponBondCalculationOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.result
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))

###############################################################################        
def vanilla_bond_pricer(pricing_date,
                        instrument,
                        mkt_data_set,
                        risk_settings):
    '''
    @args:
        1. pricing_date: string, format='%Y-%m-%d'
        2. instrument: dqproto.VanillaBond
        3. mkt_data_set: dqproto.FiMktDataSet
        4. risk_settings: FiRiskSettings
    @return:
        dqproto.IrPricingResults
    '''
    try:     
        if instrument.vanilla_bond_type == FIXED_COUPON_BOND:
            return fixed_cpn_bond_pricer(pricing_date,
                                         instrument,
                                         mkt_data_set,
                                         risk_settings)
        elif instrument.vanilla_bond_type == ZERO_COUPON_BOND:
            return zero_cpn_bond_pricer(pricing_date,
                                        instrument,
                                        mkt_data_set,
                                        risk_settings)
        else:
            raise Exception('This type of bond is not supported yet!')
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        

###############################################################################
def vanilla_bond_calcualtor(as_of_date,
                            instrument,
                            compounding_type,
                            yield_to_maturity):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        2. instrument: dqproto.VanillaBond
       
    @return:
        dqproto.BondPricingResults
    '''
    try:     
        if instrument.vanilla_bond_type == FIXED_COUPON_BOND:
            return fixed_cpn_bond_calcualtor(as_of_date,
                                             instrument,
                                             compounding_type,
                                             yield_to_maturity)
        elif instrument.vanilla_bond_type == ZERO_COUPON_BOND:
            return zero_cpn_bond_calcualtor(as_of_date,
                                            instrument,
                                            compounding_type,
                                            yield_to_maturity)
        else:
            raise Exception('This type of bond is not supported yet!')
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def yield_to_maturity_calculator(as_of_date,
                                 instrument,
                                 compounding_type,
                                 forward_curve,
                                 price,
                                 price_type):    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        p_calculation_date = to_date(as_of_date, '%Y-%m-%d')
        p_bond = instrument
        p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[compounding_type.upper()].number
        p_forward_curve = forward_curve   
        p_price = price 
        p_price_type = price_type
        pb_input = dqCreateProtoYieldToMaturityCalculationInput(p_calculation_date, 
                                                                p_compounding_type, 
                                                                p_bond, 
                                                                p_forward_curve, 
                                                                p_price, 
                                                                p_price_type)
        req_name = 'YIELD_TO_MATURITY_CALCULATOR'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = YieldToMaturityCalculationOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.ytm
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))        