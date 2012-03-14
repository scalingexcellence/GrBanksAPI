import time
from decimal import *

FILTER_ALL = lambda row: True

FILTER_POSITIVE = lambda row: row['amount']>0

FILTER_NEGATIVE = lambda row: row['amount']<0

class Type:
    ROW=1
    CURRENCY=2

def format_day(row):
    return time.strftime('%d/%m/%Y',row['date'])
    
FORMAT_DEFAULT = lambda row, type = Type.ROW: (format_day(row), row['name'], row['amount'], row['description']) if type == Type.ROW else row

def FORMAT_SUPERSIZE_ME(row, type = Type.ROW):
    if type == Type.ROW:
        return (format_day(row), row['name'], row['amount']*100, row['description'])
    else:
        return row*100
    