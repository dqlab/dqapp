# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:32:17 2021

@author: dzhu
"""
from dqproto import *

from calendarmanager import CalendarManager

from vanillabondtemplatemanager import VanillaBondTemplateManager, BenchmarkBondTemplateManager 
from bondyieldcurvetemplatemanager import BondYieldCurveTemplateManager
from bondsprdcurvetemplatemanager import BondSprdCurveTemplateManager

from bondhistdatamanager import BondHistDataManager

from bondyieldcurvehistscnmanager import BondYieldCurveHistScnManager
from bondsprdcurvehistscnmanager import BondSprdCurveHistScnManager
from bondyieldcurvehiststressedscnmanager import BondYieldCurveHistStressedScnManager
from bondsprdcurvehiststressedscnmanager import BondSprdCurveHistStressedScnManager

from trddata import TrdDataManager
from vanillabondtrdmanager import VanillaBondTrdDataManager

from portfoliomanager import PortfolioManager
from pricingdata import PricingDataManager
from riskdatamanager import RiskDataManager

from fipricingengine import create_fi_mkt_data_set, create_fi_risk_settings, vanilla_bond_pricer
###############################################################################
calendar_manager = CalendarManager()

vanilla_bond_template_manager = VanillaBondTemplateManager()
benchmark_bond_template_manager = BenchmarkBondTemplateManager()
bond_yield_curve_template_manager = BondYieldCurveTemplateManager()
bond_sprd_curve_template_manager = BondSprdCurveTemplateManager()

###############################################################################
bond_hist_data_manager = BondHistDataManager(bond_yield_curve_template_manager, 
                                             bond_sprd_curve_template_manager) 

###############################################################################
as_of_date = '2021-07-22'
sim_date = '2021-07-23'
num_sims = 10
change_type = 'absolute'
liquidity_horizon = 1
    
bond_yield_curve_hist_scn_manager = BondYieldCurveHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon, 
                                                        bond_yield_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager)
bond_sprd_curve_hist_scn_manager = BondSprdCurveHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon,
                                                      bond_sprd_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager, bond_yield_curve_hist_scn_manager)
    
trd_data_manager = TrdDataManager()
vanilla_bond_trd_data_manager = VanillaBondTrdDataManager(vanilla_bond_template_manager, trd_data_manager)

###############################################################################    
portfolio_manager = PortfolioManager()
portfolio_id = portfolio_manager.get_portfolio_id('bond_all')
bond_trades = portfolio_manager.get_trades(portfolio_id)
reporting_ccy = 'cny'
risk_settings = create_fi_risk_settings('ZERO_CURVE_BUCKET_RISK',
                                        '',
                                        '',
                                        '',
                                        False,
                                        1.0e-4,
                                        1.0e-4,
                                        1.0e-4,
                                        1.0e-4,
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'SINGLE_THREADING_MODE',
                                        False)
pricing_data_manager = PricingDataManager('bond_valuation')
probability = 0.01
risk_data_manager = RiskDataManager()
###############################################################################
for trd_id in bond_trades:
    pv0 = pricing_data_manager.get_present_value(trd_id, as_of_date, reporting_ccy)    
    for i in range(num_sims):
        discount_curve_name = vanilla_bond_trd_data_manager.get_discount_curve(trd_id)
        discount_curve = bond_yield_curve_hist_scn_manager.get_yield_curve(discount_curve_name.upper(), i)
        sprd_curve_name = vanilla_bond_trd_data_manager.get_sprd_curve(trd_id)
        if sprd_curve_name=='' or sprd_curve_name == 'nan':
            sprd_curve = ''
        else:
            sprd_curve =  bond_sprd_curve_hist_scn_manager.get_sprd_curve(sprd_curve_name.upper(), i)
            
        fwd_curve_name = vanilla_bond_trd_data_manager.get_fwd_curve(trd_id)
        fwd_curve = ''    
        mkt_data_set = create_fi_mkt_data_set(sim_date,
                                              discount_curve,
                                              sprd_curve,
                                              fwd_curve,
                                              trd_id)
        trd = vanilla_bond_trd_data_manager.get_trade(trd_id)
        results = vanilla_bond_pricer(sim_date,
                                      trd,
                                      mkt_data_set,
                                      risk_settings)
        
        pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.pricing_results.present_value.currency].name
        pv = results.pricing_results.present_value.amount
        cash = results.pricing_results.cash_flow.amount        
        pnl = pv + cash - pv0
        value_id = 'PNL' + '_' + str(i)
        risk_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
        
###############################################################################
stressed_dates = ['2021-07-07', '2021-07-08', '2021-07-09', '2021-07-12', '2021-07-13', '2021-07-14', '2021-07-15', '2021-07-16', '2021-07-19', '2021-07-20', '2021-07-21', '2021-07-22']
bond_yield_curve_hist_stress_scn_manager = BondYieldCurveHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon,
                                                                     bond_yield_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager)
bond_sprd_curve_hist_stress_scn_manager = BondSprdCurveHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon,
                                                   bond_sprd_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager, bond_yield_curve_hist_stress_scn_manager)
###############################################################################
stressed_risk_data_manager = RiskDataManager()
for trd_id in bond_trades:
    pv0 = pricing_data_manager.get_present_value(trd_id, as_of_date, reporting_ccy)    
    for i in range(len(stressed_dates)):
        discount_curve_name = vanilla_bond_trd_data_manager.get_discount_curve(trd_id)
        discount_curve = bond_yield_curve_hist_stress_scn_manager.get_yield_curve(discount_curve_name.upper(), i)
        sprd_curve_name = vanilla_bond_trd_data_manager.get_sprd_curve(trd_id)
        if sprd_curve_name=='' or sprd_curve_name == 'nan':
            sprd_curve = ''
        else:
            sprd_curve =  bond_sprd_curve_hist_stress_scn_manager.get_sprd_curve(sprd_curve_name.upper(), i)
            
        fwd_curve_name = vanilla_bond_trd_data_manager.get_fwd_curve(trd_id)
        fwd_curve = ''    
        mkt_data_set = create_fi_mkt_data_set(sim_date, discount_curve, sprd_curve, fwd_curve, trd_id)
        trd = vanilla_bond_trd_data_manager.get_trade(trd_id)
        results = vanilla_bond_pricer(sim_date, trd, mkt_data_set, risk_settings)
        
        pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.pricing_results.present_value.currency].name
        pv = results.pricing_results.present_value.amount
        cash = results.pricing_results.cash_flow.amount        
        pnl = pv + cash - pv0
        value_id = 'STRESSED_PNL' + '_' + str(i)
        stressed_risk_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
###############################################################################
stressed_risk_data_manager.aggregate(portfolio_id, bond_trades, as_of_date, reporting_ccy, probability)   
stressed_risk_data_manager.save('bond_stressed_risk')