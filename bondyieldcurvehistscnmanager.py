# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 19:34:57 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 02:04:25 2021

@author: dzhu
"""

import numpy as np

from bondcurveengine import create_bond_par_curve, build_bond_yield_curve, create_bond_curve_build_settings

###############################################################################            
class BondYieldCurveHistScnManager:
    def __init__(self, as_of_date, sime_date, num_sims, change_type, liquidity_horizon,
                 bond_yield_curve_template_manager, 
                 bond_hist_data_manager, 
                 benchmark_bond_template_manager):
        self.yield_curves = dict()
        for curve_name in bond_yield_curve_template_manager.curve_names:
            currency, day_count, curve_type, interp_method, extrap_method, compounding_type, frequuency, to_settlement, quote_type = bond_yield_curve_template_manager.get_definition(curve_name)
            build_method, calc_jacobian, floating_index, fwd_curve = bond_yield_curve_template_manager.get_build_settings(curve_name)
            build_settings = create_bond_curve_build_settings(curve_name, curve_type, interp_method, extrap_method,
                                                              [currency, curve_name],
                                                              [floating_index, fwd_curve])
            pillar_data = bond_yield_curve_template_manager.get_term_structure(curve_name)
            pillar_data.loc[:,'issue_date'] = [as_of_date] * len(pillar_data)
            bond_names=list(pillar_data['bond_id'])            
            
            if change_type.lower() == 'absolute':
                data_type = 'change'
            else:
                data_type = 'change_in_percent'
            hist_data = bond_hist_data_manager.get_hist_data(bond_names, as_of_date, -num_sims, data_type)                
            base_data = bond_hist_data_manager.get_hist_data(bond_names, as_of_date, 0, 'yield')

            for i in range(num_sims):
                pillar_data.loc[:, 'quote'] = (base_data.iloc[0].to_numpy() + hist_data.iloc[i].to_numpy())*0.01
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
                other_curves=[]
                yield_curve = build_bond_yield_curve(sime_date,
                                                     curve_name,
                                                     build_settings,
                                                     par_curve,
                                                     day_count,
                                                     compounding_type,
                                                     frequuency,
                                                     to_settlement,
                                                     other_curves,
                                                     build_method,
                                                     calc_jacobian)
                
                self.yield_curves[curve_name+'_'+str(i)] = yield_curve
                        
    def get_yield_curve(self, curve_name, scn_num):
        return self.yield_curves[curve_name+'_'+str(scn_num)]

###############################################################################
if __name__ == "__main__":
    from calendarmanager import CalendarManager

    from vanillabondtemplatemanager import BenchmarkBondTemplateManager 
    from bondyieldcurvetemplatemanager import BondYieldCurveTemplateManager
    from bondsprdcurvetemplatemanager import BondSprdCurveTemplateManager
    
    from bondhistdatamanager import BondHistDataManager
    
    calendar_manager = CalendarManager()
    benchmark_bond_template_manager = BenchmarkBondTemplateManager()
    bond_yield_curve_template_manager = BondYieldCurveTemplateManager()
    bond_sprd_curve_template_manager = BondSprdCurveTemplateManager()
    
    bond_hist_data_manager = BondHistDataManager(bond_yield_curve_template_manager, 
                                                 bond_sprd_curve_template_manager) 
    
    as_of_date = '2021-07-22'
    sim_date = '2021-07-23'
    num_sims = 10
    change_type = 'absolute'
    liquidity_horizon = 1
    bond_yield_curve_hist_scn_manager = BondYieldCurveHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon,
                                                                     bond_yield_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager)
    print('bond yield curves:', bond_yield_curve_hist_scn_manager.yield_curves)