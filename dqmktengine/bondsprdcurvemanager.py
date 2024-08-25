# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:53:30 2021

@author: dzhu
"""

import pandas as pd
import numpy as np

from bondcurveengine import create_bond_par_curve, build_bond_sprd_curve, create_bond_curve_build_settings

###############################################################################            
class BondSprdCurveManager:
    def __init__(self, as_of_date, 
                 bond_sprd_curve_template_manager, 
                 bond_hist_data_manager, 
                 benchmark_bond_template_manager, bond_yield_curve_manager):
        self.sprd_curves = dict()            
        for curve_name in bond_sprd_curve_template_manager.curve_names:
            base_curve_name, currency, day_count, curve_type, interp_method, extrap_method, compounding_type, frequuency, to_settlement, quote_type = bond_sprd_curve_template_manager.get_definition(curve_name)
            build_method, calc_jacobian, floating_index, fwd_curve = bond_sprd_curve_template_manager.get_build_settings(curve_name)
            build_settings = create_bond_curve_build_settings(curve_name,
                                                              curve_type,
                                                              interp_method,
                                                              extrap_method,
                                                              [currency, curve_name],
                                                              [floating_index, fwd_curve])
            pillar_data = bond_sprd_curve_template_manager.get_term_structure(curve_name)
            pillar_data.loc[:,'issue_date'] = [as_of_date] * len(pillar_data)
            bond_names=list(pillar_data['bond_id'])
            pillar_data.loc[:,'quote'] = np.transpose(bond_hist_data_manager.get_data(bond_names, as_of_date, as_of_date).to_numpy())*0.01
            cpn_rates = list()
            for bond_name in bond_names: 
                cpn_rates.append(benchmark_bond_template_manager.get_coupon_rate(bond_name))
            pillar_data.loc[:,'coupon'] = cpn_rates  
            mat_type = 'period'            
            par_curve = create_bond_par_curve(as_of_date,
                                              currency,
                                              pillar_data,
                                              mat_type,
                                              quote_type,
                                              curve_name)
            
            base_curve = bond_yield_curve_manager.get_yield_curve(base_curve_name)
            sprd_curve = build_bond_sprd_curve(as_of_date,
                                               curve_name,
                                               build_settings,
                                               par_curve,
                                               day_count,
                                               compounding_type,
                                               frequuency,
                                               to_settlement,
                                               base_curve,
                                               build_method,
                                               calc_jacobian)
            self.sprd_curves[curve_name] = sprd_curve     
            
    def get_sprd_curve(self, curve_name):
        return self.sprd_curves[curve_name]

###############################################################################
if __name__ == "__main__":
    from calendarmanager import CalendarManager

    from vanillabondtemplatemanager import BenchmarkBondTemplateManager 
    from bondyieldcurvetemplatemanager import BondYieldCurveTemplateManager
    from bondsprdcurvetemplatemanager import BondSprdCurveTemplateManager
    
    from bondhistdatamanager import BondHistDataManager
    
    from bondyieldcurvemanager import BondYieldCurveManager
    
    calendar_manager = CalendarManager()
    benchmark_bond_template_manager = BenchmarkBondTemplateManager()
    bond_yield_curve_template_manager = BondYieldCurveTemplateManager()
    bond_sprd_curve_template_manager = BondSprdCurveTemplateManager()
    
    bond_hist_data_manager = BondHistDataManager(bond_yield_curve_template_manager, 
                                                 bond_sprd_curve_template_manager) 
    
    as_of_date = '2021-07-22'
    bond_yield_curve_manager = BondYieldCurveManager(as_of_date, bond_yield_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager)
    bond_sprd_curve_manager = BondSprdCurveManager(as_of_date, bond_sprd_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager, bond_yield_curve_manager)
    print('bond yield curves:', bond_sprd_curve_manager.sprd_curves)    
