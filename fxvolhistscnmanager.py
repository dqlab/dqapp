# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 08:43:01 2021

@author: dzhu
"""

import pandas as pd
import numpy as np

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_currency_pair, to_date, to_period
from fxvolmktdatamanager import create_fx_option_quote_matrix, build_fx_vol_surface

###############################################################################
class FxVolHistScnManager:
    def __init__(self, 
                 as_of_date, sim_date,  num_sims, change_type, liquidity_horizon,
                 fx_vol_surf_template_manager,
                 fx_option_mkt_convention_manager,
                 fx_vol_hist_data_manager,
                 fx_spot_hist_scn_manager,
                 ir_yield_curve_hist_scn_manager): 
               
        self.fx_vol_surfs = dict()        
        ccy_pairs = fx_vol_surf_template_manager.get_ccy_pairs()        
        for currency_pair in ccy_pairs:     
            terms = fx_vol_surf_template_manager.get_term_structure(currency_pair)
            atm_inst_type = fx_vol_surf_template_manager.get_atm_inst_type(currency_pair)
            otm_inst_types, otm_inst_strikes = fx_vol_surf_template_manager.get_otm_insts(currency_pair)
            if change_type.lower() == 'absolute':
                data_type = 'change'
            else:
                data_type = 'change_in_percent'
            
            base_quotes, base_quote_names = fx_vol_hist_data_manager.get_vol_matrix(currency_pair, terms, atm_inst_type, otm_inst_types, otm_inst_strikes, as_of_date, 'mid')
                
            for i in range(num_sims):
                hist_changes, quote_names = fx_vol_hist_data_manager.get_vol_matrix(currency_pair, terms, atm_inst_type, otm_inst_types, otm_inst_strikes, as_of_date, data_type)
                if change_type.lower() == 'relateive':
                    quotes = base_quotes + np.multiply(base_quotes, hist_changes)
                else:
                    quotes = base_quotes + hist_changes
                quote_matrix = create_fx_option_quote_matrix(sim_date, currency_pair, quotes, quote_names, terms)  
                
                vol_surf_definition = fx_vol_surf_template_manager.get_definition(currency_pair)
                fx_spot_rate = fx_spot_hist_scn_manager.get_fx_spot_rate(currency_pair, i)
                dom_discount_curve = ir_yield_curve_hist_scn_manager.get_yield_curve(vol_surf_definition['domestic_discount_curve'], i)
                for_discount_curve = ir_yield_curve_hist_scn_manager.get_yield_curve(vol_surf_definition['foreign_discount_curve'], i)
                market_conventions = fx_option_mkt_convention_manager.get_mkt_convention(currency_pair)
                vol_surf = build_fx_vol_surface(sim_date, currency_pair, market_conventions,
                                                quote_matrix,
                                                fx_spot_rate, dom_discount_curve, for_discount_curve,
                                                vol_surf_definition,
                                                currency_pair)
                self.fx_vol_surfs[currency_pair.upper() + '_' + str(i)] = vol_surf
    
    def get_fx_vol_surface(self, ccy_pair, scn_num):
        return self.fx_vol_surfs[ccy_pair.upper()+ '_' + str(scn_num)]
    
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

from fxspothistscnmanager import FxSpotHistScnManager
from iryieldcurvehistscnmanager import IrYieldCurveHistScnManager
###############################################################################
if __name__ == "__main__":
    as_of_date = '2021-05-21'
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
    
    sim_date = '2021-05-22'
    num_sims = 10
    change_type = 'absolute'
    liquidity_horizon = 1
    fx_spot_hist_scn_manger = FxSpotHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon,
                                                   ccy_pair_manager, fx_cash_hist_data_manager) 
    ir_yield_curve_hist_scn_manager = IrYieldCurveHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon,
                                                 ir_yield_curve_template_manager,
                                                 ir_flow_hist_data_manager,
                                                 fx_cash_hist_data_manager,
                                                 fx_spot_hist_scn_manger)
    
    fx_vol_surf_manager = FxVolHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon,
                 fx_vol_surf_template_manager,
                 fx_option_mkt_convention_manager,
                 fx_vol_hist_data_manager,
                 fx_spot_hist_scn_manger,
                 ir_yield_curve_hist_scn_manager)   
    print(fx_vol_surf_manager.fx_vol_surfs)