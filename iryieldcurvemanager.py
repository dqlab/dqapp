# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 14:00:57 2021

@author: dzhu
"""
import sys

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_date, to_excel_date, to_period

###############################################################################
def create_flat_ir_yield_curve(as_of_date,
                               ccy,
                               rate,
                               name):
    '''
    @args:
        
    @return:
        
    '''
    try:
        p_reference_date = to_date(as_of_date, '%Y-%m-%d')
        p_currency = CurrencyName.DESCRIPTOR.values_by_name[ccy.upper()].number
        p_zero_rate = rate
        p_day_count_convention = ACT_365_FIXED
        p_curve_name = name.upper()
        pb_input = dqCreateProtoCreateDefaultFlatIrYieldCurveInput(p_reference_date, 
                                                                   p_currency, 
                                                                   p_zero_rate, 
                                                                   p_day_count_convention, 
                                                                   p_curve_name)  
            
        req_name = 'CREATE_DEFAULT_FLAT_IR_YIELD_CURVE'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())   
        
        if res_msg == None:
            raise Exception('CREATE_DEFAULT_FLAT_IR_YIELD_CURVE ProcessRequest: failed!')
        pb_output = CreateDefaultFlatIrYieldCurveOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.ir_yield_curve
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))

###############################################################################
def create_ir_par_rate_curve(as_of_date,
                             currency,
                             pillar_data,
                             curve_name):
    '''
    @args:
        3. pillar_data: pandas.DataFrame, columns=['inst_name','inst_type','inst_term','factor','quote']
        
    @return:s
        dqproto.IrParRateCurve
    '''
    p_as_of_date = to_date(as_of_date, '%Y-%m-%d')
    p_currency = CurrencyName.DESCRIPTOR.values_by_name[currency.upper()].number
    p_inst_names = list(pillar_data['instrument_name'])
    p_inst_types = list(pillar_data['instrument_type'])
    p_inst_terms = list(pillar_data['instrument_term'])
    p_factors = list(pillar_data['quote_factor'])
    p_quotes = list(pillar_data['quote'])
    p_start_conventions = list()
    for i in range(len(p_inst_terms)):
        start_convention = 'spotstart'
        if p_inst_terms[i].lower() == 'on':
            start_convention = 'todaystart'
        elif p_inst_terms[i].lower() == 'tn':
            start_convention = 'tomorrowstart'
        else:
            start_convention = 'spotstart'                
        p_start_conventions.append(start_convention.upper())        
    
    p_curve_name = curve_name.upper()
    pb_input = dqCreateProtoCreateIrParRateCurveInput(p_as_of_date, 
                                                      p_currency, 
                                                      p_curve_name, 
                                                      p_inst_names, 
                                                      p_inst_types, 
                                                      p_inst_terms, 
                                                      p_factors, 
                                                      p_quotes, 
                                                      p_start_conventions)
    
    req_name = 'CREATE_IR_PAR_RATE_CURVE'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
    
    pb_output = CreateIrParRateCurveOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.ir_par_rate_curve      
        
###############################################################################
def create_ir_yield_curve_build_settings(curve_name,
                                         curve_type,
                                         discount_curve_settings,
                                         fwd_curve_settings,
                                         use_on_tn_fx_swap):
    '''
    @args:
        3. 
        4. discount_curve_settings: dictionary, where key is currency, and value is discount curve name
        5. fwd_curve_settings: list of 2 string elements, where [0]: reference index; [1]: curve name
    @return:
        dqproto.BondYieldCurveBuildSettings
    '''
    p_discount_curve_settings = list()
    for ccy in discount_curve_settings.keys():
        p_currency_name = CurrencyName.DESCRIPTOR.values_by_name[ccy.upper()].number
        p_curve_name = discount_curve_settings[ccy].lower()
        p_discount_curve_settings.append(dqCreateProtoCreateIrYieldCurveBuildSettingsInput_DiscountCurveSettings(p_currency_name, 
                                                                                                                 p_curve_name))
    
    p_forward_curve_settings = list()
    for ibor in fwd_curve_settings.keys():
        p_index_name = IborIndexName.DESCRIPTOR.values_by_name[ibor.upper()].number
        p_curve_name = fwd_curve_settings[ibor].lower()
        p_forward_curve_settings.append(dqCreateProtoCreateIrYieldCurveBuildSettingsInput_ForwardCurveSettings(p_index_name, 
                                                                                                               p_curve_name))
              
    p_curve_name = curve_name.lower()
    #p_curve_type = IrYieldCurveType.DESCRIPTOR.values_by_name[curve_type.upper()].number
    p_use_on_tn_fx_swap = bool(use_on_tn_fx_swap)
    pb_input = dqCreateProtoCreateIrYieldCurveBuildSettingsInput(p_curve_name, 
                                                                          p_use_on_tn_fx_swap, 
                                                                          p_discount_curve_settings, 
                                                                          p_forward_curve_settings)
    req_name = 'CREATE_IR_YIELD_CURVE_BUILD_SETTINGS'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
    
    pb_output = CreateIrYieldCurveBuildSettingsOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.ir_yield_curve_build_settings      
        
###############################################################################        
def build_ir_single_ccy_yield_curve(as_of_date,
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
    p_build_settings = list()
    for i in range(len(curve_name)):
        p_target_curve_name = curve_name[i].lower()
        p_ir_yield_curve_build_settings = build_settings[i]        
        p_par_curve = par_curve[i]
        p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[day_count[i].upper()].number
        p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[compounding_type[i].upper()].number
        p_frequency = Frequency.DESCRIPTOR.values_by_name[freq[i].upper()].number
        p_to_settlement = bool(to_settlement[i])
        pb_settings_container = dqCreateProtoIrSingleCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(
                p_target_curve_name, 
                p_ir_yield_curve_build_settings, 
                p_par_curve, 
                p_day_count_convention, 
                p_compounding_type, 
                p_frequency, 
                p_to_settlement)
        p_build_settings.append(pb_settings_container)
    
    p_reference_date = to_date(as_of_date, '%Y-%m-%d')
    p_other_curves = other_curves        
    p_curve_building_method = IrYieldCurveBuildingMethod.DESCRIPTOR.values_by_name[build_method.upper()].number
    p_calc_jacobian = bool(calc_jacobian)
    pb_input = dqCreateProtoIrSingleCurrencyCurveBuildingInput(p_reference_date, 
                                                               p_build_settings, 
                                                               p_other_curves, 
                                                               p_curve_building_method)  
    req_name = 'IR_SINGLE_CURRENCY_CURVE_BUILDER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('IR_SINGLE_CURRENCY_CURVE_BUILDER ProcessRequest: failed!')
    pb_output = IrSingleCurrencyCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.target_curves

###############################################################################        
def build_ir_cross_ccy_yield_curve(as_of_date,
                                   curve_name,
                                   build_settings,
                                   par_curve,
                                   day_count,
                                   compounding_type,
                                   freq,
                                   to_settlement,
                                   other_curves,
                                   fx_spot):
    '''
    @args:
        3. build_settings: dqproto.BondYieldCurveBuildSettings
        4. par_curve: dqproto.BondParCurve
        5. day_count: string
        9. other_curves: list of dqproto.IrYieldCurve
    @return:
        dqproto.IrYieldCurve
    '''
    p_build_settings = list()
    for i in range(len(curve_name)):
        p_target_curve_name = curve_name[i].lower()
        p_ir_yield_curve_build_settings = build_settings[i]
        p_par_curve = par_curve[i]
        p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[day_count[i].upper()].number
        p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[compounding_type[i].upper()].number
        p_frequency = Frequency.DESCRIPTOR.values_by_name[freq[i].upper()].number
        p_to_settlement = bool(to_settlement[i])
        pb_settings_container = dqCreateProtoIrCrossCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(
                p_target_curve_name, 
                p_ir_yield_curve_build_settings, 
                p_par_curve, 
                p_day_count_convention, 
                p_compounding_type, 
                p_frequency, 
                p_to_settlement)
        p_build_settings.append(pb_settings_container)
    
    p_reference_date = to_date(as_of_date, '%Y-%m-%d')
    p_other_curves = other_curves        
    p_fx_spot = fx_spot
    pb_input = dqCreateProtoIrCrossCurrencyCurveBuildingInput(p_reference_date, 
                                                              p_build_settings, 
                                                              p_other_curves, 
                                                              p_fx_spot)
    
    req_name = 'IR_CROSS_CURRENCY_CURVE_BUILDER'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('IR_CROSS_CURRENCY_CURVE_BUILDER ProcessRequest: failed!')
    pb_output = IrCrossCurrencyCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    
    return pb_output.target_curves
        
###############################################################################            
class IrYieldCurveManager:    
    def __init__(self, 
                 as_of_date,
                 ir_yield_curve_template_manager,
                 ir_flow_hist_data_manager,
                 fx_cash_hist_data_manager,
                 fx_mkt_data_manager):        
        self.yield_curves = dict()
        #dual single ccy curve construction:
        self.__build_dual_single_ccy_curves(as_of_date, ir_yield_curve_template_manager, ir_flow_hist_data_manager)
        #mono single ccy curve construction:
        self.__build_mono_single_ccy_curves(as_of_date, ir_yield_curve_template_manager, ir_flow_hist_data_manager)
        #cross ccy curve construction:
        self.__build_cross_ccy_curves(as_of_date, ir_yield_curve_template_manager, ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_mkt_data_manager)
    
    def __build_mono_single_ccy_curves(self, 
                                       as_of_date,
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
                
                term_structure['quote'] = list(ir_flow_hist_data_manager.get_data(curve_insts, as_of_date, as_of_date).loc[as_of_date])   
                par_curve = create_ir_par_rate_curve(as_of_date, currency, term_structure, curve_name)
                
                discount_curve = ir_yield_curve_template_manager.get_discount_curve(curve_name)
                forward_curve = ir_yield_curve_template_manager.get_forward_curve(curve_name)              
                use_on_tn_fx_swap = False
                build_settings = create_ir_yield_curve_build_settings(curve_name, curve_type, discount_curve, forward_curve, use_on_tn_fx_swap)                
                
                other_curve_names = ir_yield_curve_template_manager.get_dependent_curves(curve_name)
                other_curves = list()
                for other in other_curve_names:
                    other_curves.append(self.yield_curves[other])
                
                yield_curve = build_ir_single_ccy_yield_curve(as_of_date, [curve_name], [build_settings], [par_curve], 
                                                              [day_count], [compounding_type], [freq], [to_settlement],
                                                              other_curves,
                                                              build_method, calc_jacobian)
                self.yield_curves[curve_name] = yield_curve[0]                
                
    def __build_cross_ccy_curves(self, 
                                 as_of_date,
                                 ir_yield_curve_template_manager,
                                 ir_flow_hist_data_manager,
                                 fx_cash_hist_data_manager,
                                 fx_mkt_data_manager):
        curves = ir_yield_curve_template_manager.get_cross_ccy_curves()
        for curve_name in curves:
            currency, day_count, curve_type, interp_method, extrap_method, compounding_type, freq, to_settlement, ibor_index, cross_ccy, ccy_pair = ir_yield_curve_template_manager.get_definition(curve_name)
            build_method, calc_jacobian, mode = ir_yield_curve_template_manager.get_build_settings(curve_name)
                                            
            term_structure = ir_yield_curve_template_manager.get_term_structure(curve_name)   
            curve_insts = ir_yield_curve_template_manager.get_curve_instruments(curve_name)
            term_structure['quote'] = list(fx_cash_hist_data_manager.get_data(curve_insts, as_of_date, as_of_date).loc[as_of_date])                 
            par_curve = create_ir_par_rate_curve(as_of_date, currency, term_structure, curve_name)
            
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
                other_curves.append(self.yield_curves[other])               
            
            fx_spot = fx_mkt_data_manager.get_fx_spot_rate(ccy_pair)
            yield_curve = build_ir_cross_ccy_yield_curve(as_of_date, [curve_name], [build_settings], [par_curve], 
                                                         [day_count], [compounding_type], [freq], [to_settlement], 
                                                         other_curves, fx_spot)
                            
            self.yield_curves[curve_name] = yield_curve[0]            
                
    def __build_dual_single_ccy_curves(self, 
                                       as_of_date,
                                       ir_yield_curve_template_manager,
                                       ir_flow_hist_data_manager):        
        dual_curves = ir_yield_curve_template_manager.get_dual_curves()        
        for pair in dual_curves:
            curve_names = pair            
            build_settings = list()
            par_curves = list()
            day_counts = list()
            compounding_types = list()
            freqs = list()
            to_settlements = list()
            other_curves = []
            build_method = 'global_optimization_method'
            calc_jacobian = False
            use_on_tn_fx_swap = False
            
            for curve_name in curve_names:
                currency, day_count, curve_type, interp_method, extrap_method, compounding_type, frequency, to_settlement, ibor_index, cross_ccy, ccy_pair = ir_yield_curve_template_manager.get_definition(curve_name)
                build_method, calc_jacobian, mode = ir_yield_curve_template_manager.get_build_settings(curve_name)
                
                term_structure = ir_yield_curve_template_manager.get_term_structure(curve_name)   
                curve_insts = ir_yield_curve_template_manager.get_curve_instruments(curve_name)                
                term_structure['quote'] = list(ir_flow_hist_data_manager.get_data(curve_insts, as_of_date, as_of_date).loc[as_of_date])                 
                par_curves.append(create_ir_par_rate_curve(as_of_date, currency, term_structure, curve_name))
                
                discount_curve = ir_yield_curve_template_manager.get_discount_curve(curve_name)
                forward_curve = ir_yield_curve_template_manager.get_forward_curve(curve_name)     
                use_on_tn_fx_swap = False            
                build_settings.append(create_ir_yield_curve_build_settings(curve_name, curve_type, discount_curve, forward_curve, use_on_tn_fx_swap))
                
                day_counts.append(day_count)
                compounding_types.append(compounding_type)
                freqs.append(frequency)
                to_settlements.append(to_settlement)
            yield_curves = build_ir_single_ccy_yield_curve(as_of_date, curve_names, build_settings, par_curves, 
                                                           day_counts, compounding_types, freqs, to_settlements,
                                                           other_curves,
                                                           build_method, calc_jacobian)
            for i in range(len(pair)):
                self.yield_curves[pair[i]] = yield_curves[i]
                
    def get_yield_curve(self, curve_name):
        return self.yield_curves[curve_name.upper()]
    
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

from fxspotmktdatamanager import FxSpotMktDataManager
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
    
    fx_spot_mkt_data_manager = FxSpotMktDataManager(as_of_date, ccy_pair_manager, fx_cash_hist_data_manager)
    ir_yield_curve_manager = IrYieldCurveManager(as_of_date,
                                                 ir_yield_curve_template_manager,
                                                 ir_flow_hist_data_manager,
                                                 fx_cash_hist_data_manager,
                                                 fx_spot_mkt_data_manager)
    print(ir_yield_curve_manager.yield_curves)
    