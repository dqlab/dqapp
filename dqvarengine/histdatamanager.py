# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 22:52:52 2021

@author: dzhu
"""
from irflowhistdatamanager import IrFlowHistDataManager
from fxcashhistdatamanager import FxCashHistDataManager
from fxvolhistdatamanager import FxVolHistDataManager
from bondhistdatamanager import BondHistDataManager

###############################################################################
class HistDataManager:
    def __init__(self):
        self.ir_flow_hist_data_manager = IrFlowHistDataManager()
        self.fx_cash_hist_data_manager = FxCashHistDataManager()
        self.fx_vol_hist_data_manager = FxVolHistDataManager()
        self.bond_hist_data_manager = BondHistDataManager()