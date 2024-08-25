# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:32:29 2021

@author: dzhu
"""
import pandas as pd

###############################################################################
class FxVolSurfaceTemplateManager:
    def __init__(self):
        data_loc = 'staticdata/foreignexchange/market/fx_vol_surface/'
        
        self.definition = pd.read_csv(data_loc +'definition.csv')
        self.definition.columns = self.definition.columns.str.lower()
        self.definition = self.definition.set_index('currency_pair')
        
        self.term_structure = pd.read_csv(data_loc + 'term_structure.csv')
        self.term_structure.columns = self.term_structure.columns.str.lower()
        self.term_structure = self.term_structure.set_index('currency_pair')
        
        self.smile_structure = pd.read_csv(data_loc + 'smile_structure.csv')
        self.smile_structure.columns = self.smile_structure.columns.str.lower()
        self.smile_structure = self.smile_structure.set_index('currency_pair')
        
    def get_definition(self, ccy_pair):
        return self.definition.loc[ccy_pair.upper()].to_dict()
    
    def get_term_structure(self, ccy_pair):
        return self.term_structure.loc[ccy_pair.upper()]['term'].tolist()
    
    def get_atm_inst_type(self, ccy_pair):
        inst_type = self.smile_structure.loc[ccy_pair.upper()][(self.smile_structure['instrument_strike']=='ATM')]['instrument_type'].tolist()
        return inst_type[0]
    
    def get_otm_insts(self, ccy_pair):
        inst_types = set(self.smile_structure.loc[ccy_pair.upper()][(self.smile_structure['instrument_strike']!='ATM')]['instrument_type'].tolist())
        inst_strikes = set(self.smile_structure.loc[ccy_pair.upper()][(self.smile_structure['instrument_strike']!='ATM')]['instrument_strike'].tolist())
        return list(inst_types), list(inst_strikes)
    
    def get_ccy_pairs(self):
        return list(set(self.definition.index))
    
###############################################################################
if __name__ == "__main__":
    fx_vol_surf_template_manger = FxVolSurfaceTemplateManager()
    print(fx_vol_surf_template_manger.definition)    
    print(fx_vol_surf_template_manger.term_structure)    
    print(fx_vol_surf_template_manger.smile_structure)
    print('def:', fx_vol_surf_template_manger.get_definition('usdcny'))
    print('terms:', fx_vol_surf_template_manger.get_term_structure('usdcny'))
    print('atm inst:', fx_vol_surf_template_manger.get_atm_inst_type('usdcny'))
    print('otm insts:', fx_vol_surf_template_manger.get_otm_insts('usdcny'))
    print('ccy pairs:', fx_vol_surf_template_manger.get_ccy_pairs())