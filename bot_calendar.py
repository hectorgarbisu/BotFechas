import calendar
import datetime
import time
from calendar import monthrange

# Stores and retrieves events at specific days, months, years, or weeks


class calendario(object):
    def __init__(self):
        #days_from_epoch = int(time.mktime(datetime.date.today().timetuple()))/(24*60*60)
        self.events = {}

    def add_event(self, event, date):
        """ add_event (event, date): saves string event at date """
        num = self.date_to_total_days(date)
        if num in self.events:
            self.events[num].append(event)
        else:
            self.events[num] = [event]

    def date_to_total_days(self, date=datetime.date.today()):
        return int(time.mktime(date.timetuple()))//(24*60*60)

    def get_this_week(self):
        days_from_monday = datetime.date.today().weekday()
        monday = datetime.date.today() - datetime.timedelta(days=days_from_monday)
        return self.get_days(7, monday)

    def get_this_month(self):
        today = datetime.date.today()
        return self.get_days(monthrange(today.year, today.month)[1], datetime.date(today.year, today.month, 1))

    def get_days(self, days=1, from_day=datetime.date.today()):
        lapse = []
        for ii in range(days):
            delta = datetime.timedelta(days=ii)
            day = from_day + delta
            if self.date_to_total_days(day) in self.events:
                events_in_day = self.events[self.date_to_total_days(day)]
                for event in events_in_day:
                    lapse.append(event)
        return lapse

    def delete_all(self):
        self.events = {}

    def delete_old(self):
        self.events = {k: v for k, v in self.events.items() if k > self.date_to_total_days()}

def main():
    cal = calendario()
    today = datetime.date.today()
    cal.add_event(" esto es un evento ", today)
    cal.add_event(" esto es otro evento el mismo dia", today)
    cal.add_event(" esto es otro evento otro dia", datetime.date(2018, 10, 14))
    cal.add_event(" evento de ayer ", today + datetime.timedelta(days=-1))
    cal.add_event(" evento de principios de mes  ",
                  datetime.date(today.year, today.month, 1))
    cal.add_event(" evento de final de mes  ", datetime.date(2018, 10, 31))
    cal.add_event(" evento de otro mes  ", datetime.date(2018, 11, 1))
    print(cal.events)
    print(cal.get_this_week())
    print(cal.get_this_month())
    print(cal.get_days(20))
    cal.delete_old()
    print(cal.events)


if __name__ == "__main__":
    main()
