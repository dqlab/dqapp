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

from fxspotmktdatamanager import FxSpotMktDataManager
from iryieldcurvemanager import IrYieldCurveManager

from trddata import TrdDataManager
from irtrddatamanager import IrFlowTrdDataManager

from portfoliomanager import PortfolioManager
from pricingdata import PricingDataManager

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
as_of_date = '2021-07-22'

fx_spot_mkt_data_manager = FxSpotMktDataManager(as_of_date, ccy_pair_manager, 
                                                fx_cash_hist_data_manager)
ir_yield_curve_manager = IrYieldCurveManager(as_of_date, ir_yield_curve_template_manager,
                                             ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_mkt_data_manager)

trd_data_manager = TrdDataManager()    
ir_flow_trd_manager = IrFlowTrdDataManager(ir_vanilla_inst_template_manager, trd_data_manager, ir_flow_hist_data_manager)

###############################################################################
portfolio_manager = PortfolioManager()
portfolio_id = portfolio_manager.get_portfolio_id('ir_all')
ir_trades = portfolio_manager.get_trades(portfolio_id)
reporting_ccy = 'cny'

pricing_data_manager = PricingDataManager('ir_valuation')
risk_settings = create_ir_risk_settings('ZERO_CURVE_BUCKET_RISK',
                                        'b',
                                        'b',
                                        False,
                                        1.0e-4,
                                        1.0e-4,
                                        1.0e-4,
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'SINGLE_THREADING_MODE',
                                        False)

pre_day = '2021-07-21'
###############################################################################
for trd_id in ir_trades:
    trd_date = trd_data_manager.get_trade_date(trd_id)
    pv0 = pricing_data_manager.get_present_value(trd_id, pre_day, reporting_ccy)    
    pn_total = pricing_data_manager.get_pnl_total(trd_id, pre_day, reporting_ccy)
    
    discount_curves = dict()    
    discount_curve_names = ir_flow_trd_manager.get_discount_curve(trd_id)
    for key in discount_curve_names.keys():
        discount_curve = ir_yield_curve_manager.get_yield_curve(discount_curve_names[key])
        discount_curves[key] = discount_curve
            
    fwd_curves = dict()    
    fwd_curve_names = ir_flow_trd_manager.get_fwd_curve(trd_id)
    for key in fwd_curve_names.keys():
        fwd_curve = ir_yield_curve_manager.get_yield_curve(fwd_curve_names[key])        
        fwd_curves[key] = fwd_curve
        
    mkt_data_set = create_ir_mkt_data_set(as_of_date, discount_curves, fwd_curves)
    
    trd = ir_flow_trd_manager.get_trade(trd_id)
    results = ir_vanilla_inst_pricer(as_of_date, trd, mkt_data_set, risk_settings)
    
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
    
pricing_data_manager.aggregate(portfolio_id, ir_trades, as_of_date, reporting_ccy)   
pricing_data_manager.save('ir_valuation')