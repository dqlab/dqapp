# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 09:16:55 2021

@author: dzhu
"""
from fxspottemplatemanager import FxSpotTemplateManager
from fxforwardtemplatemanager import FxForwardTemplateManager
from fxswaptemplatemanager import FxSwapTemplateManager

###############################################################################
class FxCashInstTemplateManager:
    def __init__(self):
        self.templates = dict()
        self.templates['fx_spot'] = FxSpotTemplateManager()
        self.templates['fx_forward'] = FxForwardTemplateManager()
        self.templates['fx_swap'] = FxSwapTemplateManager()
        
    def get_template(self, inst_type):
        return self.templates[inst_type.lower()]
    
    def get_domestic_discount_curve(self, inst_type, ccy_pair):
        return self.templates[inst_type.lower()].get_domestic_discount_curve(ccy_pair)
    
    def get_foreign_discount_curve(self, inst_type, ccy_pair):
        return self.templates[inst_type.lower()].get_foreign_discount_curve(ccy_pair)
    
###############################################################################
if __name__ == "__main__":
    fx_cash_inst_template_manager = FxCashInstTemplateManager()
    print('dom curve: ', fx_cash_inst_template_manager.get_domestic_discount_curve('fx_forward', 'usdcny'))    
    print('for curve: ', fx_cash_inst_template_manager.get_foreign_discount_curve('fx_forward', 'usdcny'))  
    print('dom curve: ', fx_cash_inst_template_manager.get_domestic_discount_curve('fx_swap', 'usdcny'))    
    print('for curve: ', fx_cash_inst_template_manager.get_foreign_discount_curve('fx_swap', 'usdcny'))  