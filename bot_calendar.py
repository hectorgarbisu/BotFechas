import calendar
import datetime, time

# Stores and retrieves events at specific days, months, years, or weeks
class calendario(object):
    def __init__(self):
        #days_from_epoch = int(time.mktime(datetime.date.today().timetuple()))/(24*60*60)
        self.events = { }
        
    def add_event (self, event, date):
        num = self.date_to_total_days(date)
        if num in self.events:
            self.events[num].append(event)
        else :
            self.events[num] = [event]

    def date_to_total_days(self, date):
        return int(time.mktime(date.timetuple()))/(24*60*60)

    def get_this_week (self):
        days_from_monday = datetime.date.today().weekday()
        monday = datetime.date.today() - datetime.timedelta(days=days_from_monday)
        week = []
        for ii in range(7):
            delta = datetime.timedelta(days=ii)
            day = monday + delta
            if self.date_to_total_days(day) in self.events:
                week.append(self.events[self.date_to_total_days(day)])
        return week

def main():
    cal = calendario()
    cal.add_event(" esto es un evento ", datetime.date.today())
    cal.add_event(" esto es otro evento el mismo dia",datetime.date.today() )
    cal.add_event(" esto es otro evento otro dia",datetime.date(2018, 10, 14))
    print cal.events
    print cal.get_this_week()

if __name__ == "__main__":
    main()


