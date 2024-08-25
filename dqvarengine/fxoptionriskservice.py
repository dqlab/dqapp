# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 19:58:51 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 10:56:36 2021

@author: dzhu
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 23:38:03 2021

@author: dzhu
"""
from calendarmanager import CalendarManager

from iborindexmanager import IborIndexManager
from irvanillainsttemplatemanager import IrVanillaInstTemplateManager
from iryieldcurvetemplatemanager import IrYieldCurveTemplateManager

from currencypairmanager import CurrencyPairManager
from fxcashinsttemplatemanager import FxCashInstTemplateManager
from fxvolsurfacetemplatemanager import FxVolSurfaceTemplateManager
from fxoptionmktconventionmanager import FxOptionMktConventionManager

from irflowhistdatamanager import IrFlowHistDataManager
from fxcashhistdatamanager import FxCashHistDataManager
from fxvolhistdatamanager import FxVolHistDataManager

from fxspothistscnmanager import FxSpotHistScnManager
from iryieldcurvehistscnmanager import IrYieldCurveHistScnManager
from fxvolhistscnmanager import FxVolHistScnManager
from fxspothiststressedscnmanager import FxSpotHistStressedScnManager
from iryieldcurvehiststressedscnmanager import IrYieldCurveHistStressedScnManager
from fxvolhiststressedscnmanager import FxVolHistStressedScnManager

from trddata import TrdDataManager
from fxtrddatamanager import FxTrdManager, FxCashTrdManager, FxOptionTrdManager
from portfoliomanager import PortfolioManager
from pricingdata import PricingDataManager
from riskdatamanger import RiskDataManager

from fxpricingengine import *

###############################################################################
calendar_manager = CalendarManager()
    
ibor_index_manager = IborIndexManager()    
ir_vanilla_inst_template_manager = IrVanillaInstTemplateManager()
ir_yield_curve_template_manager = IrYieldCurveTemplateManager()

ccy_pair_manager = CurrencyPairManager()
fx_cash_inst_template_manager = FxCashInstTemplateManager()
fx_option_mkt_convention_manager = FxOptionMktConventionManager()
fx_vol_surf_template_manager = FxVolSurfaceTemplateManager()    

ir_flow_hist_data_manager = IrFlowHistDataManager()
fx_cash_hist_data_manager = FxCashHistDataManager()
fx_vol_hist_data_manager = FxVolHistDataManager()

###############################################################################
trd_manager = TrdDataManager()
fx_trd_manager = FxTrdManager(fx_cash_inst_template_manager, trd_manager)
fx_option_trd_manager = FxOptionTrdManager(trd_manager) 
###############################################################################
as_of_date = '2021-07-22'
###############################################################################
sim_date = '2021-07-23'
num_sims = 10
change_type = 'absolute'
liquidity_horizon = 1

fx_spot_hist_scn_manager = FxSpotHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon, 
                                                ccy_pair_manager, 
                                                fx_cash_hist_data_manager)

ir_yield_curve_hist_scn_manager = IrYieldCurveHistStressedScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon, 
                                                                     ir_yield_curve_template_manager,
                                                                     ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_hist_scn_manager)

fx_vol_hist_scn_manager = FxVolHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon, 
                                              fx_vol_surf_template_manager, fx_option_mkt_convention_manager, 
                                              fx_vol_hist_data_manager,
                                              fx_spot_hist_scn_manager, ir_yield_curve_hist_scn_manager)   
 
###############################################################################
portfolio_manager = PortfolioManager()
portfolio_id = portfolio_manager.get_portfolio_id('fx_option_all')
fx_option_trades = portfolio_manager.get_trades(portfolio_id)
reporting_ccy = 'cny'
risk_settings = create_fx_risk_settings(False,
                                        False,
                                        '',
                                        '',
                                        '',
                                        't',
                                        False,
                                        1.0e-2,
                                        1.0e-2,
                                        1.0e-4, 
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'SINGLE_THREADING_MODE',
                                        False)
fx_option_pricing_data_manager = PricingDataManager('fx_option_valuation')
probability = 0.01
risk_data_manager = RiskDataManager()
###############################################################################
for trd_id in fx_option_trades:
    pv0 = fx_option_pricing_data_manager.get_present_value(trd_id, as_of_date, reporting_ccy)    
    for i in range(num_sims): 
        discount_curves = list()    
        discount_curves.append(ir_yield_curve_hist_scn_manager.get_yield_curve(fx_trd_manager.get_domestic_discount_curve(trd_id, i)))
        discount_curves.append(ir_yield_curve_hist_scn_manager.get_yield_curve(fx_trd_manager.get_foreign_discount_curve(trd_id, i)))
        spots = list()
        ccy_pair = trd_manager.get_underlying(trd_id)
        spots.append(fx_spot_hist_scn_manager.get_fx_spot_rate(ccy_pair, i))
        vol_surfs = list()
        vol_surfs.append(fx_vol_hist_scn_manager.get_fx_vol_surface(ccy_pair, i))
        mkt_data_set = create_fx_mkt_data_set(sim_date, discount_curves, spots, vol_surfs)
        
        model_settings = create_pricing_model_settings('BLACK_SCHOLES_MERTON', [0.0], [], ccy_pair, False)    
        pricing_ccy = trd_manager.get_payoff_ccy(trd_id)
        pricing_settings = create_fx_pricing_settings(model_settings, 'ANALYTICAL', ccy_pair[3:6], PdeSettings(), MonteCarloSettings())
        
        trd = fx_option_trd_manager.get_trade(trd_id)
        inst_type = trd_manager.get_inst_type(trd_id)
        if inst_type.lower() == 'fx_european_option':
            results = fx_european_option_pricer(sim_date, trd, mkt_data_set, pricing_settings, risk_settings)    
        else:
            raise Exception('This instrument type is not supported!')
        
        pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.present_value.currency].name
        pv = results.present_value.amount
        cash = results.cash_flow.amount
        pnl = pv + cash - pv0
        value_id = 'PNL' + '_' + str(i)
        risk_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
        
risk_data_manager.aggregate(portfolio_id, fx_option_trades, as_of_date, reporting_ccy)   
risk_data_manager.save('fx_option_risk')

###############################################################################
stressed_dates = ['2021-07-07', '2021-07-08', '2021-07-09', '2021-07-12', '2021-07-13', '2021-07-14', '2021-07-15', '2021-07-16', '2021-07-19', '2021-07-20', '2021-07-21', '2021-07-22']

fx_spot_hist_stressed_scn_manager = FxSpotHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon, 
                                                ccy_pair_manager, 
                                                fx_cash_hist_data_manager)

ir_yield_curve_hist_stressed_scn_manager = IrYieldCurveHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon, 
                                                                     ir_yield_curve_template_manager,
                                                                     ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_hist_stressed_scn_manager)

fx_vol_hist_stressed_scn_manager = FxVolHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon, 
                                                              fx_vol_surf_template_manager, fx_option_mkt_convention_manager, 
                                                              fx_vol_hist_data_manager,
                                                              fx_spot_hist_stressed_scn_manager, ir_yield_curve_hist_stressed_scn_manager)   

###############################################################################
stressed_risk_data_manager = RiskDataManager()
for trd_id in fx_option_trades:
    pv0 = fx_option_pricing_data_manager.get_present_value(trd_id, as_of_date, reporting_ccy)    
    for i in range(len(stressed_dates)): 
        discount_curves = list()    
        discount_curves.append(ir_yield_curve_hist_stressed_scn_manager.get_yield_curve(fx_trd_manager.get_domestic_discount_curve(trd_id), i))
        discount_curves.append(ir_yield_curve_hist_stressed_scn_manager.get_yield_curve(fx_trd_manager.get_foreign_discount_curve(trd_id), i))
        spots = list()
        ccy_pair = trd_manager.get_underlying(trd_id)
        spots.append(fx_spot_hist_stressed_scn_manager.get_fx_spot_rate(ccy_pair, i))
        vol_surfs = list()
        vol_surfs.append(fx_vol_hist_scn_manager.get_fx_vol_surface(ccy_pair, i))
        mkt_data_set = create_fx_mkt_data_set(sim_date, discount_curves, spots, vol_surfs)
        
        model_settings = create_pricing_model_settings('BLACK_SCHOLES_MERTON', [0.0], [], ccy_pair, False)    
        pricing_ccy = trd_manager.get_payoff_ccy(trd_id)
        pricing_settings = create_fx_pricing_settings(model_settings, 'ANALYTICAL', ccy_pair[3:6], PdeSettings(), MonteCarloSettings())
        
        trd = fx_option_trd_manager.get_trade(trd_id)
        inst_type = trd_manager.get_inst_type(trd_id)
        if inst_type.lower() == 'fx_european_option':
            results = fx_european_option_pricer(sim_date, trd, mkt_data_set, pricing_settings, risk_settings)    
        else:
            raise Exception('This instrument type is not supported!')
        
        pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.present_value.currency].name
        pv = results.present_value.amount
        cash = results.cash_flow.amount
        pnl = pv + cash - pv0
        value_id = 'STRESSED_PNL' + '_' + str(i)
        stressed_risk_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
        
stressed_risk_data_manager.aggregate(portfolio_id, fx_option_trades, as_of_date, reporting_ccy)   
stressed_risk_data_manager.save('fx_option_stressed_risk')