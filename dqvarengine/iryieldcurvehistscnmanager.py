# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 17:32:19 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 14:00:57 2021

@author: dzhu
"""
import numpy as np

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_date, to_excel_date, to_period
from iryieldcurvemanager import create_ir_yield_curve_build_settings, create_ir_par_rate_curve, build_ir_single_ccy_yield_curve, build_ir_cross_ccy_yield_curve

###############################################################################            
class IrYieldCurveHistScnManager:    
    def __init__(self, 
                 as_of_date,
                 sim_date,                 
                 num_sims,
                 change_type,
                 liquidity_horizon,
                 ir_yield_curve_template_manager,
                 ir_flow_hist_data_manager,
                 fx_cash_hist_data_manager,
                 fx_spot_hist_scn_manager):        
        self.yield_curves = dict()
        #dual single ccy curve construction:
        #self.__build_dual_single_ccy_curves(as_of_date, ir_yield_curve_template_manager, ir_flow_hist_data_manager)
        #mono single ccy curve construction:
        self.__build_mono_single_ccy_curves(as_of_date, sim_date, num_sims, change_type, liquidity_horizon, ir_yield_curve_template_manager, ir_flow_hist_data_manager)
        #cross ccy curve construction:
        self.__build_cross_ccy_curves(as_of_date, sim_date, num_sims, change_type, liquidity_horizon, ir_yield_curve_template_manager, ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_hist_scn_manager)
    
    def __build_mono_single_ccy_curves(self, 
                                       as_of_date,
                                       sim_date,                 
                                       num_sims,
                                       change_type,
                                       liquidity_horizon,
                                       ir_yield_curve_template_manager,
                                       ir_flow_hist_data_manager):   
        
        lowest_priority = ir_yield_curve_template_manager.get_lowest_priority()
        for priority in range(lowest_priority):
            curves = ir_yield_curve_template_manager.get_mono_single_ccy_curves_with_priority(priority)
            for curve_name in curves:
                currency, day_count, curve_type, interp_method, extrap_method, compounding_type, freq, to_settlement, ibor_index, cross_ccy, ccy_pair = ir_yield_curve_template_manager.get_definition(curve_name)
                build_method, calc_jacobian, mode = ir_yield_curve_template_manager.get_build_settings(curve_name)
                
                term_structure = ir_yield_curve_template_manager.get_term_structure(curve_name)
                curve_insts = ir_yield_curve_template_manager.get_curve_instruments(curve_name)
                if change_type.lower() == 'absolute':
                    data_type = 'change'
                else:
                    data_type = 'change_in_percent'
                hist_data = ir_flow_hist_data_manager.get_hist_data(curve_insts, as_of_date, -num_sims, data_type)                
                base_data = ir_flow_hist_data_manager.get_hist_data(curve_insts, as_of_date, 0, 'mid')
                
                for i in range(len(hist_data)):
                    term_structure.loc[:,'quote'] = base_data.iloc[0].to_numpy() + hist_data.iloc[i].to_numpy()  
                    par_curve = create_ir_par_rate_curve(sim_date, currency, term_structure, curve_name)
                    
                    discount_curve = ir_yield_curve_template_manager.get_discount_curve(curve_name)
                    forward_curve = ir_yield_curve_template_manager.get_forward_curve(curve_name)              
                    use_on_tn_fx_swap = False
                    build_settings = create_ir_yield_curve_build_settings(curve_name, curve_type, discount_curve, forward_curve, use_on_tn_fx_swap)                
                    
                    other_curve_names = ir_yield_curve_template_manager.get_dependent_curves(curve_name)
                    other_curves = list()
                    for other in other_curve_names:
                        other_curves.append(self.yield_curves[other])
                    
                    yield_curve = build_ir_single_ccy_yield_curve(sim_date, [curve_name], [build_settings], [par_curve], 
                                                                  [day_count], [compounding_type], [freq], [to_settlement],
                                                                  other_curves,
                                                                  build_method, calc_jacobian)
                    self.yield_curves[curve_name+'_'+str(i)] = yield_curve[0]                
                
    def __build_cross_ccy_curves(self, 
                                 as_of_date,
                                 sim_date,                 
                                 num_sims,
                                 change_type,
                                 liquidity_horizon,
                                 ir_yield_curve_template_manager,
                                 ir_flow_hist_data_manager,
                                 fx_cash_hist_data_manager,
                                 fx_spot_hist_scn_manager):
        curves = ir_yield_curve_template_manager.get_cross_ccy_curves()
        for curve_name in curves:
            currency, day_count, curve_type, interp_method, extrap_method, compounding_type, freq, to_settlement, ibor_index, cross_ccy, ccy_pair = ir_yield_curve_template_manager.get_definition(curve_name)
            build_method, calc_jacobian, mode = ir_yield_curve_template_manager.get_build_settings(curve_name)
                                            
            term_structure = ir_yield_curve_template_manager.get_term_structure(curve_name)   
            curve_insts = ir_yield_curve_template_manager.get_curve_instruments(curve_name)
            if change_type.lower() == 'absolute':
                data_type = 'change'
            else:
                data_type = 'change_in_percent'
            hist_data = fx_cash_hist_data_manager.get_hist_data(curve_insts, as_of_date, -num_sims, data_type)                
            base_data = fx_cash_hist_data_manager.get_hist_data(curve_insts, as_of_date, 0, 'mid')
                            
            for i in range(num_sims):
                term_structure.loc[:, 'quote'] = base_data.iloc[0].to_numpy() + hist_data.iloc[i].to_numpy()                 
                par_curve = create_ir_par_rate_curve(sim_date, currency, term_structure, curve_name)
                
                discount_curve = ir_yield_curve_template_manager.get_discount_curve(curve_name)
                forward_curve = ir_yield_curve_template_manager.get_forward_curve(curve_name)     
                use_on_tn_fx_swap = False
                inst_terms = term_structure['instrument_term'].str.lower().tolist()            
                if  'on' in inst_terms and 'tn' in inst_terms:
                    use_on_tn_fx_swap = True
                build_settings = create_ir_yield_curve_build_settings(curve_name, curve_type, discount_curve, forward_curve, use_on_tn_fx_swap)
                                
                other_curves = list()
                other_curve_names = ir_yield_curve_template_manager.get_dependent_curves(curve_name)
                for other in other_curve_names:
                    other_curves.append(self.yield_curves[other + '_' + str(i)])               
                
                fx_spot = fx_spot_hist_scn_manager.get_fx_spot_rate(ccy_pair, i)
                yield_curve = build_ir_cross_ccy_yield_curve(sim_date, [curve_name], [build_settings], [par_curve], 
                                                             [day_count], [compounding_type], [freq], [to_settlement], 
                                                             other_curves, fx_spot)
                                
                self.yield_curves[curve_name+'_'+str(i)] = yield_curve[0]            
                
    def __build_dual_single_ccy_curves(self, 
                                       as_of_date,
                                       sim_date,                 
                                       num_sims,
                                       change_type,
                                       liquidity_horizon,
                                       ir_yield_curve_template_manager,
                                       ir_flow_hist_data_manager):        
        dual_curves = ir_yield_curve_template_manager.get_dual_curves()        
        for pair in dual_curves:
            curve_names = pair            
            build_settings = list()
            day_counts = list()
            compounding_types = list()
            freqs = list()
            to_settlements = list()
            other_curves = []
            build_method = 'global_optimization_method'
            calc_jacobian = False
            use_on_tn_fx_swap = False
            hist_data = dict()
            base_data = dict()
            term_structure = dict()
            for curve_name in curve_names:
                currency, day_count, curve_type, interp_method, extrap_method, compounding_type, frequency, to_settlement, ibor_index, cross_ccy, ccy_pair = ir_yield_curve_template_manager.get_definition(curve_name)
                build_method, calc_jacobian, mode = ir_yield_curve_template_manager.get_build_settings(curve_name)
                
                discount_curve = ir_yield_curve_template_manager.get_discount_curve(curve_name)
                forward_curve = ir_yield_curve_template_manager.get_forward_curve(curve_name)     
                use_on_tn_fx_swap = False            
                build_settings.append(create_ir_yield_curve_build_settings(curve_name, curve_type, discount_curve, forward_curve, use_on_tn_fx_swap))
                
                day_counts.append(day_count)
                compounding_types.append(compounding_type)
                freqs.append(frequency)
                to_settlements.append(to_settlement)
                    
                term_structure[curve_name] = ir_yield_curve_template_manager.get_term_structure(curve_name)   
                curve_insts = ir_yield_curve_template_manager.get_curve_instruments(curve_name)                
                if change_type.lower() == 'absolute':
                    data_type = 'change'
                else:
                    data_type = 'change_in_percent'
                    
                hist_data[curve_name] = ir_flow_hist_data_manager.get_hist_data(curve_insts, as_of_date, -num_sims, data_type)                
                base_data[curve_name] = ir_flow_hist_data_manager.get_hist_data(curve_insts, as_of_date, 0, 'mid')                
           
            for i in range(len(num_sims)):
               par_curves = list()
               for curve_name in curve_names:
                   term_structure[curve_name].loc[:,'quote'] = base_data[curve_name].iloc[0].to_numpy() + hist_data[curve_name].iloc[i].to_numpy()                 
                   par_curves.append(create_ir_par_rate_curve(as_of_date, currency, term_structure, curve_name))
                
                yield_curves = build_ir_single_ccy_yield_curve(as_of_date, curve_names, build_settings, par_curves, 
                                                               day_counts, compounding_types, freqs, to_settlements,
                                                               other_curves,
                                                               build_method, calc_jacobian)
                for i in range(len(pair)):
                    self.yield_curves[pair[i] + '_' + str(i)] = yield_curves[i]
                
    def get_yield_curve(self, curve_name, scn_num):
        return self.yield_curves[curve_name.upper()+'_'+str(scn_num)]
    
###############################################################################
from calendarmanager import CalendarManager
       
from iborindexmanager import IborIndexManager
from irvanillainsttemplatemanager import IrVanillaInstTemplateManager
from iryieldcurvetemplatemanager import IrYieldCurveTemplateManager

from currencypairmanager import CurrencyPairManager
from fxspottemplatemanager import FxSpotTemplateManager
from fxswaptemplatemanager import FxSwapTemplateManager

from irflowhistdatamanager import IrFlowHistDataManager
from fxcashhistdatamanager import FxCashHistDataManager

from fxspothistscnmanager import FxSpotHistScnManager
###############################################################################
if __name__ == "__main__":
    as_of_date = '2021-07-22'
    calendar_manager = CalendarManager()
    
    ibor_manager = IborIndexManager()
    ir_vanilla_inst_template_manager = IrVanillaInstTemplateManager()       
    ir_yield_curve_template_manager = IrYieldCurveTemplateManager()
    
    ccy_pair_manager = CurrencyPairManager()
    fx_spot_template_manager = FxSpotTemplateManager()
    fx_swap_template_manger = FxSwapTemplateManager()
    
    ir_flow_hist_data_manager = IrFlowHistDataManager()
    fx_cash_hist_data_manager = FxCashHistDataManager()  
       
    sim_date = '2021-07-23'
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
    print(ir_yield_curve_hist_scn_manager.yield_curves)
    