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

from fxspotmktdatamanager import FxSpotMktDataManager
from iryieldcurvemanager import IrYieldCurveManager
from fxvolmktdatamanager import FxVolMktDataManager

from trddata import TrdDataManager
from fxtrddatamanager import FxTrdManager, FxCashTrdManager, FxOptionTrdManager
from portfoliomanager import PortfolioManager
from pricingdata import PricingDataManager
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
as_of_date = '2021-05-28'

fx_spot_mkt_data_manager = FxSpotMktDataManager(as_of_date, ccy_pair_manager, 
                                                fx_cash_hist_data_manager)
ir_yield_curve_manager = IrYieldCurveManager(as_of_date, ir_yield_curve_template_manager,
                                             ir_flow_hist_data_manager, fx_cash_hist_data_manager, fx_spot_mkt_data_manager)
fx_vol_surf_manager = FxVolMktDataManager(as_of_date, fx_vol_surf_template_manager, fx_option_mkt_convention_manager, 
                                          fx_vol_hist_data_manager,
                                          fx_spot_mkt_data_manager, ir_yield_curve_manager)   

trd_manager = TrdDataManager()
fx_trd_manager = FxTrdManager(fx_cash_inst_template_manager, trd_manager)
fx_cash_trd_manager = FxCashTrdManager(trd_manager)
fx_option_trd_manager = FxOptionTrdManager(trd_manager)    
###############################################################################
portfolio_manager = PortfolioManager()
portfolio_id = portfolio_manager.get_portfolio_id('fx_cash_all')
fx_cash_trades = portfolio_manager.get_trades(portfolio_id)
reporting_ccy = 'cny'

fx_cash_pricing_data_manager = PricingDataManager('fx_cash_valuation')
risk_settings = create_fx_risk_settings(True,
                                        False,
                                        '',
                                        '',
                                        '',
                                        'b',
                                        False,
                                        1.0e-2,
                                        1.0e-2,
                                        1.0e-4, 
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'CENTRAL_DIFFERENCE_METHOD',
                                        'SINGLE_THREADING_MODE',
                                        False)
pre_day = '2021-05-27'
###############################################################################
for trd_id in fx_cash_trades:
    trd_date = trd_manager.get_trade_date(trd_id)
    pv0 = fx_cash_pricing_data_manager.get_present_value(trd_id, pre_day, reporting_ccy)    
    pn_total = fx_cash_pricing_data_manager.get_pnl_total(trd_id, pre_day, reporting_ccy)
    
    discount_curves = list()    
    discount_curves.append(ir_yield_curve_manager.get_yield_curve(fx_trd_manager.get_domestic_discount_curve(trd_id)))
    discount_curves.append(ir_yield_curve_manager.get_yield_curve(fx_trd_manager.get_foreign_discount_curve(trd_id)))
    spots = list()
    ccy_pair = trd_manager.get_underlying(trd_id)
    spots.append(fx_spot_mkt_data_manager.get_fx_spot_rate(ccy_pair))
    vol_surfs = list()
    mkt_data_set = create_fx_mkt_data_set(as_of_date, discount_curves, spots, vol_surfs)
    
    trd = fx_cash_trd_manager.get_trade(trd_id)
    inst_type = trd_manager.get_inst_type(trd_id)
    if inst_type.lower() == 'fx_forward':
        results = fx_forward_pricer(as_of_date, trd, mkt_data_set, risk_settings)
    elif inst_type.lower() == 'fx_swap':
        results = fx_swap_pricer(as_of_date, trd, mkt_data_set, risk_settings)
    else:
        raise Exception('This instrument type is not supported!')
    
    pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.present_value.currency].name
    pv = results.present_value.amount
    value_id = 'PRESENT_VALUE'
    fx_cash_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pv)
    
    cash = results.cash_flow.amount
    value_id = 'CASH_VALUE'
    fx_cash_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, cash)    
    
    pnl = 0.0
    if as_of_date > trd_date:
        pnl = pv + cash - pv0        
    value_id = 'PNL_DAILY'
    fx_cash_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
    
    pnl_total = pn_total + pnl
    value_id = 'PNL_TOTAL'
    fx_cash_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl_total) 
    
    for j in range(len(results.sensitivity.data)):
        tags = results.sensitivity.data[j].tag[0].tags        
        sensi_name = results.sensitivity.data[j].name    
        for k in range(len(tags)):
            tag_list = tags[k].split('|')
            risk_class = tag_list[1]
            if risk_class.lower() == 'fx':
                risk_type = tag_list[0]                 
            elif risk_class.lower() == 'girr':
                term = tag_list[3]
                if term.lower() == 'total': 
                    risk_type = tag_list[0]                    
                else:
                    risk_type = 'bucket_' + tag_list[0]
            else:
                raise Exception('No such risk class!')
                
            und_name = sensi_name.replace(tag_list[0]+'_', '')
            if und_name !='':                
                value = results.sensitivity.data[j].value[0].data[k]
                if value != 0.0:
                    if risk_class.lower() == 'fx':
                        und_name = und_name[7:13]                    
                    value_id = risk_type + '_' + risk_class + '_' + und_name                    
                    if risk_class.lower() == 'girr':
                        value_id = value_id + '_' + term
                    value_id = value_id.upper()                     
                    fx_cash_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
    
