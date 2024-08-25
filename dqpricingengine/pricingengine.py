# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 16:16:02 2021

@author: dzhu
"""
import sys

from dqproto import *

###############################################################################
def create_pricing_model_settings(model_name,
                                  constant_model_params,
                                  term_structured_model_params,
                                  underlying,
                                  model_calibrated):
    '''
    @args:
        2. model_params: dict
    @return:
        
    '''
    try:
        p_model_name = PricingModelName.DESCRIPTOR.values_by_name[model_name.upper()].number
        p_constant_params = constant_model_params        
        p_model_params = term_structured_model_params        
        p_asset = underlying.upper()
        p_model_calibrated = bool(model_calibrated)
        settings = dqCreateProtoPricingModelSettings(p_model_name, 
                                                     p_constant_params, 
                                                     p_model_params, 
                                                     p_asset, 
                                                     p_model_calibrated)
        return settings
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))

###############################################################################        
def create_pde_settings(t_size, 
                        x_size, 
                        x_min, 
                        x_max, 
                        x_min_max_type, 
                        x_density, 
                        x_grid_type, 
                        x_interp_method, 
                        y_size, 
                        y_min, 
                        y_max, 
                        y_min_max_type, 
                        y_density, 
                        y_grid_type,
                        y_interp_method, 
                        z_size, 
                        z_min, 
                        z_max, 
                        z_min_max_type, 
                        z_density, 
                        z_grid_type, 
                        z_interp_method):
    '''
    @args:
        
    @return:
        
    '''
    try:
        p_t_size = t_size
        p_x_size = x_size 
        p_x_min = x_min 
        p_x_max = x_max 
        p_x_min_max_type = PdeSettings.MinMaxType.DESCRIPTOR.values_by_name[x_min_max_type.upper()].number
        p_y_size = y_size 
        p_y_min = y_min 
        p_y_max = y_max 
        p_y_min_max_type = PdeSettings.MinMaxType.DESCRIPTOR.values_by_name[y_min_max_type.upper()].number 
        p_z_size = z_size 
        p_z_min = z_min 
        p_z_max = z_max 
        p_z_min_max_type = PdeSettings.MinMaxType.DESCRIPTOR.values_by_name[z_min_max_type.upper()].number 
        p_x_density = x_density 
        p_y_density = y_density 
        p_z_density = z_density 
        p_x_grid_type = GridType.DESCRIPTOR.values_by_name[x_grid_type.upper()].number 
        p_y_grid_type = GridType.DESCRIPTOR.values_by_name[y_grid_type.upper()].number  
        p_z_grid_type = GridType.DESCRIPTOR.values_by_name[z_grid_type.upper()].number  
        p_x_interp_method = InterpMethod.DESCRIPTOR.values_by_name[x_interp_method.upper()].number  
        p_y_interp_method = InterpMethod.DESCRIPTOR.values_by_name[y_interp_method.upper()].number 
        p_z_interp_method = InterpMethod.DESCRIPTOR.values_by_name[z_interp_method.upper()].number 
        
        settings = dqCreateProtoPdeSettings(p_t_size, 
                                            p_x_size, 
                                            p_x_min, 
                                            p_x_max, 
                                            p_x_min_max_type, 
                                            p_y_size, 
                                            p_y_min, 
                                            p_y_max, 
                                            p_y_min_max_type, 
                                            p_z_size, 
                                            p_z_min, 
                                            p_z_max, 
                                            p_z_min_max_type, 
                                            p_x_density, 
                                            p_y_density, 
                                            p_z_density, 
                                            p_x_grid_type, 
                                            p_y_grid_type, 
                                            p_z_grid_type, 
                                            p_x_interp_method, 
                                            p_y_interp_method, 
                                            p_z_interp_method)
    
        return settings
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################        
def create_mc_settings(t_size, 
                        x_size, 
                        x_min, 
                        x_max, 
                        x_min_max_type, 
                        x_density, 
                        x_grid_type, 
                        x_interp_method, 
                        y_size, 
                        y_min, 
                        y_max, 
                        y_min_max_type, 
                        y_density, 
                        y_grid_type,
                        y_interp_method, 
                        z_size, 
                        z_min, 
                        z_max, 
                        z_min_max_type, 
                        z_density, 
                        z_grid_type, 
                        z_interp_method):
    '''
    @args:
        
    @return:
        
    '''
    try:
        p_num_simulations = num_sims
        p_uniform_number_type = UniformRandomNumberType.DESCRIPTOR.values_by_name[x_min_max_type.upper()].number
        p_seed = seed         
        p_wiener_process_build_method = WienerProcessBuildMethod.DESCRIPTOR.values_by_name[y_min_max_type.upper()].number         
        p_gaussian_number_method = GaussianNumberMethod.DESCRIPTOR.values_by_name[z_min_max_type.upper()].number
        p_use_antithetic = bool(antithetic) 
        p_num_steps = num_steps         
        settings = dqCreateProtoMonteCarloSettings(p_num_simulations, 
                                                   p_uniform_number_type, 
                                                   p_seed, 
                                                   p_wiener_process_build_method, 
                                                   p_gaussian_number_method, 
                                                   p_use_antithetic, 
                                                   p_num_steps)    
    
        return settings
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))