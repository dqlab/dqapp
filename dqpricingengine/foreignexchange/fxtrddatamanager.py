# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 08:39:17 2021

@author: dzhu
"""
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *

from utility import to_currency_pair, to_date, to_period

###############################################################################
def create_fx_forward(currency_pair,
                      buy_ccy,
                      buy_amount,
                      sell_ccy,
                      sell_amount,
                      delivery,
                      expiry):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_currency_pair = to_currency_pair(currency_pair)
    p_buy_ccy = CurrencyName.DESCRIPTOR.values_by_name[buy_ccy.upper()].number
    p_strike = sell_amount / buy_amount
    p_notional = dqCreateProtoNotional(p_buy_ccy, buy_amount)
    p_buy_sell = BUY
    if p_buy_ccy == p_currency_pair.right_currency.name:
        p_strike = buy_amount / sell_amount            
        p_sell_ccy = CurrencyName.DESCRIPTOR.values_by_name[sell_ccy.upper()].number        
        p_notional = dqCreateProtoNotional(p_sell_ccy, sell_amount)    
        p_buy_sell = SELL
    
    p_delivery_date  = to_date(delivery, '%Y-%m-%d')
    p_expiry_date  = to_date(expiry, '%Y-%m-%d')
    pb_inst = dqCreateProtoFxForward(p_currency_pair, 
                                     p_buy_sell, 
                                     p_notional, 
                                     p_strike, 
                                     p_delivery_date, 
                                     p_expiry_date)
    
    return pb_inst    
        
###############################################################################
def create_fx_swap(currency_pair,
                   near_buy_ccy,
                   near_buy_amount,
                   near_sell_ccy,
                   near_sell_amount,
                   near_delivery,
                   near_expiry,
                   far_buy_ccy,
                   far_buy_amount,
                   far_sell_ccy,
                   far_sell_amount,
                   far_delivery,
                   far_expiry):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_currency_pair = to_currency_pair(currency_pair)
        
    p_near_buy_ccy = CurrencyName.DESCRIPTOR.values_by_name[near_buy_ccy.upper()].number
    p_near_strike = near_sell_amount / near_buy_amount
    p_near_notional = dqCreateProtoNotional(p_near_buy_ccy, near_buy_amount)
    p_near_buy_sell = BUY
    if p_near_buy_ccy == p_currency_pair.right_currency.name:
        p_near_strike = near_buy_amount / near_sell_amount            
        p_near_sell_ccy = CurrencyName.DESCRIPTOR.values_by_name[near_sell_ccy.upper()].number        
        p_near_notional = dqCreateProtoNotional(p_near_sell_ccy, near_sell_amount)    
        p_near_buy_sell = SELL
    
    p_near_delivery = to_date(near_delivery, '%Y-%m-%d')
    p_near_expiry = to_date(near_expiry, '%Y-%m-%d')
    
    p_far_buy_ccy = CurrencyName.DESCRIPTOR.values_by_name[far_buy_ccy.upper()].number
    p_far_strike = near_sell_amount / near_buy_amount
    p_far_notional = dqCreateProtoNotional(p_far_buy_ccy, far_buy_amount)
    p_far_buy_sell = BUY
    if p_far_buy_ccy == p_currency_pair.right_currency.name:
        p_far_strike = far_buy_amount / far_sell_amount            
        p_far_sell_ccy = CurrencyName.DESCRIPTOR.values_by_name[far_sell_ccy.upper()].number        
        p_far_notional = dqCreateProtoNotional(p_far_sell_ccy, far_sell_amount)    
        p_far_buy_sell = SELL
    
    p_far_delivery = to_date(far_delivery, '%Y-%m-%d')
    p_far_expiry = to_date(far_expiry, '%Y-%m-%d')
    pb_inst = dqCreateProtoFxSwap(p_currency_pair, 
                                  p_near_buy_sell, 
                                  p_near_notional, 
                                  p_near_strike, 
                                  p_near_delivery, 
                                  p_near_expiry, 
                                  p_far_buy_sell, 
                                  p_far_notional, 
                                  p_far_strike, 
                                  p_far_delivery, 
                                  p_far_expiry)
    return pb_inst

###############################################################################
def create_fx_european_option(currency_pair,
                              call_ccy,
                              put_ccy,
                              strike,
                              expiry,
                              delivery,
                              nominal):    
    '''
    @args:
        
        
    @return:
        
    '''
    p_currency_pair = to_currency_pair(currency_pair)
    p_strike = strike
    p_notional = dqCreateProtoNotional(p_currency_pair.left_currency.name, nominal)
    p_call_ccy = CurrencyName.DESCRIPTOR.values_by_name[call_ccy.upper()].number        
    if p_call_ccy == p_currency_pair.left_currency.name:
        p_payoff_type = CALL
    else:
        p_payoff_type = PUT
    
    p_delivery_date  = to_date(delivery, '%Y-%m-%d')
    p_expiry_date  = to_date(expiry, '%Y-%m-%d')
    pb_inst = dqCreateProtoFxEuropeanOption(p_currency_pair, 
                                            p_payoff_type, 
                                            p_notional, 
                                            p_strike, 
                                            p_delivery_date, 
                                            p_expiry_date)        
    return pb_inst    

###############################################################################
class FxTrdManager:
    def __init__(self, fx_inst_template_manager, trd_manager):
        self.trd_data = pd.read_csv('trddata/foreignexchange/fx_trades.csv')  
        self.trd_data.columns = self.trd_data.columns.str.lower()
        self.trd_data = self.trd_data.set_index('trade_id')
        
        for trd_id in set(self.trd_data.index):
            dom_curve = str(self.trd_data.loc[trd_id,'domestic_discount_curve'])
            if dom_curve.lower() in ['', 'nan']:
                inst_type = trd_manager.get_inst_type(trd_id)
                inst_name = trd_manager.get_inst_name(trd_id)
                ccy_pair = trd_manager.get_underlying(trd_id)
                dom_curve = fx_inst_template_manager.get_domestic_discount_curve(inst_type, ccy_pair)
                self.trd_data.loc[trd_id, 'domestic_discount_curve'] = dom_curve.upper()
            for_curve = str(self.trd_data.loc[trd_id,'foreign_discount_curve'])
            if for_curve.lower() in ['', 'nan']:
                inst_type = trd_manager.get_inst_type(trd_id)
                inst_name = trd_manager.get_inst_name(trd_id)
                ccy_pair = trd_manager.get_underlying(trd_id)
                for_curve = fx_inst_template_manager.get_foreign_discount_curve(inst_type, ccy_pair)
                self.trd_data.loc[trd_id, 'foreign_discount_curve'] = for_curve.upper()
    
    def get_domestic_discount_curve(self, trd_id):        
        return str(self.trd_data.loc[trd_id, 'domestic_discount_curve'])
    
    def get_foreign_discount_curve(self, trd_id):        
        return str(self.trd_data.loc[trd_id, 'foreign_discount_curve'])
              
###############################################################################
class FxCashTrdManager:
    def __init__(self, trd_data_manager):
        self.trd_data = pd.read_csv('trddata/foreignexchange/cash/fx_cash_trades.csv')  
        self.trd_data.columns = self.trd_data.columns.str.lower()
        self.trd_data = self.trd_data.set_index('trade_id')
        
        self.pb_trade_data = dict() 
        trade_set = set(self.trd_data.index)
        
        for trd_id in trade_set:            
            inst_type = trd_data_manager.get_inst_type(trd_id)
                         
            currency_pair = trd_data_manager.get_underlying(trd_id)
            
            if inst_type.lower() == 'fx_forward':                
                buy_ccy = self.trd_data.loc[trd_id, 'buy_currency']
                buy_amount = float(self.trd_data.loc[trd_id, 'buy_amount'])
                sell_ccy = self.trd_data.loc[trd_id, 'sell_currency']
                sell_amount = float(self.trd_data.loc[trd_id, 'sell_amount'])
                delivery = self.trd_data.loc[trd_id, 'delivery_date']
                expiry = self.trd_data.loc[trd_id, 'expiry_date']                
                trd = create_fx_forward(currency_pair, buy_ccy, buy_amount, sell_ccy, sell_amount, delivery, expiry)
            
            elif inst_type.lower() == 'fx_swap':
                trd_data = self.trd_data.loc[trd_id]
                trd_data = trd_data.set_index('delivery_date')
                trd_data = trd_data.sort_index()
                near_delivery = trd_data.index[0]
                near_buy_ccy = trd_data.loc[near_delivery, 'buy_currency']
                near_buy_amount = float(trd_data.loc[near_delivery, 'buy_amount'])
                near_sell_ccy = trd_data.loc[near_delivery, 'sell_currency']
                near_sell_amount = float(trd_data.loc[near_delivery, 'sell_amount'])
                near_expiry = trd_data.loc[near_delivery, 'expiry_date']
                far_delivery = trd_data.index[1]
                far_buy_ccy = trd_data.loc[far_delivery, 'buy_currency']
                far_buy_amount = float(trd_data.loc[far_delivery, 'buy_amount'])
                far_sell_ccy = trd_data.loc[far_delivery, 'sell_currency']
                far_sell_amount = float(trd_data.loc[far_delivery, 'sell_amount'])
                far_expiry = trd_data.loc[far_delivery, 'expiry_date']
                trd = create_fx_swap(currency_pair, near_buy_ccy, near_buy_amount, near_sell_ccy, near_sell_amount, near_delivery, near_expiry,
                                     far_buy_ccy, far_buy_amount, far_sell_ccy, far_sell_amount, far_delivery, far_expiry)
            else:
                raise Exception('This instrument type is not supported yet!')
                        
            self.pb_trade_data[trd_id] = trd     
        
    def get_trade(self, trd_id):
        return self.pb_trade_data[trd_id.upper()]

###############################################################################
class FxOptionTrdManager:
    def __init__(self, trd_data_manager):
        self.trd_data = pd.read_csv('trddata/foreignexchange/option/fx_european_option/fx_european_option.csv')  
        self.trd_data.columns = self.trd_data.columns.str.lower()
        self.trd_data = self.trd_data.set_index('trade_id')
        
        self.pb_trade_data = dict() 
        trade_set = set(self.trd_data.index)        
        for trd_id in trade_set:      
            
            inst_type = trd_data_manager.get_inst_type(trd_id)                         
            currency_pair = trd_data_manager.get_underlying(trd_id)
            
            if inst_type.lower() == 'fx_european_option':                
                call_ccy = self.trd_data.loc[trd_id, 'call_currency']
                put_ccy = self.trd_data.loc[trd_id, 'put_currency']
                nominal = trd_data_manager.get_nominal(trd_id)
                delivery = self.trd_data.loc[trd_id, 'delivery']
                expiry = self.trd_data.loc[trd_id, 'expiry']    
                strike = float(self.trd_data.loc[trd_id, 'strike'])
                trd = create_fx_european_option(currency_pair, call_ccy, put_ccy, strike, expiry, delivery, nominal)
            else:
                raise Exception('This instrument type is not supported yet!')
                        
            self.pb_trade_data[trd_id] = trd     
        
    def get_trade(self, trd_id):
        return self.pb_trade_data[trd_id.upper()]
###############################################################################
from trddata import TrdDataManager
from fxcashinsttemplatemanager import FxCashInstTemplateManager

if __name__ == "__main__":
    fx_cash_inst_template_manager = FxCashInstTemplateManager()
    trd_manager = TrdDataManager()
    fx_trd_manager = FxTrdManager(fx_cash_inst_template_manager, trd_manager)
    fx_cash_trd_manager = FxCashTrdManager(trd_manager)
    print(fx_cash_trd_manager.pb_trade_data)
    
    fx_option_trd_manager = FxOptionTrdManager(trd_manager)
    print(fx_option_trd_manager.pb_trade_data)
    