fx_cash_pricing_data_manager.aggregate(portfolio_id, fx_cash_trades, as_of_date, reporting_ccy)   
fx_cash_pricing_data_manager.save('fx_cash_valuation')

###############################################################################
portfolio_id = portfolio_manager.get_portfolio_id('fx_option_all')
fx_option_trades = portfolio_manager.get_trades(portfolio_id)
fx_option_pricing_data_manager = PricingDataManager('fx_option_valuation')

risk_settings = create_fx_risk_settings(True,
                                        True,
                                        'b',
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

###############################################################################
for trd_id in fx_option_trades:
    trd_date = trd_manager.get_trade_date(trd_id)
    pv0 = fx_option_pricing_data_manager.get_present_value(trd_id, pre_day, reporting_ccy)    
    pn_total = fx_option_pricing_data_manager.get_pnl_total(trd_id, pre_day, reporting_ccy)
    
    discount_curves = list()    
    discount_curves.append(ir_yield_curve_manager.get_yield_curve(fx_trd_manager.get_domestic_discount_curve(trd_id)))
    discount_curves.append(ir_yield_curve_manager.get_yield_curve(fx_trd_manager.get_foreign_discount_curve(trd_id)))
    spots = list()
    ccy_pair = trd_manager.get_underlying(trd_id)
    spots.append(fx_spot_mkt_data_manager.get_fx_spot_rate(ccy_pair))
    vol_surfs = list()
    vol_surfs.append(fx_vol_surf_manager.get_fx_vol_surface(ccy_pair))
    mkt_data_set = create_fx_mkt_data_set(as_of_date, discount_curves, spots, vol_surfs)
    
    model_settings = create_pricing_model_settings('BLACK_SCHOLES_MERTON', [0.0], [], ccy_pair, False)    
    pricing_ccy = trd_manager.get_payoff_ccy(trd_id)
    pricing_settings = create_fx_pricing_settings(model_settings, 'ANALYTICAL', ccy_pair[3:6], PdeSettings(), MonteCarloSettings())
    
    trd = fx_option_trd_manager.get_trade(trd_id)
    inst_type = trd_manager.get_inst_type(trd_id)
    if inst_type.lower() == 'fx_european_option':
        results = fx_european_option_pricer(as_of_date, trd, mkt_data_set, pricing_settings, risk_settings)    
    else:
        raise Exception('This instrument type is not supported!')
    
    pricing_ccy = CurrencyName.DESCRIPTOR.values_by_number[results.present_value.currency].name
    pv = results.present_value.amount
    value_id = 'PRESENT_VALUE'
    fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pv)
    
    cash = results.cash_flow.amount
    value_id = 'CASH_VALUE'
    fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, cash)    
    
    pnl = 0.0
    if as_of_date > trd_date:
        pnl = pv + cash - pv0        
    value_id = 'PNL_DAILY'
    fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl) 
    
    pnl_total = pn_total + pnl
    value_id = 'PNL_TOTAL'
    fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, pnl_total) 
    
    for j in range(len(results.sensitivity.data)):             
        sensi_name = results.sensitivity.data[j].name
        if 'DELTA' in sensi_name:
            value_id = 'DELTA' + '_' + 'FX' + '_' + ccy_pair
            value = results.sensitivity.data[j].value[0].data[0] 
            fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
        elif 'GAMMA' in sensi_name:
            value_id = 'GAMMA' + '_' + 'FX' + '_' + ccy_pair
            value = results.sensitivity.data[j].value[0].data[0] 
            fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
        elif 'VEGA' in sensi_name:
            if len(results.sensitivity.data[j].value) > 1:
                terms = fx_vol_surf_template_manager.get_term_structure(ccy_pair)
                for k in range(len(results.sensitivity.data[j].value)):                    
                    value = results.sensitivity.data[j].value[k].data[0]
                    if value != 0.0:
                        value_id = 'VEGA' + '_' + 'FX' + '_' + ccy_pair + '_' + terms[k]
                        fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
            else:
                value_id = 'VEGA' + '_' + 'FX' + '_' + ccy_pair + '_TOTAL'
                value = results.sensitivity.data[j].value[0].data[0]
                fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
        elif 'RHO' in sensi_name and 'IR' in sensi_name:
            value_id = 'DELTA' + '_' + 'GIRR' + '_' + fx_trd_manager.get_domestic_discount_curve(trd_id) + '_TOTAL'
            value = results.sensitivity.data[j].value[0].data[0] 
            fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
        elif 'RHO' in sensi_name and 'DIVIDEND' in sensi_name:
            value_id = 'DELTA' + '_' + 'GIRR' + '_' + fx_trd_manager.get_foreign_discount_curve(trd_id) + '_TOTAL'
            value = results.sensitivity.data[j].value[0].data[0] 
            fx_option_pricing_data_manager.add(trd_id, as_of_date, pricing_ccy, value_id, value)
        else:
            raise Exception('This risk type is not supported!')
    
fx_option_pricing_data_manager.aggregate(portfolio_id, fx_cash_trades, as_of_date, reporting_ccy)   
fx_option_pricing_data_manager.save('fx_option_valuation')