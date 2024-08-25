# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 22:21:04 2021

@author: dzhu
"""
from fxspotmktdatamanager import FxSpotMktDataManager
from iryieldcurvemanager import IrYieldCurveManager
from bondyieldcurvemanager import BondYieldCurveManager
from bondsprdcurvemanager import BondSprdCurveManager
from fxvolmktdatamanager import FxVolMktDataManager

###############################################################################
class MktDataManager:
    def __init__(self, as_of_date, hist_data_manager, static_data_manager):
        
        self.fx_spot_rate_manager = FxSpotMktDataManager(as_of_date, 
                                                         static_data_manager.ccy_pair_manager, 
                                                         hist_data_manager.fx_cash_hist_data_manager)
        
        self.ir_yield_curve_manager = IrYieldCurveManager(as_of_date, 
                                                          static_data_manager.ir_yield_curve_template_manager,
                                                          hist_data_manager.ir_flow_hist_data_manager, 
                                                          hist_data_manager.sfx_cash_hist_data_manager, 
                                                          self.fx_spot_rate_manager)
        
        self.bond_yield_curve_manager = BondYieldCurveManager(as_of_date, 
                                                              static_data_manager.bond_yield_curve_template_manager, 
                                                              static_data_manager.bond_hist_data_manager, 
                                                              static_data_manager.benchmark_bond_template_manager)
        
        self.bond_sprd_curve_manager = BondSprdCurveManager(as_of_date, 
                                                            static_data_manager.bond_sprd_curve_template_manager, 
                                                            hist_data_manager.bond_hist_data_manager, 
                                                            static_data_manager.benchmark_bond_template_manager, 
                                                            self.bond_yield_curve_manager)
        
        self.fx_vol_surf_manager = FxVolMktDataManager(as_of_date, 
                                                       static_data_manager.fx_vol_surf_template_manager, 
                                                       static_data_manager.fx_option_mkt_convention_manager, 
                                                       hist_data_manager.fx_vol_hist_data_manager,
                                                       self.fx_spot_mkt_data_manager, 
                                                       self.ir_yield_curve_manager)   
        
    
###############################################################################
if __name__ == '__main__':    
    as_of_date = '2021-07-22'    
    mkt_data_manager = MktDataManager(as_of_date, hist_data_manager, static_data_manager)
