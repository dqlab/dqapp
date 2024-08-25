# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 19:50:31 2021

@author: dzhu
"""
import sys
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_date, to_calendar_name_list, to_period
from utility import save_pb_data
from marketdata import create_time_series

###############################################################################
def build_ir_vanilla_trade(inst_type,
                           inst_name, 
                           pay_receive,
                           rate, 
                           spread, 
                           start_date,
                           maturity,
                           inst_template,
                           nominal, 
                           leg_fixings):
    '''
    @args:
        leg_fixings: pandas.DataFrame, index = datetime.date, columns = {Ibor Index 1, Ibor Index 2,...}
    '''
    p_start_date = to_date(start_date, '%Y-%m-%d')
    p_maturity_date = to_date(maturity, '%Y-%m-%d')
    p_fixed_rate = rate
    p_spread = spread
    p_pay_receive = PayReceiveFlag.DESCRIPTOR.values_by_name[pay_receive.upper()].number
    p_inst_tempalte = inst_template
    p_notional = nominal
    p_leg_fixings_maps = list()
    for col in leg_fixings.columns:
        p_time_series = col.upper()
        mode = 'TS_FORWARD_MODE'
        #print(leg_fixings)
        data = leg_fixings[[col]]
        data.columns=['value']
        data = data.reset_index()
        #data.rename(columns = {col:'value'}, inplace = True) 
        p_time_series = create_time_series(data, mode, col)
        p_leg_fixings_maps.append(dqCreateProtoTimeSeriesMap(col, p_time_series)) 
    p_leg_fixings = dqCreateProtoLegFixings(p_leg_fixings_maps)    
    
    p_capital_conversion_rate = 1.0
    
    pb_input = dqCreateProtoBuildIrVanillaInstrumentInput(p_start_date, 
                                                          p_maturity_date, 
                                                          p_pay_receive, 
                                                          p_fixed_rate, 
                                                          p_spread, 
                                                          p_notional, 
                                                          p_capital_conversion_rate, 
                                                          p_inst_tempalte, 
                                                          p_leg_fixings)    
    req_name = 'BUILD_IR_VANILLA_INSTRUMENT'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    pb_output = BuildIrVanillaSwapOutput()
    pb_output.ParseFromString(res_msg)        
    return pb_output.inst   

###############################################################################
class IrFlowTrdDataManager:
    def __init__(self, 
                 ir_vanilla_inst_template_manager, 
                 trd_data_manager, 
                 ir_flow_hist_data_manager):
        
        self.trd_data = pd.read_csv('trddata/interestrate/flow/ir_flow_trades.csv')  
        self.trd_data.columns = self.trd_data.columns.str.lower()
        self.trd_data = self.trd_data.set_index('trade_id')
        
        self.pb_trade_data = dict()    
        self.discount_curves = dict()
        self.fwd_curves = dict()
        trade_set = set(self.trd_data.index)
        for trd_id in trade_set:            
            inst_type = trd_data_manager.get_inst_type(trd_id)
            inst_name = trd_data_manager.get_inst_name(trd_id)
            nominal = trd_data_manager.get_nominal(trd_id)           
            trade_date = trd_data_manager.get_trade_date(trd_id)
            maturity = trd_data_manager.get_maturity(trd_id)            
            start_date = trd_data_manager.get_start_date(trd_id)
            
            this_trd = self.trd_data.loc[[trd_id]]
            rate = float(this_trd[(this_trd['leg_type'] == 'FIXED_LEG')]['rate'].iloc[0])
            spread = 0.0
            if inst_type == 'IR_VANILLA_SWAP':
                spread = float(this_trd[(this_trd['leg_type'] == 'FLOATING_LEG')]['spread'].iloc[0])                        
            pay_receive = str(this_trd[(this_trd['leg_type'] == 'FIXED_LEG')]['pay_receive'].iloc[0])                 
            
            inst_template = ir_vanilla_inst_template_manager.get_inst_template(inst_type, inst_name)
            
            ref_rate = ir_vanilla_inst_template_manager.get_reference_rate(inst_type, inst_name)
            mkt_insts = pd.DataFrame()
            mkt_insts['type'] = ['DEPOSIT'] * len(ref_rate)
            mkt_insts['name'] = ref_rate
            mkt_insts['term'] = ''
            leg_fixings = ir_flow_hist_data_manager.get_data(mkt_insts, trade_date, maturity)
            
            trd = build_ir_vanilla_trade(inst_type,
                                         inst_name, 
                                         pay_receive,
                                         rate, 
                                         spread, 
                                         start_date,
                                         maturity,
                                         inst_template,
                                         nominal, 
                                         leg_fixings)
            
            discount_curves = ir_vanilla_inst_template_manager.get_discount_curve(inst_type, inst_name)
            fwd_curves = ir_vanilla_inst_template_manager.get_fwd_curve(inst_type, inst_name)
            
            self.pb_trade_data[trd_id] = trd
            self.discount_curves[trd_id] = discount_curves
            self.fwd_curves[trd_id] = fwd_curves
        
    def get_trade(self, trd_id):
        return self.pb_trade_data[trd_id.upper()]

    def get_discount_curve(self, trd_id):
        return self.discount_curves[trd_id]
    
    def get_fwd_curve(self, trd_id):
        return self.fwd_curves[trd_id]
    
###############################################################################
from calendarmanager import CalendarManager

from iborindexmanager import IborIndexManager
from irvanillainsttemplatemanager import IrVanillaInstTemplateManager

from irflowhistdatamanager import IrFlowHistDataManager

from trddata import TrdDataManager

if __name__ == "__main__":
    calendar_manager = CalendarManager()
    ibor_manager = IborIndexManager()
    ir_vanilla_inst_template_manager = IrVanillaInstTemplateManager()       
    ir_flow_hist_data_manager = IrFlowHistDataManager()    
    trd_data_manager = TrdDataManager()    
    if_flow_trd_manager = IrFlowTrdDataManager(ir_vanilla_inst_template_manager,
                                               trd_data_manager,
                                               ir_flow_hist_data_manager)