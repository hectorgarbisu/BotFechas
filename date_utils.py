
# -*- coding: utf-8 -*-
import datetime


month = "enero febrero marzo abril mayo junio julio agosto septiembre setiembre octubre noviembre diciembre".split()
week_day = u"lunes martes miercoles miércoles jueves viernes sabado sábado domingo".split()
cardinal = [str(x+1) for x in range(31)]
ordinal = u"primero segundo tercero cuarto quinto sexto séptimo septimo octavo noveno décimo decimo undécimo decimoprimero decimoprimer duodécimo decimosegundo".split()
# MOCK
def cardinal_to_date(str):
    return datetime.datetime.now()
# MOCK
def ordinal_to_date(str):
    return datetime.datetime.now()   
# MOCK
def next_weekday_to_date(str):
    return datetime.datetime.now()   
# MOCK
def thisweekday_to_date(str):
    return datetime.datetime.now()   
# MOCK
def update_day(date, str):
    return datetime.datetime.now()   
# MOCK
def is_month_day(str):
    return False  
# MOCK
def is_date(str):
    return False