# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:53:30 2021

@author: dzhu
"""

import pandas as pd
import numpy as np

from bondcurveengine import create_bond_par_curve, build_bond_sprd_curve, create_bond_curve_build_settings

###############################################################################            
class BondSprdCurveHistStressedScnManager:
    def __init__(self, as_of_date, sime_date, stressed_dates, change_type, liquidity_horizon,
                 bond_sprd_curve_template_manager, 
                 bond_hist_data_manager, 
                 benchmark_bond_template_manager, bond_yield_curve_hist_stress_scn_manager):
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
            
            if change_type.lower() == 'absolute':
                data_type = 'change'
            else:
                data_type = 'change_in_percent'
            hist_data = bond_hist_data_manager.get_stressed_data(bond_names, stressed_dates, data_type)                      
            base_data = bond_hist_data_manager.get_hist_data(bond_names, as_of_date, 0, 'yield')
            
            for i in range(len(stressed_dates)):
                pillar_data.loc[:,'quote'] = (base_data.iloc[0].to_numpy() + hist_data.iloc[i].to_numpy())*0.01
                cpn_rates = list()
                for bond_name in bond_names: 
                    cpn_rates.append(benchmark_bond_template_manager.get_coupon_rate(bond_name))
                pillar_data.loc[:,'coupon'] = cpn_rates  
                mat_type = 'period'            
                par_curve = create_bond_par_curve(sime_date,
                                                  currency,
                                                  pillar_data,
                                                  mat_type,
                                                  quote_type,
                                                  curve_name)
                
                base_curve = bond_yield_curve_hist_stress_scn_manager.get_yield_curve(base_curve_name,i)
                sprd_curve = build_bond_sprd_curve(sime_date,
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
                self.sprd_curves[curve_name+'_'+str(i)] = sprd_curve     
            
    def get_sprd_curve(self, curve_name, scn_num):
        return self.sprd_curves[curve_name+'_'+str(scn_num)]

###############################################################################
if __name__ == "__main__":
    from calendarmanager import CalendarManager

    from vanillabondtemplatemanager import BenchmarkBondTemplateManager 
    from bondyieldcurvetemplatemanager import BondYieldCurveTemplateManager
    from bondsprdcurvetemplatemanager import BondSprdCurveTemplateManager
    
    from bondhistdatamanager import BondHistDataManager
    
    from bondyieldcurvehiststressedscnmanager import BondYieldCurveHistStressedScnManager
    
    calendar_manager = CalendarManager()
    benchmark_bond_template_manager = BenchmarkBondTemplateManager()
    bond_yield_curve_template_manager = BondYieldCurveTemplateManager()
    bond_sprd_curve_template_manager = BondSprdCurveTemplateManager()
    
    bond_hist_data_manager = BondHistDataManager(bond_yield_curve_template_manager, 
                                                 bond_sprd_curve_template_manager) 
    
    as_of_date = '2021-07-22'
    sim_date = '2021-07-23'
    stressed_dates = ['2021-07-07', '2021-07-08', '2021-07-09', '2021-07-12', '2021-07-13', '2021-07-14', '2021-07-15', '2021-07-16', '2021-07-19', '2021-07-20', '2021-07-21', '2021-07-22']
    change_type = 'absolute'
    liquidity_horizon = 1
    bond_yield_curve_hist_stress_scn_manager = BondYieldCurveHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon,
                                                                     bond_yield_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager)
    bond_sprd_curve_hist_stress_scn_manager = BondSprdCurveHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon,
                                                   bond_sprd_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager, bond_yield_curve_hist_stress_scn_manager)
    print('bond yield curves:', bond_sprd_curve_hist_stress_scn_manager.sprd_curves)    
