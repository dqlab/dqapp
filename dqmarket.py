import sys

from dqproto import *

'''###############################To Currency Pair##########################'''
def to_currency_pair(ccy_pair):
    '''
    args:
        1. ccy_pair: string, i.e.'3M'
    return:
        dqproto.CurrencyPair
    '''
    try:
        left = ccy_pair[0:3]
        right = ccy_pair[3:6]
        left = dqCreateProtoCurrency(CurrencyName.DESCRIPTOR.values_by_name[left.upper()].number)
        right = dqCreateProtoCurrency(CurrencyName.DESCRIPTOR.values_by_name[right.upper()].number)
        
        return dqCreateProtoCurrencyPair(left, right)
    
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
