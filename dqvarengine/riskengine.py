# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 13:03:06 2021

@author: dzhu
"""

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *

###############################################################################
def calculate_risk_factor_change(risk_factor_values, change_type):
    '''
    '''
    p_type = RiskFactorChangeType.DESCRIPTOR.values_by_name[change_type.upper()].number 
    p_samples = list(risk_factor_values)
    pb_input = dqCreateProtoRiskFactorChangeCalculationInput(p_type, p_samples)
    req_name = 'RISK_FACTOR_CHANGE_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('RISK_FACTOR_CHANGE_CALCULATOR ProcessRequest: failed!')
    pb_output = RiskFactorChangeCalculationOutput()
    pb_output.ParseFromString(res_msg)    
    return pb_output.result

###############################################################################
def simulate_risk_factor(risk_factor_changes, change_type, base):
    '''
    '''
    p_type = RiskFactorChangeType.DESCRIPTOR.values_by_name[change_type.upper()].number 
    p_changes = list(risk_factor_values)
    p_base = float(base)
    pb_input = dqCreateProtoRiskFactorSimulationInput(p_type, p_changes, p_base)    
    req_name = 'RISK_FACTOR_SIMULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('RISK_FACTOR_SIMULATOR ProcessRequest: failed!')
    pb_output = RiskFactorSimulationOutput()
    pb_output.ParseFromString(res_msg)    
    return pb_output.result
    
###############################################################################
def calculate_expected_shortfall(pnls, prob, mirror):
    '''
    '''
    p_profit_loss_samples = dqCreateProtoVector(list(pnls))
    p_probability = float(prob)
    p_calc_es_mirrored = bool(mirror)
    pb_input = dqCreateProtoCalculateExpectedShortfallInput(p_profit_loss_samples, 
                                                            p_probability, 
                                                            p_calc_es_mirrored)
    req_name = 'CALCULATE_EXPECTED_SHORT_FALL'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('CALCULATE_EXPECTED_SHORTFALL ProcessRequest: failed!')
    pb_output = CalculateExpectedShortfallOutput()
    pb_output.ParseFromString(res_msg)    
    return pb_output.expected_shortfall, pb_output.expected_shortfall_mirrored

###############################################################################
def calculate_value_at_risk(pnls, prob, mirror):
    '''
    '''    
    p_profit_loss_samples = dqCreateProtoVector(list(pnls))    
    p_probability = float(prob)
    p_calc_var_mirrored = bool(mirror)
    pb_input = dqCreateProtoCalculateValueAtRiskInput(p_profit_loss_samples, 
                                                      p_probability, 
                                                      p_calc_var_mirrored)
    req_name = 'CALCULATE_VALUE_AT_RISK'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
    if res_msg == None:
        raise Exception('CALCULATE_VALUE_AT_RISK ProcessRequest: failed!')
    pb_output = CalculateValueAtRiskOutput()
    pb_output.ParseFromString(res_msg)    
    return pb_output.value_at_risk, pb_output.value_at_risk_mirrored