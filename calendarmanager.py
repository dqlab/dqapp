# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 17:54:55 2021

@author: dzhu
"""
import pandas as pd
import dqlib
from utility import save_pb_data, to_excel_date

#Calendar Manager
class CalendarManager:
    def __init__(self):
        self.holiday_data = pd.read_csv('staticdata/calendar/holidaydata.csv')
        self.holiday_data.columns = self.holiday_data.columns.str.lower()
        cal_names = set(self.holiday_data['calendar'])
        for name in cal_names:
            dqlib.create_calendar(name, 
                                  list(self.holiday_data[self.holiday_data['calendar']==name]['holiday']), 
                                  False, '')
            
###############################################################################
if __name__ == "__main__":
    calendar_manager = CalendarManager()
    print(calendar_manager.holiday_data)
        