# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 02:44:28 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 17:44:24 2021

@author: dzhu
"""
import sys
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from staticdata import create_static_data, load_src_static_data
from utility import save_pb_data, to_period, to_calendar_name_list

###############################################################################
class IrYieldCurveTemplateManager:
    def __init__(self):
        data_loc = 'interestrate/market/ir_yield_curve'
        
        self.definition = load_src_static_data(data_loc,'definition')
        self.definition.columns = self.definition.columns.str.lower()
        self.definition = self.definition.set_index('curve_id')
        
        self.term_structure = load_src_static_data(data_loc, 'term_structure')
        self.term_structure.columns = self.term_structure.columns.str.lower()
        self.term_structure = self.term_structure.set_index('curve_id')
        
        self.build_settings = load_src_static_data(data_loc, 'build_settings')
        self.build_settings.columns = self.build_settings.columns.str.lower()
        self.build_settings = self.build_settings.set_index('curve_id')
        
        self.curve_assignment = load_src_static_data(data_loc, 'curve_assignment')
        self.curve_assignment.columns = self.curve_assignment.columns.str.lower()
        for i in range(len(self.curve_assignment)):
            curve_id = self.curve_assignment.iloc[i]['curve_id']
            curve_usuage = self.curve_assignment.iloc[i]['curve_usage']
            self.curve_assignment.iloc[i]['curve_assignment_id'] = self.__create_curve_assignment_id(curve_id, curve_usuage)
        self.curve_assignment = self.curve_assignment.set_index('curve_assignment_id')
                
        self.curve_names = list(self.definition.index)
        priorities = list()
        for curve_name in self.curve_names:
            priorities.append(self.__get_curve_priority(curve_name))
        self.definition['priority'] = priorities
        
    def __create_curve_assignment_id(self, curve_id, curve_usuage):
        return curve_id.upper() + '_' + curve_usuage.upper()
    
    def __get_curve_priority(self, curve_name):
        dependent_curves = self.get_dependent_curves(curve_name)
        priority = 0
        for curve in dependent_curves:
            priority = max(priority, self.__get_curve_priority(curve) + 1)
        return priority
    
    def get_definition(self, curve_name):
        curve_name = curve_name.upper()
        ccy = str(self.definition.loc[curve_name]['currency'])
        day_count = str(self.definition.loc[curve_name]['day_count_convention'])
        curve_type = str(self.definition.loc[curve_name]['curve_type'])
        interp_method = str(self.definition.loc[curve_name]['interp_method'])
        extrap_method = str(self.definition.loc[curve_name]['extrap_method'])
        compounding_type = str(self.definition.loc[curve_name]['compounding_type'])
        frequency = str(self.definition.loc[curve_name]['frequency'])
        to_settlement = bool(self.definition.loc[curve_name]['to_settlement'])
        ibor_index = str(self.definition.loc[curve_name]['ibor_index'])
        cross_ccy = bool(self.definition.loc[curve_name]['cross_currency'])
        ccy_pair = str(self.definition.loc[curve_name]['currency_pair'])
        return ccy, day_count, curve_type, interp_method, extrap_method, compounding_type, frequency, to_settlement, ibor_index, cross_ccy, ccy_pair
       
    def get_build_settings(self, curve_name):         
        build_method =  str(self.build_settings.loc[curve_name.upper()]['build_method'])
        jacobian = bool(self.build_settings.loc[curve_name.upper()]['jacobian'])
        mode = bool(self.build_settings.loc[curve_name.upper()]['mode'])
        return build_method, jacobian, mode
    
    def get_discount_curve(self, curve_id):  
        curve_usage = 'DISCOUNT_CURVE'              
        discount_curve = pd.DataFrame(self.curve_assignment[(self.curve_assignment['curve_id']==curve_id.upper()) 
                                                             & (self.curve_assignment['curve_usage']==curve_usage)])
        dc_settings = dict()
        for i in range(len(discount_curve)):
            dc_settings[discount_curve.iloc[i]['assignee']] = discount_curve.iloc[i]['assigned_curve']
        
        return dc_settings     
    
    def get_forward_curve(self, curve_id):                 
        curve_usage = 'FORWARD_CURVE'              
        fwd_curve = pd.DataFrame(self.curve_assignment[(self.curve_assignment['curve_id']==curve_id.upper()) 
                                                             & (self.curve_assignment['curve_usage']==curve_usage)])
        fc_settings = dict()
        for i in range(len(fwd_curve)):
            fc_settings[fwd_curve.iloc[i]['assignee']] = fwd_curve.iloc[i]['assigned_curve']        
        return fc_settings

    def get_term_structure(self, curve_name):
        return self.term_structure.loc[curve_name.upper()]       
    
    def get_curve_priority(self, curve_name):
        return int(self.definition.loc[curve_name.upper()]['priority'])
    
    def get_lowest_priority(self):
        return self.definition['priority'].max()
    
    def get_curves(self, priority):
        return list(self.definition[self.definition['priority']==priority].index)
    
    def get_dependent_curves(self, curve_name):
        curves = set(self.curve_assignment[self.curve_assignment['curve_id'] == curve_name.upper()]['assigned_curve'])        
        curves.remove(curve_name.upper())
        team_curve = str(self.build_settings.loc[curve_name]['other_curve'])
        if team_curve != 'nan':
            curves.remove(team_curve)
        return list(curves)
    
    def get_dual_curves(self):
        dual_curves = dict()
        tmp = pd.DataFrame(self.build_settings[self.build_settings['mode'] == 'DUAL'])
        for i in range(len(tmp)):
            first = tmp.index
            second = tmp.iloc[i]['other_curve']
            if second not in dual_curves:
                dual_curves[first] = second            
        dual_curve_list = list()
        for curve in dual_curves.keys():
            dual_curve_list.append([curve, dual_curves[curve]])
        return dual_curve_list
    
    def get_mono_single_ccy_curves(self):
        curves = set(self.definition.index)
        dual_curves = self.get_dual_curves()
        if len(dual_curves) > 0:
            curves.remove(dual_curves)
        cross_ccy_curves = self.get_cross_ccy_curves()
        if len(cross_ccy_curves) > 0:
            curves = curves.difference(cross_ccy_curves)
        return list(curves)
    
    def get_mono_single_ccy_curves_with_priority(self, priority):
        curves = set(self.get_curves(priority))
        dual_curves = self.get_dual_curves()
        if len(dual_curves) > 0:
            curves.remove(dual_curves)
        cross_ccy_curves = self.get_cross_ccy_curves()
        if len(cross_ccy_curves) > 0:
            curves = curves.difference(cross_ccy_curves)
        return list(curves)
    
    def get_cross_ccy_curves(self):
        curves = list(self.definition[self.definition['cross_currency']==True].index)
        return curves
    
    def get_all_curve_instruments(self):
        instruments = pd.DataFrame()  
        for curve in self.curve_names:
            pillars = self.get_term_structure(curve)
            instruments = pd.concat([instruments, pillars[['instrument_type', 'instrument_name', 'instrument_term']]], ignore_index=False, sort=False)
                
        return instruments
    
    def get_curve_instruments(self, curve_id):
        instruments = pd.DataFrame()         
        pillars = self.get_term_structure(curve_id)
        instruments = pd.concat([instruments, pillars[['instrument_type', 'instrument_name', 'instrument_term']]], ignore_index=False, sort=False)
        return instruments

###############################################################################
if __name__ == "__main__":
    ir_curve_template_manager = IrYieldCurveTemplateManager()
    
    print('Definition of CNY_FR_007:', ir_curve_template_manager.get_definition('CNY_FR_007'))
    print('Build settings of CNY_FR_007:', ir_curve_template_manager.get_build_settings('CNY_FR_007'))
    print('Term Structure of CNY_FR_007:', ir_curve_template_manager.get_term_structure('CNY_FR_007'))
    print('Discount curve of CNY_FR_007:', ir_curve_template_manager.get_discount_curve('CNY_FR_007'))
    print('Forward curve of CNY_FR_007:', ir_curve_template_manager.get_forward_curve('CNY_FR_007'))
    print('Priority of CNY_FR_007:', ir_curve_template_manager.get_curve_priority('CNY_FR_007'))
    print('Curve dependency of CNY_FR_007:', ir_curve_template_manager.get_dependent_curves('CNY_FR_007'))
    print('Curve instruments of CNY_FR_007:', ir_curve_template_manager.get_curve_instruments('CNY_FR_007'))
    
    print('Definition of CNY_SHIBOR_3M:', ir_curve_template_manager.get_definition('CNY_SHIBOR_3M'))
    print('Build settings of CNY_SHIBOR_3M:', ir_curve_template_manager.get_build_settings('CNY_SHIBOR_3M'))
    print('Term Structure of CNY_SHIBOR_3M:', ir_curve_template_manager.get_term_structure('CNY_SHIBOR_3M'))
    print('Discount curve of CNY_SHIBOR_3M:', ir_curve_template_manager.get_discount_curve('CNY_SHIBOR_3M'))
    print('Forward curve of CNY_SHIBOR_3M:', ir_curve_template_manager.get_forward_curve('CNY_SHIBOR_3M'))
    print('Priority of CNY_SHIBOR_3M:', ir_curve_template_manager.get_curve_priority('CNY_SHIBOR_3M'))
    print('Curve dependency of CNY_SHIBOR_3M:', ir_curve_template_manager.get_dependent_curves('CNY_SHIBOR_3M'))
    print('Curve instruments of CNY_SHIBOR_3M:', ir_curve_template_manager.get_curve_instruments('CNY_SHIBOR_3M'))
    
    print('Definition of USD_USDCNY_FX:', ir_curve_template_manager.get_definition('USD_USDCNY_FX'))
    print('Build settings of USD_USDCNY_FX:', ir_curve_template_manager.get_build_settings('USD_USDCNY_FX'))
    print('Term Structure of USD_USDCNY_FX:', ir_curve_template_manager.get_term_structure('USD_USDCNY_FX'))
    print('Discount curve of USD_USDCNY_FX:', ir_curve_template_manager.get_discount_curve('USD_USDCNY_FX'))
    print('Forward curve of USD_USDCNY_FX:', ir_curve_template_manager.get_forward_curve('USD_USDCNY_FX'))
    print('Priority of USD_USDCNY_FX:', ir_curve_template_manager.get_curve_priority('USD_USDCNY_FX'))
    print('Curve dependency of USD_USDCNY_FX:', ir_curve_template_manager.get_dependent_curves('USD_USDCNY_FX'))
    print('Curve instruments of USD_USDCNY_FX:', ir_curve_template_manager.get_curve_instruments('USD_USDCNY_FX'))
        
    print('Dual curves:', ir_curve_template_manager.get_dual_curves())
    print('Cross ccy curves:', ir_curve_template_manager.get_cross_ccy_curves())
    print('Mono single ccy curves:', ir_curve_template_manager.get_mono_single_ccy_curves())
    
    print('Lowest priority:', ir_curve_template_manager.get_lowest_priority())
    print('Curves of priority 0:', ir_curve_template_manager.get_curves(0))
    print('Curves of priority 1:', ir_curve_template_manager.get_curves(1))
    print('Curves of priority 2:', ir_curve_template_manager.get_curves(2))
    print('All curve instruments:', ir_curve_template_manager.get_all_curve_instruments())
    
    