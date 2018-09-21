import calendar
import datetime

# Stores and retrieves events at specific days, months, years, or weeks
# All JSON
class calendario(object):
    def __init__(self):
        self.cuac = 5
        today = datetime.date.today()
        self.years = {today.year : {
                        today.month : {
                            today.day : {
                                'weekday' : today.weekday(),
                                'events' : {}
                            }
                        }
                    }
        }

    def get_this_year (self):
        this_year = datetime.date.today().year
        return self.years[this_year]

    def get_this_month (self):
        this_month = datetime.date.today().month
        return self.get_this_year()[this_month]
    
    def get_today(self):
        this_day = datetime.date.today().day
        return self.get_this_month()[this_day]

    def get_this_week (self):
        days_from_monday = datetime.date.today().weekday()
        monday = datetime.date.today() - datetime.timedelta(days=days_from_monday)
        week = []
        for ii in range(7):
            delta = datetime.timedelta(days=ii)
            day = monday + delta
            week.append(self.years.get(day.year).get(day.month).get(day.day))
        return week



