# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 17:44:24 2021

@author: dzhu
"""
import sys
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from staticdata import create_static_data
from utility import save_pb_data, to_period, to_calendar_name_list
from irmarket import create_leg_definition
        
###############################################################################        
def create_deposit_template(inst_name,
                            start_delay,
                            currency,
                            day_count_convention,
                            calendar,
                            interest_day_convention,
                            pay_day_offset,
                            pay_day_convention, 
                            inst_start_convention,
                            save,
                            loc):
    '''
    @args:
       
    @return:
        
    '''   
    #try:
    leg_definition = create_leg_definition('FIXED_LEG',
                                           currency,
                                           day_count_convention,
                                           'INVALID_IBOR_INDEX_NAME',
                                           'NO_DISCOUNT',
                                           'STANDARD',                          
                                           'INITIAL_FINAL_EXCHANGE',
                                           False,
                                           False,
                                           False,
                                           calendar,
                                           'ONCE',
                                           interest_day_convention,
                                           'INITIAL',
                                           'LONG',
                                           pay_day_offset,
                                           pay_day_convention,
                                           [calendar],
                                           'INVALID_FREQUENCY',
                                           'INVALID_BUSINESS_DAY_CONVENTION',
                                           'INVALID_DATE_GENERATION_MODE',
                                           '0d')
    
    inst_type = DEPOSIT       
    pb_data = dqCreateProtoInterestRateInstrumentTemplate(inst_type,
                                                          inst_name,
                                                          to_period(start_delay),
                                                          [leg_definition],
                                                          InstrumentStartConvention.DESCRIPTOR.values_by_name[inst_start_convention.upper()].number)
    
    pb_data_list = dqCreateProtoInterestRateInstrumentTemplateList([pb_data])
    
    create_static_data('SDT_IR_VANILLA_INSTRUMENT', pb_data_list)
    
    if save:
        save_pb_data(pb_data_list, inst_name, loc)
    
    return pb_data_list.interest_rate_instrument_template[0]
    
###############################################################################
def create_ir_vanilla_swap_template(inst_name,
                                    start_delay,
                                    currency,
                                    leg1_type,
                                    leg1_day_count,
                                    leg1_ref_index,
                                    leg1_rate_calc_method,
                                    leg1_spread,
                                    leg1_calendar,
                                    leg1_freq,
                                    leg1_interest_day_convention,
                                    leg1_stub_policy,
                                    leg1_broken_period_type,
                                    leg1_pay_day_offset,
                                    leg1_pay_day_convention,
                                    leg1_fixing_calendars,
                                    leg1_fixing_freq,
                                    leg1_fixing_day_convention,
                                    leg1_fixing_mode,
                                    leg1_fixing_day_offset,
                                    leg2_type,
                                    leg2_day_count,
                                    leg2_ref_index,
                                    leg2_rate_calc_method,
                                    leg2_spread,
                                    leg2_calendar,
                                    leg2_freq,
                                    leg2_interest_day_convention,
                                    leg2_stub_policy,
                                    leg2_broken_period_type,
                                    leg2_pay_day_offset,
                                    leg2_pay_day_convention,
                                    leg2_fixing_calendars,
                                    leg2_fixing_freq,
                                    leg2_fixing_day_convention,
                                    leg2_fixing_mode,
                                    leg2_fixing_day_offset,
                                    start_convention,
                                    save,
                                    loc):
    '''
    @args:
       
    @return:
        
    '''   
    
    leg1_definition = create_leg_definition(leg1_type,
                                            currency,
                                            leg1_day_count,
                                            leg1_ref_index,
                                            'NO_DISCOUNT',
                                            leg1_rate_calc_method,                          
                                            'INVALID_NOTIONAL_EXCHANGE',
                                            leg1_spread,
                                            False,
                                            False,
                                            leg1_calendar,
                                            leg1_freq,
                                            leg1_interest_day_convention,
                                            leg1_stub_policy,
                                            leg1_broken_period_type,
                                            leg1_pay_day_offset,
                                            leg1_pay_day_convention,
                                            leg1_fixing_calendars,
                                            leg1_fixing_freq,
                                            leg1_fixing_day_convention,
                                            leg1_fixing_mode,
                                            leg1_fixing_day_offset)
    
    leg2_definition = create_leg_definition(leg2_type,
                                            currency,
                                            leg2_day_count,
                                            leg2_ref_index,
                                            'NO_DISCOUNT',
                                            leg2_rate_calc_method,                          
                                            'INVALID_NOTIONAL_EXCHANGE',
                                            leg1_spread,
                                            False,
                                            False,
                                            leg2_calendar,
                                            leg2_freq,
                                            leg2_interest_day_convention,
                                            leg2_stub_policy,
                                            leg2_broken_period_type,
                                            leg2_pay_day_offset,
                                            leg2_pay_day_convention,
                                            leg2_fixing_calendars,
                                            leg2_fixing_freq,
                                            leg2_fixing_day_convention,
                                            leg2_fixing_mode,
                                            leg2_fixing_day_offset)
    
    p_instrument_type = IR_VANILLA_SWAP
    p_start_delay = to_period(start_delay)
    p_leg_definition = [leg1_definition, leg2_definition]
    p_start_convention = InstrumentStartConvention.DESCRIPTOR.values_by_name[start_convention.upper()].number
    pb_data = dqCreateProtoInterestRateInstrumentTemplate(p_instrument_type, 
                                                          inst_name, 
                                                          p_start_delay, 
                                                          p_leg_definition, 
                                                          p_start_convention)
    pb_data_list = dqCreateProtoInterestRateInstrumentTemplateList([pb_data])
    create_static_data('SDT_IR_VANILLA_INSTRUMENT', pb_data_list)
    
    if save:
        save_pb_data(pb_data_list, inst_name, loc)

    return pb_data_list.interest_rate_instrument_template[0]
    
###############################################################################
class IrVanillaInstTemplateManager:
    def __init__(self):
        self.data_loc = 'staticdata/interestrate/instrument/ir_vanilla_instrument/'
        
        self.inst_definition = pd.read_csv(self.data_loc + 'inst_definition.csv')
        self.inst_definition.columns = self.inst_definition.columns.str.lower()
        self.inst_definition = self.inst_definition.set_index('instrument_template_id')
        
        self.leg_definition = pd.read_csv(self.data_loc + 'leg_definition.csv')
        self.leg_definition.columns = self.leg_definition.columns.str.lower()
        self.leg_definition = self.leg_definition.set_index('instrument_template_id')
        
        #load data into dqlib cache:
        self.inst_templates = pd.DataFrame()        
        self.inst_templates = pd.concat([self.inst_templates,self.__create_deposit_template(self.inst_definition, 
                                                                                            self.leg_definition)],axis=0)
        self.inst_templates = pd.concat([self.inst_templates,self.__create_ir_vanilla_swap_template(self.inst_definition, 
                                                                                                    self.leg_definition)],axis=0)
        
        
        self.inst_templates = self.inst_templates.set_index('inst_template_id')

    def __create_deposit_template(self, inst_definition, leg_definition):
        inst_templates = pd.DataFrame(columns=['inst_template_id', 'inst_template'])
        inst_type = 'deposit'
        tmp = inst_definition[inst_definition['instrument_type'] == inst_type.upper()]
        for i in range(len(tmp)):
            inst_name = str(tmp.iloc[i]['instrument_name'])
            inst_template_id = IrVanillaInstTemplateManager.create_inst_template_id(inst_type, inst_name)            
            start_delay = str(tmp.iloc[i]['start_delay'])           
            currency = str(inst_definition.iloc[i]['currency'])
            
            day_count_convention = str(leg_definition.loc[inst_template_id]['day_count_convention'])
            calendar= str(leg_definition.loc[inst_template_id]['calendar'])
            interest_day_convention = str(leg_definition.loc[inst_template_id]['interest_day_convention'])
            pay_day_offset = str(leg_definition.loc[inst_template_id]['pay_day_offset'])
            pay_day_convention = str(leg_definition.loc[inst_template_id]['pay_day_convention'])
            inst_start_convention='SPOT_START'                
            inst_template = create_deposit_template(inst_name,
                                                    start_delay,
                                                    currency,
                                                    day_count_convention,
                                                    calendar,
                                                    interest_day_convention,
                                                    pay_day_offset,
                                                    pay_day_convention, 
                                                    inst_start_convention,
                                                    True,
                                                    self.data_loc)            
            inst_templates = inst_templates.append({'inst_template_id': inst_template_id,
                                                    'inst_template': inst_template}, ignore_index=True)
        
        return inst_templates
                
    def __create_ir_vanilla_swap_template(self, inst_definition, leg_definition):
        '''
        @args:
           
        @return:
            pandas.DataFrame  s  
        '''       
        inst_templates = pd.DataFrame(columns=['inst_template_id', 'inst_template'])
        inst_type = 'ir_vanilla_swap'
        tmp = inst_definition[inst_definition['instrument_type'] == inst_type.upper()]
        for i in range(len(tmp)):
            inst_name = str(tmp.iloc[i]['instrument_name'])  
            inst_template_id = IrVanillaInstTemplateManager.create_inst_template_id(inst_type, inst_name)                          
            start_delay = str(inst_definition.iloc[i]['start_delay'])
            currency = str(inst_definition.iloc[i]['currency'])
            
            leg_type = list(leg_definition.loc[inst_template_id]['leg_type'])
            leg_type =list(map(str, leg_type))
            day_count = list(leg_definition.loc[inst_template_id]['day_count_convention'])
            day_count =list(map(str, day_count))
            ref_index = list(leg_definition.loc[inst_template_id]['reference_rate'])
            ref_index =list(map(str, ref_index))
            rate_calc_method = list(leg_definition.loc[inst_template_id]['rate_calc_method'])
            rate_calc_method =list(map(str, rate_calc_method))
            spread = list(leg_definition.loc[inst_template_id]['spread'])
            spread =list(map(bool, spread))
            calendar = list(leg_definition.loc[inst_template_id]['calendar'])
            calendar =list(map(str, calendar))
            freq = list(leg_definition.loc[inst_template_id]['frequency'])
            freq =list(map(str, freq))
            interest_day_convention = list(leg_definition.loc[inst_template_id]['interest_day_convention'])
            interest_day_convention =list(map(str, interest_day_convention))
            stub_policy = list(leg_definition.loc[inst_template_id]['stub_policy'])
            stub_policy =list(map(str, stub_policy))
            broken_period_type = list(leg_definition.loc[inst_template_id]['broken_period_type'])
            broken_period_type =list(map(str, broken_period_type))
            pay_day_offset = list(leg_definition.loc[inst_template_id]['pay_day_offset'])
            pay_day_offset =list(map(str, pay_day_offset))
            pay_day_convention = list(leg_definition.loc[inst_template_id]['pay_day_convention'])
            pay_day_convention =list(map(str, pay_day_convention))
            fixing_calendars = list(leg_definition.loc[inst_template_id]['fixing_calendars'])
            fixing_calendars =list(map(str, fixing_calendars))
            fixing_freq = list(leg_definition.loc[inst_template_id]['fixing_frequency'])
            fixing_freq =list(map(str, fixing_freq))
            fixing_day_convention = list(leg_definition.loc[inst_template_id]['fixing_day_convention'])
            fixing_day_convention =list(map(str, fixing_day_convention))
            fixing_mode = list(leg_definition.loc[inst_template_id]['fixing_mode'])
            fixing_mode =list(map(str, fixing_mode))
            fixing_day_offset = list(leg_definition.loc[inst_template_id]['fixing_day_offset'])
            fixing_day_offset =list(map(str, fixing_day_offset))
            start_convention = 'SPOT_START'                
            inst_template = create_ir_vanilla_swap_template(inst_name,
                                                            start_delay,
                                                            currency,
                                                            leg_type[0], day_count[0], ref_index[0], rate_calc_method[0], spread[0], calendar[0], freq[0], interest_day_convention[0], stub_policy[0], broken_period_type[0], pay_day_offset[0], pay_day_convention[0],
                                                            fixing_calendars[0].split(','), fixing_freq[0], fixing_day_convention[0], fixing_mode[0], fixing_day_offset[0],
                                                            leg_type[1], day_count[1], ref_index[1], rate_calc_method[1], spread[1], calendar[1], freq[1], interest_day_convention[1], stub_policy[1], broken_period_type[1], pay_day_offset[1], pay_day_convention[1],
                                                            fixing_calendars[1].split(','), fixing_freq[1], fixing_day_convention[1], fixing_mode[1], fixing_day_offset[1],
                                                            start_convention,
                                                            True,
                                                            self.data_loc)
            
            inst_templates = inst_templates.append({'inst_template_id': inst_template_id,
                                                   'inst_template': inst_template}, ignore_index=True)
                
        return inst_templates  

    def get_inst_template(self, inst_type, inst_name):
        inst_template_id = IrVanillaInstTemplateManager.create_inst_template_id(inst_type, inst_name)
        return self.inst_templates.loc[inst_template_id]['inst_template']

    def get_reference_rate(self, inst_type, inst_name):
        inst_template_id = IrVanillaInstTemplateManager.create_inst_template_id(inst_type, inst_name)
        ref_rate = self.leg_definition.loc[[inst_template_id]]['reference_rate'].tolist()
        ref_rate = list(map(str, ref_rate))        
        if 'nan' in ref_rate:
            ref_rate.remove('nan')
        return ref_rate
    
    def get_discount_curve(self, inst_type, inst_name):
        inst_template_id = IrVanillaInstTemplateManager.create_inst_template_id(inst_type, inst_name)
        leg_ccy = self.leg_definition.loc[[inst_template_id]]['leg_currency'].tolist()
        discount_curve = self.leg_definition.loc[[inst_template_id]]['discount_curve'].tolist()
        discount_curves = dict()
        for i in range(len(leg_ccy)):
            ccy = str(leg_ccy[i])
            if ccy != 'nan':
                discount_curves[ccy] = discount_curve[i]
        return discount_curves
    
    def get_fwd_curve(self, inst_type, inst_name):
        inst_template_id = IrVanillaInstTemplateManager.create_inst_template_id(inst_type, inst_name)
        ref_rate = self.leg_definition.loc[[inst_template_id]]['reference_rate'].tolist()        
        fwd_curve = self.leg_definition.loc[[inst_template_id]]['forward_curve'].tolist()
        fwd_curves = dict()
        for i in range(len(ref_rate)):
            rate = str(ref_rate[i])
            if rate != 'nan':
                fwd_curves[rate] = fwd_curve[i]
        return fwd_curves
    
    @staticmethod
    def create_inst_template_id(inst_type, inst_name):
        inst_template_id = inst_type.upper() + '_' + inst_name.upper()    
        return inst_template_id
    
    @staticmethod
    def create_inst_leg_template_id(inst_type, inst_name, leg_type, reference_rate):
        template_id = IrVanillaInstTemplateManager.create_inst_template_id(inst_type, inst_name)
        template_id = template_id + '_' + leg_type.upper()
        if reference_rate != '' and reference_rate != 'nan':
            template_id = template_id + '_' + reference_rate.upper() 
        return template_id
        
###############################################################################
if __name__ == "__main__":
    ir_vanilla_inst_template_manager = IrVanillaInstTemplateManager()        
    print('discount curve:', ir_vanilla_inst_template_manager.get_discount_curve('DEPOSIT', 'FR_007'))
    print('fwd curve:', ir_vanilla_inst_template_manager.get_fwd_curve('DEPOSIT', 'FR_007'))    
    print('discount curve:', ir_vanilla_inst_template_manager.get_discount_curve('DEPOSIT', 'SHIBOR_3M'))
    print('fwd curve:', ir_vanilla_inst_template_manager.get_fwd_curve('DEPOSIT', 'SHIBOR_3M')) 
    print('discount curve:', ir_vanilla_inst_template_manager.get_discount_curve('IR_VANILLA_SWAP', 'CNY_FR_007'))
    print('fwd curve:', ir_vanilla_inst_template_manager.get_fwd_curve('IR_VANILLA_SWAP', 'CNY_FR_007'))    
    print('discount curve:', ir_vanilla_inst_template_manager.get_discount_curve('IR_VANILLA_SWAP', 'CNY_SHIBOR_3M'))
    print('fwd curve:', ir_vanilla_inst_template_manager.get_fwd_curve('IR_VANILLA_SWAP', 'CNY_SHIBOR_3M')) 
    
