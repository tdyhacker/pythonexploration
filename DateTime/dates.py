#!/usr/bin/env python
import datetime

dates = ["2009-05-05 05:55:55", "2009-04-17 06:45:23"]

def convert_to_datetime(date):
    return datetime.datetime(year = int(date[0:4]), month = int(date[5:7]), day = int(date[8:10]), hour = int(date[11:13]), minute = int(date[14:16]), second = int(date[17:19]))
    
