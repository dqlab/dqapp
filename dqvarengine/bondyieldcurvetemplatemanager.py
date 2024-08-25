# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:14:52 2021

@author: dzhu
"""

import pandas as pd

###############################################################################
class BondYieldCurveTemplateManager:
    def __init__(self):
        data_loc = 'staticdata/fixedincome/market/bond_yield_curve/'
        
        self.definition = pd.read_csv(data_loc+'definition.csv')
        self.definition.columns = self.definition.columns.str.lower()
        self.definition = self.definition.set_index('curve_id')
        
        self.term_structure = pd.read_csv(data_loc+'term_structure.csv')
        self.term_structure.columns = self.term_structure.columns.str.lower()
        self.term_structure = self.term_structure.set_index('curve_id')
        
        self.build_settings = pd.read_csv(data_loc+'build_settings.csv')
        self.build_settings.columns = self.build_settings.columns.str.lower()
        self.build_settings = self.build_settings.set_index('curve_id')
                
        self.curve_names = list(self.definition.index)
        
    def get_definition(self, curve_name):
        ccy = str(self.definition.loc[curve_name]['currency'])
        day_count = str(self.definition.loc[curve_name]['day_count_convention'])
        curve_type = str(self.definition.loc[curve_name]['curve_type'])
        interp_method = str(self.definition.loc[curve_name]['interp_method'])
        extrap_method = str(self.definition.loc[curve_name]['extrap_method'])
        compounding_type = str(self.definition.loc[curve_name]['compounding_type'])
        frequency = str(self.definition.loc[curve_name]['frequency'])
        to_settlement = bool(self.definition.loc[curve_name]['to_settlement'])
        quote_type = str(self.definition.loc[curve_name]['quote_type'])
        return ccy, day_count, curve_type, interp_method, extrap_method, compounding_type, frequency, to_settlement, quote_type
       
    def get_build_settings(self, curve_name): 
        floating_index =str(self.build_settings.loc[curve_name]['floating_index'])
        if floating_index == 'nan':
            floating_index = ''
        forward_curve =str(self.build_settings.loc[curve_name]['forward_curve'])
        if forward_curve == 'nan':
            forward_curve = ''
            
        build_method =  str(self.build_settings.loc[curve_name]['build_method'])
        jacobian = bool(self.build_settings.loc[curve_name]['jacobian'])
        return build_method, jacobian, floating_index, forward_curve     
       
    def get_term_structure(self, curve_name):
        return self.term_structure.loc[curve_name]       
    
    def get_curve_bonds(self):
        bonds = set()
        
        for curve in self.curve_names:
            pillars = self.get_term_structure(curve)
            for i in range(len(pillars)):
                bonds.add(pillars.iloc[i]['bond_id'])
                
        return list(bonds)

###############################################################################
if __name__ == "__main__":
    manager = BondYieldCurveTemplateManager()
    print('definition:', manager.definition)
    print('term_structure:', manager.term_structure)
    print('build_settings:', manager.build_settings)