from calendar import month
from datetime import time
# ============================================== Set Up ==============================================
import datetime
from numpy import append
from datetime import time

# ============================================== Class ===============================================
class DifferenceTime:
    _Years = 0
    _Months = 0
    _Days = 0
    _Hours = 0
    _Minutes = 0
    _Seconds = 0

# =========================================== Constructor ============================================
    def __init__(self, years = 0, months = 0, days = 0, hours = 0, minutes = 0, seconds = 0, milliseconds = 0, microseconds = 0):
        self._Years = years
        self._Months = months
        self._Days = days
        self._Hours = hours
        self._Minutes = minutes
        self._Seconds = seconds
        self._Microseconds = microseconds
        self._Milliseconds = milliseconds

# ============================================= Objects ==============================================
    def DifferenceTime(self):
        return 0 

    # Year
    def setYear(self,year):
        self._Years = year

    def getYear(self):
        return self._Years
    
    # Month
    def setMonth(self,Month):
        self._Months = Month

    def getYear(self):
        return self._Months

    # Day
    def setDay(self,Day):
        self._Days = Day

    def getDay(self):
        return self._Days
        
    # Hour
    def setHour(self,Hour):
        self._Hours = Hour

    def getHour(self):
        return self._Hours
    

    # Minute
    def setMinute(self,Minute):
        self._Minutes = Minute

    def getMinute(self):
        return self._Minutes

    # Second
    def setSecond(self,Second):
        self._Seconds = Second

    def getSecond(self):
        return self._Seconds


    # Microseconds
    def setMicrosecond(self,MicroSecond):
        self._Microseconds = MicroSecond

    def getSecond(self):
        return self._Seconds

    # Millisecond
    def setSecond(self,Second):
        self._Seconds = Second

    def getSecond(self):
        return self._Seconds

    def getNextMonday(self):
        'Gets the next Monday'
        today = datetime.date.today()
        days=-today.weekday()
        next_monday = today + datetime.timedelta(days=days+7)
        monDateTime =  datetime.date(next_monday.year,next_monday.month,next_monday.day)
        diff = monDateTime - today
        self.setDay(diff.days)

    def getTime(self):
        'Adds the delta time to the current time '
        startTime = datetime.datetime.now().replace(microsecond=0)
        if self.RetreiveValues('MidnightExecutions'):
            # nowTime = startTime + datetime.timedelta(hours=24) # Might need to uncomment this out in the final Release
            nowTime = startTime.replace(hour=0,minute=0, second=0)

        else:
            nowTime = startTime.replace(second=0)

        DailyTime = nowTime + datetime.timedelta(days=self.getDay(),
                                                    hours=self.getHour(),
                                                    minutes=self.getMinute(), 
                                                    seconds=self.getSecond())
        return DailyTime
    
    def nextTime(self):
        startTime = datetime.datetime.now().replace(microsecond=0)

        DailyTime = startTime + datetime.timedelta(days=self._Days,
                                                    hours=self._Hours,
                                                    minutes=self._Minutes, 
                                                    seconds=self._Seconds,
                                                    milliseconds=self._Milliseconds)
        return DailyTime
        pass

    def setTime(self,HH,MM,SS):
        'Setting the date time'
        dt1 = datetime.datetime.now()
        datenow = datetime.date.today()
        dt2 = datetime.datetime(datenow.year,datenow.month,datenow.day,HH,MM,SS) 
        diff = dt2 - dt1
        print(diff.replace(microsecond=0))
        print(diff.replace(microsecond=0))

    def setDateTime(self,YY,mm,DD,HH,MM,SS):
        'Setting the date time'
        dt1 = datetime.datetime.now()
        datenow = datetime.date.today()
        dt2 = datetime.datetime(YY,mm,DD,HH,MM,SS) 
        diff = dt2 - dt1
        print(diff.replace(microsecond=0))
        print(diff.replace(microsecond=0))

    def printDateTime(self):
        'Prints the the objects that is set in the difference'
        stringList = []
        if self._Years != 0:
            stringList.append(f"Year: {self._Years}")
        if self._Months != 0:
            stringList.append(f"Month: {self._Months}")
        if self._Days != 0:
            stringList.append(f"Days: {self._Days}")
        if self._Hours != 0:
            stringList.append(f"Hours: {self._Hours}")
        if self._Minutes != 0:
            stringList.append(f"Minutes: {self._Minutes}")
        if self._Seconds != 0:
            stringList.append(f"Seconds: {self._Seconds}")
        if self._Microseconds != 0:
            stringList.append(f"Microseconds: {self._Microseconds}")
        if self._Milliseconds != 0:
            stringList.append(f"Milliseconds: {self._Milliseconds}")
        return ' '.join(stringList)