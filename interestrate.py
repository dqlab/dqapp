# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 02:26:41 2021

@author: dzhu
"""

###############################################################################
def create_ir_par_curve(as_of_date,
                        currency,
                        pillar_data,
                        curve_name):
    '''
    @args:
        3. pillar_data: pandas.DataFrame, columns=['name','type','term','quote','factor']
    @return:
        dqproto.IrParRateCurve
    '''
    try:
        p_as_of_date = to_date(as_of_date, '%Y-%m-%d')
        p_currency = CurrencyName.DESCRIPTOR.values_by_name[discount_curve_settings[0].upper()].number
        p_curve_name = curve_name.upper()
        p_inst_names = list()
        p_inst_types = list()
        p_inst_terms = list()
        p_factors = list()
        p_quotes = list()
        p_start_conventions = list()

        for i in range(len(pillar_data)):
            p_inst_name = pillar_data.iloc[i]['name']
            p_inst_names.append(p_inst_name.upper())            
            p_inst_type = pillar_data.iloc[i]['type']
            p_inst_types.append(p_inst_type.upper())
            p_term = pillar_data.iloc[i]['term']
            p_inst_terms.append(p_term.upper())
            p_quote = pillar_data.iloc[i]['quote']
            p_quotes.append(p_quote)
            p_factor = pillar_data.iloc[i]['factor']
            p_factors.append(p_factor)
            if p_term.upper() == 'ON':
                p_start_conventions.append('TODAY_START')
            elif p_term.upper() == 'TN':
                p_start_conventions.append('TOMORROW_START')
            else:
                p_start_conventions.append('SPOT_START')
        pb_input = dqCreateProtoCreateIrParRateCurveInput(p_as_of_date, 
                                                          p_currency, 
                                                          p_curve_name, 
                                                          p_inst_names, 
                                                          p_inst_types, 
                                                          p_inst_terms, 
                                                          p_factors, 
                                                          p_quotes, 
                                                          p_start_conventions)
        
        req_name = 'CREATE_IR_PAR_RATE_CURVE'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = CreateIrParRateCurveOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.ir_par_rate_curve
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def create_ir_yield_curve_build_settings(curve_name,                                     
                                         discount_curve_settings,
                                         fwd_curve_settings,
                                         use_on_tn_fx_swap):
    '''
    @args:
        1. 
        2. discount_curve_settings: list of list of 2 elements, where [0]: currency; [1]: curve name
        3. fwd_curve_settings: list of list of 2 elements, where [0]: reference index; [1]: curve name
    @return:
        dqproto.IrYieldCurveBuildSettings
    '''
    try:
        p_discount_curve_settings = list()
        for s in discount_curve_settings:
            p_currency_name = CurrencyName.DESCRIPTOR.values_by_name[s[0].upper()].number
            p_discnt_curve_name = s[1].lower()        
            p_discount_curve_settings.append(dqCreateProtoCreateIrYieldCurveBuildSettingsInput_DiscountCurveSettings(p_currency_name, 
                                                                                                                     p_discnt_curve_name))
    
        p_forward_curve_settings = list()
        for s in discount_curve_settings:
            p_ref_index_name = s[0].lower()
            p_fwd_curve_name = s[1].lower()
            p_forward_curve_settings.append(dqCreateProtoCreateIrYieldCurveBuildSettingsInput_ForwardCurveSettings(p_ref_index_name, 
                                                                                                                   p_fwd_curve_name))
    
        p_curve_name = curve_name.lower()
        p_use_on_tn_fx_swap = bool(use_on_tn_fx_swap)
        pb_build_settings = dqCreateProtoCreateIrYieldCurveBuildSettingsInput(p_curve_name, 
                                                                              p_use_on_tn_fx_swap, 
                                                                              p_discount_curve_settings, 
                                                                              p_forward_curve_settings)
        
        return pb_build_settings    
        
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))

###############################################################################        
def build_ir_single_ccy_yield_curve(as_of_date,
                                    build_settings, 
                                    par_curves,
                                    curve_settings,
                                    other_curves,
                                    build_method,
                                    calc_jacobian):
    '''
    @args:
        2. build_settings: dict, <key, value> = <curve name, settings>
        3. par_curves: dict, <key, value> = <curve name, par curve>
        4. curve_settings: pandas.DataFrame
        9. other_curves: list of dqproto.IrYieldCurve
    @return:
        dqproto.IrYieldCurve
    '''
    try:
        p_build_settings = list()
        for i in len(range(curve_settings)):            
            p_target_curve_name = curve_settings.iloc[i]['curve_name'].lower()
            p_bond_yield_curve_build_settings = build_settings[p_target_curve_name]
            p_par_curve = par_curves[p_target_curve_name]
            p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[curve_settings.iloc[i]['day_count'].upper()].number
            p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[curve_settings.iloc[i]['compounding_type'].upper()].number
            p_frequency = Frequency.DESCRIPTOR.values_by_name[curve_settings.iloc[i]['frequency'].upper()].number
            p_to_settlement = bool(curve_settings.iloc[i]['to_settlement'])
            pb_settings_container = dqCreateProtoIrSingleCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(p_target_curve_name, 
                                                                                                                       p_ir_yield_curve_build_settings, 
                                                                                                                       p_par_curve, 
                                                                                                                       p_day_count_convention, 
                                                                                                                       p_compounding_type, 
                                                                                                                       p_frequency, 
                                                                                                                       p_to_settlement)
            p_build_settings.append(pb_settings_container)
    
        p_reference_date = to_date(as_of_date, '%Y-%m-%d')
        p_other_curves = other_curves        
        p_building_method = IrYieldCurveBuildingMethod.DESCRIPTOR.values_by_name[build_method.upper()].number
        p_calc_jacobian = bool(calc_jacobian)
        
        pb_input = dqCreateProtoIrSingleCurrencyCurveBuildingInput(p_reference_date, 
                                                                   p_build_settings, 
                                                                   p_other_curves, 
                                                                   p_building_method)
        
        req_name = 'IR_SINGLE_CURRENCY_CURVE_BUILDER'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = IrSingleCurrencyCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.target_curves
            
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################        
def build_ir_cross_ccy_yield_curve(as_of_date,
                                   build_settings, 
                                   par_curves,
                                   curve_settings,
                                   other_curves,
                                   fx_spot):
    '''
    @args:
        2. build_settings: dict, <key, value> = <curve name, settings>
        3. par_curves: dict, <key, value> = <curve name, par curve>
        4. curve_settings: pandas.DataFrame
        9. other_curves: list of dqproto.IrYieldCurve
    @return:
        dqproto.IrYieldCurve
    '''
    try:
        p_build_settings = list()
        for i in len(range(curve_settings)):            
            p_target_curve_name = curve_settings.iloc[i]['curve_name'].lower()
            p_ir_yield_curve_build_settings = build_settings[p_target_curve_name]
            p_par_curve = par_curves[p_target_curve_name]
            p_day_count_convention = DayCountConvention.DESCRIPTOR.values_by_name[curve_settings.iloc[i]['day_count'].upper()].number
            p_compounding_type = CompoundingType.DESCRIPTOR.values_by_name[curve_settings.iloc[i]['compounding_type'].upper()].number
            p_frequency = Frequency.DESCRIPTOR.values_by_name[curve_settings.iloc[i]['frequency'].upper()].number
            p_to_settlement = bool(curve_settings.iloc[i]['to_settlement'])
            pb_settings_container = dqCreateProtoIrSingleCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(p_target_curve_name, 
                                                                                                                       p_ir_yield_curve_build_settings, 
                                                                                                                       p_par_curve, 
                                                                                                                       p_day_count_convention, 
                                                                                                                       p_compounding_type, 
                                                                                                                       p_frequency, 
                                                                                                                       p_to_settlement)
            p_build_settings.append(pb_settings_container)
    
        p_reference_date = to_date(as_of_date, '%Y-%m-%d')
        p_other_curves = other_curves        
        p_fx_spot = fx_spot
        pb_input = dqCreateProtoIrCrossCurrencyCurveBuildingInput(p_reference_date, 
                                                                  p_build_settings, 
                                                                  p_other_curves, 
                                                                  p_fx_spot)
        
        req_name = 'IR_CROSS_CURRENCY_CURVE_BUILDER'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = IrCrossCurrencyCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.target_curves
            
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        

###############################################################################
def create_ir_mkt_data_set(as_of_date,
                           discount_curves,
                           forward_curves,
                           capfloor_vol_surfs,
                           swaption_vol_surfs,
                           swaption_quote_cubes,
                           fx_spot_rate):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        2. discount_curve: dqproto.IrYieldCurve
        4. forward_curve: dqproto.IrYieldCurve
        5. underlying: string
    @return:
        dqproto.IrMktDataSet
    '''
    try: 
        p_as_of_date = to_date(as_of_date, '%Y-%m-%d')   
        p_fx_spot = fx_spot_rate
        p_use_binary = False
        p_fx_spot_bin = b''
        
        p_discount_curves = list()
        for name in discount_curves.keys():
            p_name = name
            p_curve = discount_curves[name]
            p_curve_bin=b''
            p_map = dqCreateProtoIrMktDataSet_DiscountCurveMap(p_name, 
                                                               p_curve, 
                                                               p_curve_bin)
            p_discount_curves.append(p_map)
            
        p_forward_curves = list()
        for name in forward_curves.keys():
            p_name = name
            p_curve = forward_curves[name]
            p_curve_bin=b''
            p_map = dqCreateProtoIrMktDataSet_ForwardCurveMap(p_name, 
                                                              p_curve, 
                                                              p_curve_bin)
            p_forward_curves.append(p_map)
            
        p_capfloor_vol_surfs = list()
        for name in capfloor_vol_surfs.keys():
            p_name = name
            p_surf = capfloor_vol_surfs[name]
            p_surf_bin=b''
            p_map = dqCreateProtoIrMktDataSet_IrCapFloorVolSurfMap(p_name, 
                                                                   p_surf, 
                                                                   p_surf_bin)
            p_capfloor_vol_surfs.append(p_map)
            
        p_swaption_vol_surfs = list()
        for name in swaption_vol_surfs.keys():
            p_name = name
            p_surf = swaption_vol_surfs[name]
            p_surf_bin=b''
            p_map = dqCreateProtoIrMktDataSet_IrSwaptionVolSurfMap(p_name, 
                                                                   p_surf, 
                                                                   p_surf_bin)
            p_swaption_vol_surfs.append(p_map)
            
        p_swaption_quote_cubes = list()
        for name in swaption_quote_cubes.keys():
            p_name = name
            p_cube = swaption_quote_cubes[name]
            p_cube_bin=b''
            p_map = dqCreateProtoIrMktDataSet_IrSwaptionQuoteCubeMap(p_name, 
                                                                     p_cube, 
                                                                     p_cube_bin)
            p_swaption_quote_cubes.append(p_map)
            
        
        mds = dqCreateProtoIrMktDataSet(p_as_of_date, 
                                        p_discount_curves, 
                                        p_forward_curves, 
                                        p_capfloor_vol_surfs, 
                                        p_swaption_vol_surfs, 
                                        p_swaption_quote_cubes, 
                                        p_fx_spot, 
                                        p_use_binary, 
                                        p_fx_spot_bin)
    
        
        return mds
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))

###############################################################################
def build_ir_future():    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        print('to be implemented!')
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))        

###############################################################################
def build_deposit(reference_date,
                  inst_name,
                  tenor,
                  rate,
                  pay_receive,
                  nominal,
                  currency):    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        p_reference_date = to_date(reference_date, '%Y-%m-%d')
        p_inst_name = inst_name.upper()
        p_tenor = to_period(tenor)
        p_rate = rate
        p_pay_receive = PayReceiveFlag.DESCRIPTOR.values_by_name[pay_receive.upper()].number
        p_notional = dqCreateProtoNotional(nominal, currency)
        pb_input = dqCreateProtoCreateIrDepositInput(p_reference_date, 
                                                     p_inst_name, 
                                                     p_tenor, 
                                                     p_rate, 
                                                     p_pay_receive, 
                                                     p_notional)
        
        req_name = 'CREATE_IR_DEPOSIT'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = CreateIrDepositOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.inst
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        
###############################################################################
def build_forward_rate_agreement():    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        print('to be implemented!')
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))    
        
###############################################################################
def build_ir_vanilla_swap(inst_name,
                          start_date,
                          maturity,
                          pay_receive,
                          fixed_rate,
                          spread,
                          nominal,
                          currency
                          ibor_fixings):    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        p_start_date = to_date(start_date, '%Y-%m-%d')
        p_inst_name = inst_name.upper() 
        p_maturity_date = to_date(maturity, '%Y-%m-%d')
        p_pay_receive = PayReceiveFlag.DESCRIPTOR.values_by_name[pay_receive.upper()].number
        p_fixed_rate = fixed_rate
        p_spread = spread
        p_notional = dqCreateProtoNotional(nominal, 
                                           currency)        
        p_fixings = list()
        for f in ibor_fixings.keys():
            p_name = f.upper()
            p_time_series = ibor_fixings[f]
            p_ts_map = dqCreateProtoTimeSeriesMap(p_name, p_time_series)
            p_fixings.append(p_ts_map)        
        p_leg_fixings = dqCreateProtoLegFixings(p_fixings)
        
        pb_input = dqCreateProtoBuildIrVanillaSwapInput(p_start_date, 
                                                        p_inst_name, 
                                                        p_maturity_date, 
                                                        p_pay_receive, 
                                                        p_fixed_rate, 
                                                        p_spread, 
                                                        p_notional, 
                                                        p_leg_fixings)
        
        req_name = 'BUILD_IR_VANILLA_SWAP'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = BuildIrVanillaSwapOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.inst
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))    

###############################################################################
def build_cross_ccy_swap():    
    '''
    @args:
        
        
    @return:
        
    '''
    try:
        print('to be implemented!')
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        
###############################################################################       
def ir_vanilla_instrument_pricer(pricing_date,
                                 instrument,
                                 mkt_data_set,
                                 risk_settings):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        
    @return:
        dqproto.IrPricingResult
    '''
    try:
        p_pricing_date = to_date(pricing_date, '%Y-%m-%d')
        p_instrument = instrument
        p_mkt_data = mkt_data_set
        p_pricing_settings = PricingSettings()
        p_risk_settings = risk_settings
        p_use_binary = False
        p_instrument_bin = b''
        p_mkt_data_bin = b''
        p_pricing_settings_bin = b''
        p_risk_settings_bin = b''
        p_name = ''
        pb_input = dqCreateProtoIrVanillaInstrumentPricingInput(p_pricing_date, 
                                                                p_instrument, 
                                                                p_mkt_data, 
                                                                p_pricing_settings, 
                                                                p_risk_settings, 
                                                                p_use_binary, 
                                                                p_instrument_bin, 
                                                                p_mkt_data_bin, 
                                                                p_pricing_settings_bin, 
                                                                p_risk_settings_bin)
        req_name = 'IR_VANILLA_INSTRUMENT_PRICER'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = IrVanillaInstrumentPricingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.results
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################       
def cross_ccy_swap_pricer(pricing_date,
                          instrument,
                          mkt_data_set,
                          risk_settings):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        
    @return:
        dqproto.IrPricingResult
    '''
    try:
        p_pricing_date = to_date(pricing_date, '%Y-%m-%d')
        p_instrument = instrument
        p_mkt_data = mkt_data_set
        p_pricing_settings = PricingSettings()
        p_risk_settings = risk_settings
        p_use_binary = False
        p_instrument_bin = b''
        p_mkt_data_bin = b''
        p_pricing_settings_bin = b''
        p_risk_settings_bin = b''
        p_name = ''
        pb_input = dqCreateProtoIrCrossCurrencySwapPricingInput(p_pricing_date, 
                                                                p_instrument,                                                                
                                                                p_pricing_settings, 
                                                                p_mkt_data, 
                                                                p_risk_settings, 
                                                                p_use_binary, 
                                                                p_instrument_bin,                                                                 
                                                                p_pricing_settings_bin, 
                                                                p_mkt_data_bin, 
                                                                p_risk_settings_bin)
        req_name = 'IR_CROSS_CURRENCY_SWAP_PRICER'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = IrCrossCurrencySwapPricingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.results
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################       
def mtm_cross_ccy_swap_pricer(pricing_date,
                              instrument,
                              mkt_data_set,
                              risk_settings):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        
    @return:
        dqproto.IrPricingResult
    '''
    try:
        p_pricing_date = to_date(pricing_date, '%Y-%m-%d')
        p_instrument = instrument
        p_mkt_data = mkt_data_set
        p_pricing_settings = PricingSettings()
        p_risk_settings = risk_settings
        p_use_binary = False
        p_instrument_bin = b''
        p_mkt_data_bin = b''
        p_pricing_settings_bin = b''
        p_risk_settings_bin = b''
        p_name = ''
        pb_input = dqCreateProtoIrMarkToMarketCrossCurrencySwapPricingInput(p_pricing_date, 
                                                                            p_instrument,                                                                             
                                                                            p_pricing_settings, 
                                                                            p_mkt_data, 
                                                                            p_risk_settings, 
                                                                            p_use_binary, 
                                                                            p_instrument_bin,                                                                             
                                                                            p_pricing_settings_bin, 
                                                                            p_mkt_data_bin, 
                                                                            p_risk_settings_bin)
        req_name = 'IR_MTM_CROSS_CURRENCY_SWAP_PRICER'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = IrMarkToMarketCrossCurrencySwapPricingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.results
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
 
############################################################################### 
def discount_factor(term_date,
                    ir_yield_curve):
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        
    @return:
        dqproto.IrPricingResult
    '''
    try:
        p_discount_date = to_date(term_date, '%Y-%m-%d')
        p_ir_yield_curve = ir_yield_curve
        pb_input = dqCreateProtoDiscountFactorCalculationInput(p_discount_date, 
                                                               p_ir_yield_curve)
        req_name = 'DISCOUNT_FACTOR_CALCULATOR'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = DiscountFactorCalculationOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.discount_factor
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def ibor_index_rate_calculator(as_of_date,
                               fixing_date,
                               ibor_index,
                               forward_curve):        
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        
    @return:
        double
    '''
    try:
        p_calculate_date = to_date(as_of_date, '%Y-%m-%d')
        p_fixing_date = to_date(fixing_date, '%Y-%m-%d')
        p_ibor_index = IborIndexName.DESCRIPTOR.values_by_name[ibor_index.upper()].number
        p_ir_yield_curve = forward_curve
        pb_input = dqCreateProtoIborIndexRateCalculationInput(p_calculate_date, 
                                                              p_fixing_date, 
                                                              p_ibor_index, 
                                                              p_ir_yield_curve)
        req_name = 'IBOR_INDEX_RATE_CALCULATOR'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = IborIndexRateCalculationOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.ibor_index_rate
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
###############################################################################
def ir_vanilla_swap_rate_calculator(as_of_date,
                                    inst_name,
                                    tenor,
                                    discount_curve,
                                    forward_curve):        
    '''
    @args:
        1. as_of_date: string, format='%Y-%m-%d'
        
    @return:
        double
    '''
    try:
        p_calculation_date = to_date(as_of_date, '%Y-%m-%d')
        p_instrument_name = inst_name.upper()
        p_tenor = to_period(tenor)
        p_discount_curve = discount_curve
        p_forward_curve = forward_curve
        pb_input = dqCreateProtoIrVanillaSwapRateCalculationInput(p_calculation_date, 
                                                                  p_instrument_name, 
                                                                  p_tenor, 
                                                                  p_discount_curve, 
                                                                  p_forward_curve)
        req_name = 'IR_VANILLA_SWAP_RATE_CALCULATOR'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())        
        
        pb_output = IrVanillaSwapRateCalculationOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.swap_rate
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))