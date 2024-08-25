# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:49:26 2021

@author: dzhu
"""

import pandas as pd

###############################################################################
class BondHistDataManager:
    def __init__(self, bond_yield_curve_template_manager, bond_sprd_curve_template_manager):
        data_loc = 'mktdata/histdata/fixedincome/bond/'

        self.data = dict()
        hist_data = pd.read_csv(data_loc + 'benchmark_bond.csv')
        hist_data.columns = hist_data.columns.str.lower()
        hist_data = hist_data.set_index('bond_id')  
        
        bonds = bond_yield_curve_template_manager.get_curve_bonds()
        bonds.extend(bond_sprd_curve_template_manager.get_curve_bonds())
        for bond in bonds:           
            tmp = hist_data.loc[bond][['date', 'yield']]            
            tmp = tmp.set_index('date')
            tmp = tmp.sort_index()
            tmp.loc[:,'change_in_percent'] = tmp['yield'].pct_change()
            tmp.loc[:,'change'] = tmp['yield'].diff()
            self.data[bond] = tmp
    
    def get_data(self, bond_names, start, end, data_type='yield'):
        '''
            @args:
                1. bond_names: list of string
                2. start: string, start date
                3. end: string, end date
                4. data_type: string, {'yield', 'change', 'change_in_percent'}
            @return:
                pandas.DataFrame, index = {'date'}, columns = {bond_names}
        '''
        data = pd.DataFrame()
        for name in bond_names:          
            tmp = pd.DataFrame(self.data[name][data_type])
            tmp = tmp.loc[start : end]
            tmp = tmp.rename(columns={data_type: name})            
            data = pd.concat([data,tmp],axis=1)
        return data
    
    def get_hist_data(self, bond_names, base_date, num, data_type = 'change'):
        data = pd.DataFrame()
        for name in bond_names: 
            tmp = pd.DataFrame(self.data[name][data_type])
            base_index = tmp.index.get_loc(base_date)
            
            if num < 0:
                tmp = tmp.iloc[base_index + num + 1 : base_index + 1]
            else:
                tmp = tmp.iloc[base_index : base_index + num + 1]
            tmp = tmp.rename(columns={data_type: name})            
            data = pd.concat([data,tmp],axis=1)
        return data
    
    def get_stressed_data(self, bond_names, stressed_dates, data_type = 'change'):
        data = pd.DataFrame()
        for name in bond_names: 
            tmp = pd.DataFrame(self.data[name][data_type])
            tmp = tmp.reindex(stressed_dates)
            tmp = tmp.rename(columns={data_type: name})            
            data = pd.concat([data,tmp],axis=1)
        return data
        
###############################################################################
if __name__ == "__main__":
    from bondyieldcurvetemplatemanager import BondYieldCurveTemplateManager
    from bondsprdcurvetemplatemanager import BondSprdCurveTemplateManager
    
    bond_yield_curve_template_manager = BondYieldCurveTemplateManager()
    bond_sprd_curve_template_manager = BondSprdCurveTemplateManager()
    manager = BondHistDataManager(bond_yield_curve_template_manager, bond_sprd_curve_template_manager)
    changes = manager.get_data(['CNY_TREASURY_BOND_CFETS_1Y', 'CNY_TREASURY_BOND_CFETS_2Y'], '2021-05-22', '2021-07-22', data_type = 'change')
    print(changes)
    changes = manager.get_data(['CNY_TREASURY_BOND_CFETS_6M'], '2021-05-22', '2021-07-22', data_type = 'change')
    print(changes)
    changes = manager.get_hist_data(['CNY_TREASURY_BOND_CFETS_1Y', 'CNY_TREASURY_BOND_CFETS_2Y'], '2021-07-22', -10, data_type = 'change')
    print(changes)
    stress_changes = manager.get_stressed_data(['CNY_TREASURY_BOND_CFETS_1Y', 'CNY_TREASURY_BOND_CFETS_2Y'], ['2021-05-21', '2021-07-22'], data_type = 'change')
    print(stress_changes)
    
    