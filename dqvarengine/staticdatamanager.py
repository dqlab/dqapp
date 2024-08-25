# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 19:37:31 2021

@author: dzhu
"""
from calendarmanager import CalendarManager

from iborindexmanager import IborIndexManager

from vanillabondtemplatemanager import VanillaBondTemplateManager, BenchmarkBondTemplateManager
from irvanillainsttemplatemanager import IrVanillaInstTemplateManager

from currencypairmanager import CurrencyPairManager
from fxcashinsttemplatemanager import FxCashInstTemplateManager
 
from bondyieldcurvetemplatemanager import BondYieldCurveTemplateManager
from bondsprdcurvetemplatemanager import BondSprdCurveTemplateManager

from iryieldcurvetemplatemanager import IrYieldCurveTemplateManager

from fxvolsurfacetemplatemanager import FxVolSurfaceTemplateManager
from fxoptionmktconventionmanager import FxOptionMktConventionManager

###############################################################################
class StaticDataManager:
    def __init__(self, instruments, markets):
        self.calendar_manager = CalendarManager()
        
        self.ibor_index_manager = IborIndexManager()
        
        self.currency_pair_manager = CurrencyPairManager()
        
        self.ir_flow_template_manager = IrVanillaInstTemplateManager()
        
        self.fx_cash_template_manager = FxCashInstTemplateManager() 
        
        self.vanilla_bond_template_manager = VanillaBondTemplateManager()
        self.benchmark_bond_template_manager = BenchmarkBondTemplateManager()
                
        self.ir_yield_curve_template_manager = IrYieldCurveTemplateManager()
        
        self.fx_option_mkt_convention_manager = FxOptionMktConventionManager()
        self.fx_vol_surface_template_manager = FxVolSurfaceTemplateManager()
                
        self.bond_yield_curve_template_manager = BondYieldCurveTemplateManager()
        self.bond_sprd_curve_template_manager = BondSprdCurveTemplateManager()