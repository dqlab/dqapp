# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 08:43:01 2021

@author: dzhu
"""

import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_currency_pair, to_date, to_period

###############################################################################
def create_fx_option_quote_matrix(as_of_date,
                                  currency_pair,
                                  quotes,
                                  quote_names,
                                  quote_terms):    
    '''
    @args:
        3. quotes: pandas.DataFrame
        
    @return:
        
    '''
    p_as_of_date = to_date(as_of_date, '%Y-%m-%d')
    p_currency_pair = to_currency_pair(currency_pair)
    p_terms = quote_terms
    p_quote_names = quote_names    
    quote_values = quotes
    p_rows = len(quote_terms)
    p_cols = len(quote_names)
    p_data = list(quote_values.flatten())
    
    p_storage_order = Matrix.StorageOrder.ColMajor
    p_quotes = dqCreateProtoMatrix(p_rows, p_cols, p_data, p_storage_order)    
    pb_input = dqCreateProtoCreateFxOptionQuoteMatrixInput(p_currency_pair, p_as_of_date, p_terms, p_quote_names, p_quotes)    
    req_name = 'CREATE_FX_OPTION_QUOTE_MATRIX'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
    pb_output = CreateFxOptionQuoteMatrixOutput()
    pb_output.ParseFromString(res_msg)    
    return pb_output.fx_option_quote_matrix
        
###############################################################################
def build_fx_vol_surface(as_of_date,
                         currency_pair,
                         market_conventions,
                         quote_matrix,
                         fx_spot_rate,
                         dom_discount_curve,
                         for_discount_curve,
                         vol_surf_definition,
                         name):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_reference_date = to_date(as_of_date, '%Y-%m-%d')
    p_currency_pair = to_currency_pair(currency_pair)
    
    p_atm_type = AtmType.DESCRIPTOR.values_by_name[market_conventions['atm_type'].upper()].number
    p_short_delta_type = FxDeltaType.DESCRIPTOR.values_by_name[market_conventions['short_delta_type'].upper()].number
    p_long_delta_type = FxDeltaType.DESCRIPTOR.values_by_name[market_conventions['long_delta_type'].upper()].number
    p_risk_reversal = FxRiskReversal.DESCRIPTOR.values_by_name[market_conventions['risk_reversal'].upper()].number
    p_smile_quote_type = FxSmileQuoteType.DESCRIPTOR.values_by_name[market_conventions['smile_quote_type'].upper()].number
    p_short_delta_cutoff = to_period(market_conventions['short_delta_cutoff'])
    p_market_conventions = dqCreateProtoFxMarketConventions(p_atm_type,
                                                            p_short_delta_type, 
                                                            p_long_delta_type, 
                                                            p_short_delta_cutoff, 
                                                            p_risk_reversal, 
                                                            p_smile_quote_type, 
                                                            p_currency_pair)
    p_quotes = quote_matrix
    p_fx_spot_rate = fx_spot_rate
    p_domestic_discount_curve = dom_discount_curve
    p_foreign_discount_curve = for_discount_curve
    
    p_vol_smile_type = VolSmileType.DESCRIPTOR.values_by_name[vol_surf_definition['vol_smile_type'].upper()].number
    p_smile_method = VolSmileMethod.DESCRIPTOR.values_by_name[vol_surf_definition['smile_method'].upper()].number
    p_smile_extrap_method = ExtrapMethod.DESCRIPTOR.values_by_name[vol_surf_definition['smile_extrap_method'].upper()].number
    p_time_interp_method = VolTermInterpMethod.DESCRIPTOR.values_by_name[vol_surf_definition['time_interp_method'].upper()].number
    p_time_extrap_method = VolTermExtrapMethod.DESCRIPTOR.values_by_name[vol_surf_definition['time_extrap_method'].upper()].number
    p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[vol_surf_definition['day_count_convention'].upper()].number
    p_vol_type = VolatilityType.DESCRIPTOR.values_by_name[vol_surf_definition['volatility_type'].upper()].number
    p_wing_strike_type = WingStrikeType.DESCRIPTOR.values_by_name[vol_surf_definition['wing_strike_type'].upper()].number
    p_lower = vol_surf_definition['lower_bound']
    p_upper = vol_surf_definition['upper_bound']
    p_definition = dqCreateProtoVolatilitySurfaceDefinition(p_vol_smile_type, 
                                                            p_smile_method, 
                                                            p_smile_extrap_method, 
                                                            p_time_interp_method, 
                                                            p_time_extrap_method, 
                                                            p_day_count_convention, 
                                                            p_vol_type, 
                                                            p_wing_strike_type, 
                                                            p_lower, 
                                                            p_upper)

    p_settings = dqCreateProtoVolatilitySurfaceBuildSettings(1, 0.5)
    p_name = name.upper()
    pb_input = dqCreateProtoFxVolatilitySurfaceBuildingInput(p_reference_date, 
                                                             p_currency_pair, 
                                                             p_market_conventions, 
                                                             p_quotes, 
                                                             p_fx_spot_rate, 
                                                             p_domestic_discount_curve, 
                                                             p_foreign_discount_curve, 
                                                             p_definition, 
                                                             p_settings, 
                                                             p_name)
    #print(pb_input)
    req_name = 'FX_VOLATILITY_SURFACE_BUILDER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    
    pb_output = FxVolatilitySurfaceBuildingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.fx_volatility_surface
        
###############################################################################
class FxVolMktDataManager:
    def __init__(self, 
                 as_of_date, 
                 fx_vol_surf_template_manager,
                 fx_option_mkt_convention_manager,
                 fx_vol_hist_data_manager,
                 fx_spot_mkt_data_manager,
                 ir_yield_curve_manager): 
               
        self.fx_vol_surfs = dict()        
        ccy_pairs = fx_vol_surf_template_manager.get_ccy_pairs()        
        for currency_pair in ccy_pairs:     
            terms = fx_vol_surf_template_manager.get_term_structure(currency_pair)
            atm_inst_type = fx_vol_surf_template_manager.get_atm_inst_type(currency_pair)
            otm_inst_types, otm_inst_strikes = fx_vol_surf_template_manager.get_otm_insts(currency_pair)
            quotes, quote_names = fx_vol_hist_data_manager.get_vol_matrix(currency_pair, terms, atm_inst_type, otm_inst_types, otm_inst_strikes, as_of_date)
            
            quote_matrix = create_fx_option_quote_matrix(as_of_date, currency_pair, quotes, quote_names, terms)  
            #print(quote_matrix)
            vol_surf_definition = fx_vol_surf_template_manager.get_definition(currency_pair)
            fx_spot_rate = fx_spot_mkt_data_manager.get_fx_spot_rate(currency_pair)
            dom_discount_curve = ir_yield_curve_manager.get_yield_curve(vol_surf_definition['domestic_discount_curve'])
            for_discount_curve = ir_yield_curve_manager.get_yield_curve(vol_surf_definition['foreign_discount_curve'])
            market_conventions = fx_option_mkt_convention_manager.get_mkt_convention(currency_pair)
            vol_surf = build_fx_vol_surface(as_of_date, currency_pair, market_conventions,
                                            quote_matrix,
                                            fx_spot_rate, dom_discount_curve, for_discount_curve,
                                            vol_surf_definition,
                                            currency_pair)
            self.fx_vol_surfs[currency_pair.upper()] = vol_surf
    
    def get_fx_vol_surface(self, ccy_pair):
        return self.fx_vol_surfs[ccy_pair.upper()]
    
###############################################################################
from calendarmanager import CalendarManager

from iborindexmanager import IborIndexManager
from irvanillainsttemplatemanager import IrVanillaInstTemplateManager
from iryieldcurvetemplatemanager import IrYieldCurveTemplateManager


from currencypairmanager import CurrencyPairManager
from fxspottemplatemanager import FxSpotTemplateManager
from fxswaptemplatemanager import FxSwapTemplateManager
from fxvolsurfacetemplatemanager import FxVolSurfaceTemplateManager
from fxoptionmktconventionmanager import FxOptionMktConventionManager

from irflowhistdatamanager import IrFlowHistDataManager
from fxcashhistdatamanager import FxCashHistDataManager
from fxvolhistdatamanager import FxVolHistDataManager

from fxspotmktdatamanager import FxSpotMktDataManager
from iryieldcurvemanager import IrYieldCurveManager
###############################################################################
if __name__ == "__main__":
    as_of_date = '2021-05-28'
    calendar_manager = CalendarManager()
    
    ibor_index_manager = IborIndexManager()    
    ir_vanilla_inst_template_manager = IrVanillaInstTemplateManager()
    ir_yield_curve_template_manager = IrYieldCurveTemplateManager()
    
    ccy_pair_manager = CurrencyPairManager()
    fx_spot_template_manager = FxSpotTemplateManager()
    fx_swap_template_manager = FxSwapTemplateManager()
    fx_option_mkt_convention_manager = FxOptionMktConventionManager()
    fx_vol_surf_template_manager = FxVolSurfaceTemplateManager()    
    
    ir_flow_hist_data_manager = IrFlowHistDataManager()
    fx_cash_hist_data_manager = FxCashHistDataManager()
    fx_vol_hist_data_manager = FxVolHistDataManager()
    
    fx_spot_mkt_data_manager = FxSpotMktDataManager(as_of_date, ccy_pair_manager, fx_cash_hist_data_manager)
    ir_yield_curve_manager = IrYieldCurveManager(as_of_date, ir_yield_curve_template_manager, ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_mkt_data_manager)
    
    fx_vol_surf_manager = FxVolMktDataManager(as_of_date, 
                 fx_vol_surf_template_manager,
                 fx_option_mkt_convention_manager,
                 fx_vol_hist_data_manager,
                 fx_spot_mkt_data_manager,
                 ir_yield_curve_manager)   
    print(fx_vol_surf_manager.fx_vol_surfs)