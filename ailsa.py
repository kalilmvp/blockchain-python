import datetime

# Given your birthday and the current date, calculate your age 
# in days. Compensate for leap years. Assume that the birthday 
# and current date are correct dates (and no time travel). 
# Simply put, if you were born 1 Jan 2012 and todays date is 
# 2 Jan 2012 you are 1 day old.

# IMPORTANT: You don't need to solve the problem yet! 
# Just brainstorm ways you might approach it!

daysOfMonths = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def isLeapYear(year):
    # if (year is not divisible by 4) then (it is a common year)
    # else if (year is not divisible by 100) then (it is a leap year)
    # else if (year is not divisible by 400) then (it is a common year)
    # else (it is a leap year)
    if year % 400 is 0 or year % 100 is 0 or year % 4 is 0:
        return True
    return False

    ##
    # Your code here. Return True or False
    # Pseudo code for this algorithm is found at
    # http://en.wikipedia.org/wiki/Leap_year#Algorithm
    ##

def daysBetweenDates(y1, m1, d1, y2, m2, d2):
    # ano de nascimento maior que ano atual
    if y1 > y2:
        print('No time travel')
        return None

    print(isLeapYear(y1))
    print(isLeapYear(y2))

    birth_date = datetime.datetime(year=y1, month=m1, day=d1)
    today = datetime.datetime(year=y2, month=m2, day=d2)

    print(birth_date)
    print(today)

    days = (today - birth_date).days
    
    return days

days_age = daysBetweenDates(1986, 10, 25, 2018, 8, 3);
years = int(days_age / 365)

print('Days between total: {}'.format(days_age))
print('Years: {}'.format(years))