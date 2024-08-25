# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 03:59:06 2021

@author: dzhu
"""
from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *

from utility import to_date
from dqmarket import to_currency_pair
from pricingengine import create_pricing_model_settings

###############################################################################
def create_fx_mkt_data_set(as_of_date,
                           discount_curves,
                           spots,
                           vol_surfs):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_as_of_date = to_date(as_of_date, '%Y-%m-%d')
    p_discount_curves = discount_curves
    p_spots = spots
    p_vol_surfs = vol_surfs
    p_use_binary = False
    p_discount_curves_bin = b''
    p_spots_bin = b''
    p_vol_surfs_bin = b''
    mds = dqCreateProtoFxMktDataSet(p_as_of_date, 
                                    p_discount_curves, 
                                    p_spots, 
                                    p_vol_surfs, 
                                    p_use_binary, 
                                    p_discount_curves_bin, 
                                    p_spots_bin, 
                                    p_vol_surfs_bin)
    
    return mds    

###############################################################################
def create_fx_pricing_settings(model_settings,
                               pricing_method,
                               pricing_currency,
                               pde_settings,
                               mc_settings):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_model_settings = model_settings        
    p_pricing_currency = dqCreateProtoCurrency(CurrencyName.DESCRIPTOR.values_by_name[pricing_currency.upper()].number)
    p_risk_settings = RiskSettings()
    p_pricing_method = PricingMethodName.DESCRIPTOR.values_by_name[pricing_method.upper()].number
    p_pde_settings = PdeSettings()
    if p_pricing_method == PDE:
        p_pde_settings = pde_settings
    p_mc_settings = MonteCarloSettings()
    if p_pricing_method == MONTE_CARLO:
        p_mc_settings = mc_settings
        
    ps = dqCreateProtoPricingSettings(p_pde_settings, 
                                      p_mc_settings, 
                                      p_model_settings, 
                                      p_pricing_method, 
                                      p_risk_settings, 
                                      p_pricing_currency)
    return ps
        
###############################################################################
def create_fx_risk_settings(fx_spot_delta,
                            fx_spot_gamma,
                            fx_vega,
                            fx_volga,
                            fx_vanna,
                            ir_curve_delta,
                            theta,
                            spot_shift,
                            vol_shift,
                            ir_shift, 
                            spot_shift_method,
                            vol_shift_method,
                            ir_shift_method,
                            threading_mode,
                            analytical):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_calc_delta = bool(fx_spot_delta)
    p_calc_gamma = bool(fx_spot_gamma)
    
    if fx_vega.lower()=='t' or fx_vega.lower()=='total':
        p_calc_vega = True
        p_calc_bucket_vega = False
    elif fx_vega.lower()=='b' or fx_vega.lower()=='bucket':
        p_calc_bucket_vega = True
        p_calc_vega = False
    else:
        p_calc_vega = False
        p_calc_bucket_vega = False
        
    if fx_volga.lower()=='t' or fx_volga.lower()=='total':
        p_calc_volga = True
        p_calc_bucket_volga = False
    elif fx_volga.lower()=='b' or fx_volga.lower()=='bucket':
        p_calc_bucket_volga = True
        p_calc_volga = False
    else:
        p_calc_volga = False
        p_calc_bucket_volga = False
        
    if fx_vanna.lower()=='t' or fx_vanna.lower()=='total':
        p_calc_vanna = True
        p_calc_bucket_vanna = False
    elif fx_vanna.lower()=='b' or fx_vanna.lower()=='bucket':
        p_calc_bucket_vanna = True
        p_calc_vanna = False
    else:
        p_calc_vanna = False
        p_calc_bucket_vanna = False
        
    p_calc_theta = bool(theta) 
    
    if ir_curve_delta.lower()=='t' or ir_curve_delta.lower()=='total':
        p_calc_rho_ir = True
        p_calc_rho_dividend_yield = True
        p_calc_bucket_rho_ir = False
        p_calc_bucket_rho_dividend_yield = False
    elif ir_curve_delta.lower()=='b' or ir_curve_delta.lower()=='bucket':
        p_calc_rho_ir = False
        p_calc_rho_dividend_yield = False
        p_calc_bucket_rho_ir = True
        p_calc_bucket_rho_dividend_yield = True
    else:
        p_calc_rho_ir = False
        p_calc_rho_dividend_yield = False
        p_calc_bucket_rho_ir = False
        p_calc_bucket_rho_dividend_yield = False
    
    p_spot_shift = spot_shift 
    p_vol_shift = vol_shift  
    p_ir_shift = ir_shift
    p_dividend_yield_shift = ir_shift
    p_theta_shift = 1 
    
    p_delta_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[spot_shift_method.upper()].number
    p_vega_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[vol_shift_method.upper()].number 
    p_rho_ir_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[ir_shift_method.upper()].number 
    p_rho_dividend_yield_method = FiniteDifferenceMethod.DESCRIPTOR.values_by_name[ir_shift_method.upper()].number 
    p_threading_mode = ThreadingMode.DESCRIPTOR.values_by_name[threading_mode.upper()].number 
    p_analytical = bool(analytical)
    
    p_calc_rho_dividend_cash = False
    p_calc_corr_risk = False
    p_calc_bucket_rho_dividend_cash = False
    p_calc_bucket_corr_risk = False
    p_calc_quanto_rho_ir = False
    p_calc_quanto_fx_vega = False
    p_calc_quanto_corr_risk = False
    p_calc_bucket_quanto_rho_ir = False
    p_calc_bucket_quanto_fx_vega = False
    p_calc_bucket_quanto_corr_risk = False
    p_dividend_cash_shift = 0.0
    p_correlation_shift = 0.0 
    p_quanto_ir_shift = 0.0 
    p_quanto_fx_vol_shift = 0.0 
    p_quanto_corr_shift = 0.0 
    p_rho_dividend_cash_method = CENTRAL_DIFFERENCE_METHOD
    p_corr_risk_method = CENTRAL_DIFFERENCE_METHOD
    p_quanto_rho_ir_method = CENTRAL_DIFFERENCE_METHOD
    p_quanto_fx_vega_method = CENTRAL_DIFFERENCE_METHOD
    p_quanto_corr_risk_method = CENTRAL_DIFFERENCE_METHOD
    rs = dqCreateProtoRiskSettings(p_calc_delta, 
                                   p_calc_gamma, 
                                   p_calc_vega, 
                                   p_calc_volga, 
                                   p_calc_vanna, 
                                   p_calc_theta, 
                                   p_calc_rho_ir, 
                                   p_calc_rho_dividend_yield, 
                                   p_calc_rho_dividend_cash, 
                                   p_calc_corr_risk, 
                                   p_calc_bucket_vega, 
                                   p_calc_bucket_volga, 
                                   p_calc_bucket_vanna, 
                                   p_calc_bucket_rho_ir, 
                                   p_calc_bucket_rho_dividend_yield, 
                                   p_calc_bucket_rho_dividend_cash, 
                                   p_calc_bucket_corr_risk, 
                                   p_calc_quanto_rho_ir, 
                                   p_calc_quanto_fx_vega, 
                                   p_calc_quanto_corr_risk, 
                                   p_calc_bucket_quanto_rho_ir, 
                                   p_calc_bucket_quanto_fx_vega, 
                                   p_calc_bucket_quanto_corr_risk, 
                                   p_spot_shift, 
                                   p_vol_shift, 
                                   p_theta_shift, 
                                   p_ir_shift, 
                                   p_dividend_yield_shift, 
                                   p_dividend_cash_shift, 
                                   p_correlation_shift, 
                                   p_quanto_ir_shift, 
                                   p_quanto_fx_vol_shift, 
                                   p_quanto_corr_shift, 
                                   p_delta_method, 
                                   p_vega_method, 
                                   p_rho_ir_method, 
                                   p_rho_dividend_yield_method, 
                                   p_rho_dividend_cash_method, 
                                   p_corr_risk_method, 
                                   p_quanto_rho_ir_method, 
                                   p_quanto_fx_vega_method, 
                                   p_quanto_corr_risk_method, 
                                   p_threading_mode, 
                                   p_analytical)

    return rs

        
###############################################################################
def fx_forward_pricer(pricing_date,
                      inst,
                      mkt_data_set,
                      risk_settings):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_pricing_date = to_date(pricing_date, '%Y-%m-%d')
    p_instrument = inst
    p_mkt_data = mkt_data_set
    p_pricing_settings = PricingSettings()
    p_pricing_settings.risk_settings.CopyFrom(risk_settings)
    
    p_use_binary = False
    p_instrument_bin = b''
    p_mkt_data_bin = b''
    p_pricing_settings_bin = b''
    pb_input = dqCreateProtoFxForwardPricingInput(p_pricing_date, 
                                                  p_instrument, 
                                                  p_mkt_data, 
                                                  p_pricing_settings, 
                                                  p_use_binary, 
                                                  p_instrument_bin, 
                                                  p_mkt_data_bin, 
                                                  p_pricing_settings_bin)        
    
    req_name = 'FX_FORWARD_PRICER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxForwardPricingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.results
        
      
###############################################################################
def fx_swap_pricer(pricing_date,
                   inst,
                   mkt_data_set,
                   risk_settings):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_pricing_date = to_date(pricing_date, '%Y-%m-%d')
    p_instrument = inst
    p_mkt_data = mkt_data_set
    p_pricing_settings = PricingSettings()
    p_pricing_settings.risk_settings.CopyFrom(risk_settings)
    
    p_use_binary = False
    p_instrument_bin = b''
    p_mkt_data_bin = b''
    p_pricing_settings_bin = b''
    pb_input = dqCreateProtoFxSwapPricingInput(p_pricing_date, 
                                               p_instrument, 
                                               p_mkt_data, 
                                               p_pricing_settings, 
                                               p_use_binary, 
                                               p_instrument_bin, 
                                               p_mkt_data_bin, 
                                               p_pricing_settings_bin)        

    req_name = 'FX_SWAP_PRICER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxSwapPricingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.results

###############################################################################
def fx_european_option_pricer(pricing_date,
                              inst,
                              mkt_data_set,
                              pricing_settings,
                              risk_settings):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_pricing_date = to_date(pricing_date, '%Y-%m-%d')
    p_instrument = inst
    p_mkt_data = mkt_data_set
    p_pricing_settings = pricing_settings
    p_pricing_settings.risk_settings.CopyFrom(risk_settings)
    
    p_use_binary = False
    p_instrument_bin = b''
    p_mkt_data_bin = b''
    p_pricing_settings_bin = b''
    pb_input = dqCreateProtoFxEuropeanOptionPricingInput(p_pricing_date, 
                                                         p_instrument, 
                                                         p_mkt_data, 
                                                         p_pricing_settings, 
                                                         p_use_binary, 
                                                         p_instrument_bin, 
                                                         p_mkt_data_bin, 
                                                         p_pricing_settings_bin)        
    
    req_name = 'FX_EUROPEAN_OPTION_PRICER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxEuropeanOptionPricingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.results

###############################################################################
def fx_delta_to_strike_calculator(delta_type, 
                                  delta, 
                                  option_type, 
                                  expiry_date, 
                                  fx_spot_rate, 
                                  domestic_discount_curve, 
                                  foreign_discount_curve, 
                                  volatility_surface):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_delta_type = FxDeltaType.DESCRIPTOR.value_by_name[delta_type.upper()].number
    p_delta = delta 
    p_option_type = PayoffType.DESCRIPTOR.value_by_name[option_type.upper()].number
    p_expiry_date = to_date(expiry_date,'%Y-%m-%d') 
    p_fx_spot_rate = fx_spot_rate 
    p_domestic_discount_curve = domestic_discount_curve 
    p_foreign_discount_curve = foreign_discount_curve 
    p_volatility_surface = volatility_surface
    pb_input = dqCreateProtoFxDeltaToStrikeCalculationInput(p_delta_type, 
                                                            p_delta, 
                                                            p_option_type, 
                                                            p_expiry_date, 
                                                            p_fx_spot_rate, 
                                                            p_domestic_discount_curve, 
                                                            p_foreign_discount_curve, 
                                                            p_volatility_surface)

    req_name = 'FX_DELTA_TO_STRIKE_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxDeltaToStrikeCalculationOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.strike
        
###############################################################################
def fx_atm_strike_calculator(atm_type,
                             expiry_date, 
                             fx_spot_rate, 
                             domestic_discount_curve, 
                             foreign_discount_curve, 
                             volatility_surface):     
    '''
    @args:
        
        
    @return:
        
    '''
    p_atm_type = AtmType.DESCRIPTOR.value_by_name[option_type.upper()].number
    p_expiry_date = to_date(expiry_date,'%Y-%m-%d') 
    p_fx_spot_rate = fx_spot_rate 
    p_domestic_discount_curve = domestic_discount_curve 
    p_foreign_discount_curve = foreign_discount_curve 
    p_volatility_surface = volatility_surface
    pb_input = dqCreateProtoFxAtmStrikeCalculationInput(p_atm_type, 
                                                        p_expiry_date, 
                                                        p_fx_spot_rate, 
                                                        p_domestic_discount_curve, 
                                                        p_foreign_discount_curve, 
                                                        p_volatility_surface)    

    req_name = 'FX_ATM_STRIKE_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxAtmStrikeCalculationOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.strike
        
###############################################################################
def fx_option_date_calculator(as_of_date,
                              term,
                              currency_pair,
                              business_day_convention):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_business_day_convention = BusinessDayConvention.DESCRIPTOR.value_by_name[business_day_convention.upper()].number
    p_calculation_date = to_date(as_of_date,'%Y-%m-%d') 
    p_term = to_period(term) 
    p_currency_pair = to_currency_pair(currency_pair)
    pb_input = dqCreateProtoFxOptionDateCalculationInput(p_calculation_date, 
                                                         p_currency_pair, 
                                                         p_term, 
                                                         p_business_day_convention)

    req_name = 'FX_OPTION_DATE_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxOptionDateCalculationOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.expiry_date, pb_output.delivery_date
        
###############################################################################
def fx_swap_point_calculator(as_of_date,
                             currency_pair,
                             delivery_date,
                             fx_spot_rate,
                             domestic_discount_curve,
                             foreign_discount_curve):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_calculation_date = to_date(as_of_date,'%Y-%m-%d') 
    p_currency_pair = to_currency_pair(currency_pair)
    p_delivery_date = to_date(delivery_date,'%Y-%m-%d') 
    p_fx_spot_rate = fx_spot_rate 
    p_domestic_discount_curve = domestic_discount_curve 
    p_foreign_discount_curve = foreign_discount_curve 
    pb_input = dqCreateProtoFxSwapPointCalculationInput(p_calculation_date, 
                                                        p_currency_pair, 
                                                        p_delivery_date, 
                                                        p_fx_spot_rate, 
                                                        p_domestic_discount_curve, 
                                                        p_foreign_discount_curve)


    req_name = 'FX_SWAP_POINT_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxSwapPointCalculationOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.swap_point
        
###############################################################################
def fx_vol_calculator(fx_volatility_surface,
                      term_date,
                      strike):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_strike = strike
    p_term_date = to_date(term_date,'%Y-%m-%d') 
    p_fx_volatility_surface = fx_volatility_surface 
    pb_input = dqCreateProtoFxVolatilityCalculationInput(p_fx_volatility_surface, 
                                                         p_term_date, 
                                                         p_strike)


    req_name = 'FX_VOLATILITY_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxVolatilityCalculationOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.swap_point

###############################################################################
if __name__ == "__main__":
    as_of_date = '2021-05-28'
    mds = create_fx_mkt_data_set(as_of_date,
                           [IrYieldCurve(), IrYieldCurve()],
                           [FxSpotRate()],
                           [FxVolatilitySurface()])
    print(mds)
    
    ps = create_fx_pricing_settings(PricingModelSettings(),
                                    'ANALYTICAL',
                                    'CNY',
                                    PdeSettings(),
                                    MonteCarloSettings())
    print(ps)
    
    rs = create_fx_risk_settings(True,
                            True,
                            'b',
                            'b',
                            'b',
                            't',
                            False,
                            1.0e-2,
                            1.0e-2,
                            1.0e-4,
                            'CENTRAL_DIFFERENCE_METHOD',
                            'CENTRAL_DIFFERENCE_METHOD',
                            'CENTRAL_DIFFERENCE_METHOD',
                            'SINGLE_THREADING_MODE',
                            True)
    print(rs)