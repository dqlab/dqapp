# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 07:38:36 2021

@author: dzhu
"""
from dqmarket import *

def tet_to_currency_pair():
    res = to_currency_pair('usdcny')
    print(res)
    test = (res.left_currency == USD) and (res.right_currency == CNY)
    return test

###############################################################################
tet_to_currency_pair()