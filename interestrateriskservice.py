# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 23:38:03 2021

@author: dzhu
"""
from dqproto import *

from calendarmanager import CalendarManager

from iborindexmanager import IborIndexManager
from irvanillainsttemplatemanager import IrVanillaInstTemplateManager
from iryieldcurvetemplatemanager import IrYieldCurveTemplateManager

from currencypairmanager import CurrencyPairManager
from fxcashinsttemplatemanager import FxCashInstTemplateManager

from irflowhistdatamanager import IrFlowHistDataManager
from fxcashhistdatamanager import FxCashHistDataManager

from fxspothistscnmanager import FxSpotHistScnManager
from iryieldcurvehistscnmanager import IrYieldCurveHistScnManager
from fxspothiststressedscnmanager import FxSpotHistStressedScnManager
from iryieldcurvehiststressedscnmanager import IrYieldCurveHistStressedScnManager

from trddata import TrdDataManager
from irtrddatamanager import IrFlowTrdDataManager

from portfoliomanager import PortfolioManager
from pricingdata import PricingDataManager
from riskdatamanger import RiskDataManager

from irpricingengine import *
###############################################################################
calendar_manager = CalendarManager()
    
ibor_index_manager = IborIndexManager()    
ir_vanilla_inst_template_manager = IrVanillaInstTemplateManager()
ir_yield_curve_template_manager = IrYieldCurveTemplateManager()
    
ccy_pair_manager = CurrencyPairManager()
fx_cash_inst_template_manager = FxCashInstTemplateManager()

###############################################################################
ir_flow_hist_data_manager = IrFlowHistDataManager()
fx_cash_hist_data_manager = FxCashHistDataManager()

###############################################################################
trd_data_manager = TrdDataManager()    
ir_flow_trd_manager = IrFlowTrdDataManager(ir_vanilla_inst_template_manager, trd_data_manager, ir_flow_hist_data_manager)

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

ir_yield_curve_hist_scn_manager = IrYieldCurveHistScnManager(as_of_date, sim_date, num_sims, change_type, liquidity_horizon, 
                                                             ir_yield_curve_template_manager,
                                                             ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_hist_scn_manager)

###############################################################################
portfolio_manager = PortfolioManager()
portfolio_id = portfolio_manager.get_portfolio_id('ir_all')
ir_trades = portfolio_manager.get_trades(portfolio_id)
reporting_ccy = 'cny'
risk_settings = create_ir_risk_settings('ZERO_CURVE_BUCKET_RISK',
                                        '',
                                        '',
                                        False,
                                        1.0e-4,
                                        1.0e-4,
                                        1.0e-4,
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'SINGLE_THREADING_MODE',
                                        False)
pricing_data_manager = PricingDataManager('ir_valuation')
probability = 0.01
risk_data_manager = RiskDataManager()
###############################################################################
for trd_id in ir_trades:
    pv0 = pricing_data_manager.get_present_value(trd_id, as_of_date, reporting_ccy)    
    for i in range(num_sims):
        discount_curves = dict()    
        discount_curve_names = ir_flow_trd_manager.get_discount_curve(trd_id)
        for key in discount_curve_names.keys():
            discount_curve = ir_yield_curve_hist_scn_manager.get_yield_curve(discount_curve_names[key], i)
            discount_curves[key] = discount_curve
                
        fwd_curves = dict()    
        fwd_curve_names = ir_flow_trd_manager.get_fwd_curve(trd_id)
        for key in fwd_curve_names.keys():
            fwd_curve = ir_yield_curve_hist_scn_manager.get_yield_curve(fwd_curve_names[key], i)        
            fwd_curves[key] = fwd_curve
            
        mkt_data_set = create_ir_mkt_data_set(sim_date, discount_curves, fwd_curves)
        
        trd = ir_flow_trd_manager.get_trade(trd_id)
        results = ir_vanilla_inst_pricer(sim_date, trd, mkt_data_set, risk_settings)
        
        pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.pricing_results.present_value.currency].name
        pv = results.pricing_results.present_value.amount
        cash = results.pricing_results.cash_flow.amount        
        pnl = pv + cash - pv0
        value_id = 'PNL' + '_' + str(i)
        risk_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
        
risk_data_manager.aggregate(portfolio_id, ir_trades, as_of_date, reporting_ccy)   
risk_data_manager.save('ir_risk')

###############################################################################
class IrFlowHistSimVarEngine:
    def __init__(self, probability, liquidity_horizon, num_simulations, 
                 portfolio_id, as_of_date, reporting_ccy, 
                 portfolio_manager,
                 trd_data_manager, 
                 ir_yield_curve_hist_scn_manager,
                 valuation_manager):
        
        self.probability = probability
        self.liquidity_horizon = liquidity_horizon
        self.num_simulations = num_simulations
        self.reporting_ccy = reporting_ccy
        
        self.trd_data = dict()
        self.valuation_data = dict()
        trd_id_list = portfolio_manager.get_trades(portfolio_id)
        for trd_id in trd_id_list:
            self.trd_data[trd_id] = trd_data_manager.get_trade(trd_id)
            self.valuation_data[trd_id] = valuation_manager.get_present_value(trd_id, as_of_date, reporting_ccy)   
            
        self.discount_curves = dict()
        self.fwd_curves = dict()
    
    def run(self):
        for trd_id in self.trd_data:
            pv0 = self.valuation_data[trd_id]    
            for i in range(self.num_simulations):
                discount_curves = self.__get_discount_curves(trd_id, i, ir_yield_curve_hist_scn_manager)                        
                fwd_curves = self.__get_fwd_curves(trd_id, i, ir_yield_curve_hist_scn_manager)                    
                mkt_data = create_ir_mkt_data_set(sim_date, discount_curves, fwd_curves)
                trd_data = self.trd_data_manager.get_trade(trd_id)
                pricing_results = ir_vanilla_inst_pricer(sim_date, trd_data, mkt_data, risk_settings)                
                pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.pricing_results.present_value.currency].name
                sim_pv = pricing_results.pricing_results.present_value.amount
                sim_cash = pricing_results.pricing_results.cash_flow.amount
                sim_pnl = pv + cash - pv0
                value_id = 'PNL' + '_' + str(i)
                self.risk_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
        
class IrFlowMktRiskManager:
    def __init__(self, portfolio, reporting_ccy, prob, liquidity_horizon, trd_data_manager):
        self.reporting_ccy = reporting_ccy
        self.probability = prob
        self.liquidity_horizon = liquidity_horizon
        self.trd_data_manager = trd_data_manager
        
        self.risk_data_manager = RiskDataManager()
        
    def __get_discount_curves(self, trd_id, ith_scn, ir_yield_curve_hist_scn_manager):
        discount_curves = dict()    
        discount_curve_names = ir_flow_trd_manager.get_discount_curve(trd_id)
        for key in discount_curve_names.keys():
            discount_curve = ir_yield_curve_hist_scn_manager.get_yield_curve(discount_curve_names[key], i)
            discount_curves[key] = discount_curve
        return discount_curves
    
    def __get_fwd_curves(self, trd_id, ith_scn, ir_yield_curve_hist_scn_manager):
        fwd_curves = dict()    
        fwd_curve_names = ir_flow_trd_manager.get_fwd_curve(trd_id)
        for key in fwd_curve_names.keys():
            fwd_curve = ir_yield_curve_hist_scn_manager.get_yield_curve(fwd_curve_names[key], i)        
            fwd_curves[key] = fwd_curve
        return fwd_curves
                    
    
        
###############################################################################
stressed_dates = ['2021-07-07', '2021-07-08', '2021-07-09', '2021-07-12', '2021-07-13', '2021-07-14', '2021-07-15', '2021-07-16', '2021-07-19', '2021-07-20', '2021-07-21', '2021-07-22']

fx_spot_hist_stressed_scn_manager = FxSpotHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon, 
                                                                ccy_pair_manager, 
                                                                fx_cash_hist_data_manager)

ir_yield_curve_hist_stressed_scn_manager = IrYieldCurveHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon, 
                                                                     ir_yield_curve_template_manager,
                                                                     ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_hist_stressed_scn_manager)

###############################################################################
stressed_risk_data_manager = RiskDataManager()
for trd_id in ir_trades:
    pv0 = pricing_data_manager.get_present_value(trd_id, as_of_date, reporting_ccy)    
    for i in range(len(stressed_dates)):
        discount_curves = dict()    
        discount_curve_names = ir_flow_trd_manager.get_discount_curve(trd_id)
        for key in discount_curve_names.keys():
            discount_curve = ir_yield_curve_hist_stressed_scn_manager.get_yield_curve(discount_curve_names[key], i)
            discount_curves[key] = discount_curve
                
        fwd_curves = dict()    
        fwd_curve_names = ir_flow_trd_manager.get_fwd_curve(trd_id)
        for key in fwd_curve_names.keys():
            fwd_curve = ir_yield_curve_hist_stressed_scn_manager.get_yield_curve(fwd_curve_names[key], i)        
            fwd_curves[key] = fwd_curve
            
        mkt_data_set = create_ir_mkt_data_set(sim_date, discount_curves, fwd_curves)
        
        trd = ir_flow_trd_manager.get_trade(trd_id)
        results = ir_vanilla_inst_pricer(sim_date, trd, mkt_data_set, risk_settings)
        
        pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.pricing_results.present_value.currency].name
        pv = results.pricing_results.present_value.amount
        cash = results.pricing_results.cash_flow.amount        
        pnl = pv + cash - pv0
        value_id = 'STRESSED_PNL' + '_' + str(i)
        stressed_risk_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl)  
        
###############################################################################        
stressed_risk_data_manager.aggregate(portfolio_id, ir_trades, as_of_date, reporting_ccy)   
stressed_risk_data_manager.save('ir_stressed_risk')