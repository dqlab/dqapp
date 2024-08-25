# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 11:18:13 2021

@author: dingq
"""
import numpy as np
import pandas as pd

class Bond:
    def __init__(self, nominal):
        self.nominal = nominal
        
    def num_cpns(self, reference_date):
        return len(self.leg.loc[(self.leg['pay'] > reference_date)])
        
    def maturity(self):
        mat = self.leg.iloc[len(self.leg)-1]['pay']
        return mat
    
    def cpn_period(self, reference_date):
        tmp = self.leg.loc[(self.leg['start']<=reference_date)&(self.leg['end']>reference_date)]
        start = tmp['start']
        end = tmp['end']
        pay = tmp['pay']
        return start, end, pay
        
class FixedCpnBond:
    def __init__(self, cpn_rate, cpn_freq, cpn_dates, maturity):
        '''
        cpn period: (start, end, pay)
        '''
        self.cpn_rate = cpn_rate
        self.cpn_freq = cpn_freq
        self.maturity = maturity

def ccdc_fixed_cpn_bond_pv_formula(ytm, tau, num_cpns, cpn_rate, cpn_freq, nominal):
    npv = 0.0
    if num_cpns > 1:
        #more than 1 cpn periods:
        for i in range(num_cpns):
            cpn_pv = (cpn_rate / cpn_freq) / pow(1. + ytm / cpn_freq, tau + i)
            npv = npv + cpn_pv * nominal
        npv = npv + nominal / pow(1. + ytm / cpn_freq, tau + num_cpns-1)        
    else:
         #only 1 cpn period left:
        npv = nominal * (cpn_rate / freq + 1.0)
        npv = npv / (1.0 + ytm * tau)
    return npv

def FixedCpnBondPricer(pricing_date, bond, ytm):
    '''
    CCDC Methodlogy
    '''
    start, end, pay = bond.cpn_period(pricing_date)
    act_days = end - pricing_date
    cpn_days = end - start
    tau = act_days / cpn_days
    num_cpns = bond.num_cpns(pricing_date)    
    return ccdc_fixed_cpn_bond_pv_formula(ytm, tau, num_cpns, bond.cpn_rate, bond.cpn_freq)
    
class ZeroCpnBond:
    def __init__(self, maturity, issue_price):
        self.maturity = maturity
        self.issue_price = issue_price

def ZeroCpnBondPricer(pricing_date, bond, ytm):
    return 0.0        


###############################################################################
def cubic_hermite_interp(x_val, y_val, x_deriv, x_interp):
    x_lst = [x_interp] if isinstance(x_interp, (float, int)) else x_interp
    x_loc = np.searchsorted(x_val, x_lst)
    res_lst = []
    for x, i in zip(x_lst, x_loc):
        h_i = x_val[i] - x_val[i-1]
        H_i = (1 + 2 * (x - x_val[i-1]) / h_i) * ((x - x_val[i]) / h_i) ** 2 * y_val[i-1] + \
              (1 + 2 * (x_val[i] - x) / h_i) * ((x - x_val[i-1]) / h_i) ** 2 * y_val[i] + \
              (x - x_val[i-1]) * ((x - x_val[i]) / h_i) ** 2 * x_deriv[i-1] + \
              (x - x_val[i]) * ((x - x_val[i-1]) / h_i) ** 2 * x_deriv[i]        
        res_lst.append(H_i)    
    return res_lst

################################################################################
#分段三次埃尔米特插值
ytm_curve = pd.read_excel('C:\work\App\QuantExplorer\ytm_curve.xlsx')
mat =ytm_curve['T'].to_numpy()
ytm = ytm_curve['YTM'].to_numpy()
ytm = ytm * 0.01
dT = mat[1:] - mat[:-1]
dY = ytm[1:] - ytm[:-1]
k=np.zeros(len(ytm))   #端点处导数
k[:-1] = dY/dT
t=np.linspace(0.05, 50.05, num = 501)
H1 = cubic_hermite_interp(mat,ytm,k,t[10])   #获得分段三次埃尔米特插值函数
