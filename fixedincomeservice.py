# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:32:17 2021

@author: dzhu
"""
from calendarmanager import CalendarManager

from vanillabondtemplatemanager import VanillaBondTemplateManager, BenchmarkBondTemplateManager 
from bondyieldcurvetemplatemanager import BondYieldCurveTemplateManager
from bondsprdcurvetemplatemanager import BondSprdCurveTemplateManager

from bondhistdatamanager import BondHistDataManager

from bondyieldcurvemanager import BondYieldCurveManager
from bondsprdcurvemanager import BondSprdCurveManager

from trddata import TrdDataManager
from vanillabondtrdmanager import VanillaBondTrdDataManager

from portfoliomanager import PortfolioManager
from pricingdata import PricingDataManager

from fipricingengine import *

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

bond_yield_curve_manager = BondYieldCurveManager(as_of_date, bond_yield_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager)
bond_sprd_curve_manager = BondSprdCurveManager(as_of_date, bond_sprd_curve_template_manager, bond_hist_data_manager, benchmark_bond_template_manager, bond_yield_curve_manager)
    
trd_data_manager = TrdDataManager()
vanilla_bond_trd_data_manager = VanillaBondTrdDataManager(vanilla_bond_template_manager, trd_data_manager)

###############################################################################    
portfolio_manager = PortfolioManager()
portfolio_id = portfolio_manager.get_portfolio_id('bond_all')
bond_trades = portfolio_manager.get_trades(portfolio_id)
reporting_ccy = 'cny'

pricing_data_manager = PricingDataManager('bond_valuation')

risk_settings = create_fi_risk_settings('ZERO_CURVE_BUCKET_RISK',
                                        'b',
                                        'b',
                                        '',
                                        False,
                                        1.0e-4,
                                        1.0e-4,
                                        1.0e-4,
                                        1.0e-4,
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'SINGLE_THREADING_MODE',
                                        False)
pre_day = '2021-07-21'
for trd_id in bond_trades:
    trd_date = trd_data_manager.get_trade_date(trd_id)
    pv0 = pricing_data_manager.get_present_value(trd_id, pre_day, reporting_ccy)    
    pn_total = pricing_data_manager.get_pnl_total(trd_id, pre_day, reporting_ccy)
    
    discount_curve_name = vanilla_bond_trd_data_manager.get_discount_curve(trd_id)
    discount_curve = bond_yield_curve_manager.get_yield_curve(discount_curve_name.upper())
    sprd_curve_name = vanilla_bond_trd_data_manager.get_sprd_curve(trd_id)
    if sprd_curve_name=='' or sprd_curve_name == 'nan':
        sprd_curve = ''
    else:
        sprd_curve =  bond_sprd_curve_manager.get_sprd_curve(sprd_curve_name.upper())
        
    fwd_curve_name = vanilla_bond_trd_data_manager.get_fwd_curve(trd_id)
    fwd_curve = ''    
    mkt_data_set = create_fi_mkt_data_set(as_of_date,
                                          discount_curve,
                                          sprd_curve,
                                          fwd_curve,
                                          trd_id)
    trd = vanilla_bond_trd_data_manager.get_trade(trd_id)
    results = vanilla_bond_pricer(as_of_date,
                                  trd,
                                  mkt_data_set,
                                  risk_settings)
    
    pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.pricing_results.present_value.currency].name
    pv = results.pricing_results.present_value.amount
    value_id = 'PRESENT_VALUE'
    pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pv)
    
    cash = results.pricing_results.cash_flow.amount
    value_id = 'CASH_VALUE'
    pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, cash)    
    
    pnl = 0.0
    if as_of_date > trd_date:
        pnl = pv + cash - pv0        
    value_id = 'PNL_DAILY'
    pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
    
    pnl_total = pn_total + pnl
    value_id = 'PNL_TOTAL'
    pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl_total) 
    for j in range(len(results.pricing_results.sensitivity.data)):
        tags = results.pricing_results.sensitivity.data[j].tag[0].tags
        sensi_name = results.pricing_results.sensitivity.data[j].name    
        for k in range(len(tags)):
            tag_list = tags[k].split('|')
            risk_class = tag_list[1]
            risk_type = 'bucket_' + tag_list[0]
            term = tag_list[3]
            und_name = sensi_name.replace(tag_list[0]+'_', '')
            if und_name !='':                
                value = results.pricing_results.sensitivity.data[j].value[0].data[k]
                if value != 0.0:
                    value_id = risk_type + '_' + risk_class + '_' + und_name + '_' + term
                    value_id = value_id.upper()                    
                    pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
    
pricing_data_manager.aggregate(portfolio_id, bond_trades, as_of_date, reporting_ccy)   
pricing_data_manager.save('bond_valuation')