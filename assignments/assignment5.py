# 1 - Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.
import random as r
import datetime as datet

# between 0 and 1
print(r.random())

#between 1 and 10
print(r.randint(1, 10))

# 2 - Use the datetime library together with the random number to generate a random, unique value.
print(datet.date(r.randint(1990, 2018), r.randint(1, 12), r.randint(1, 31)))

print('{:.2f} generated at the time {}'.format(r.uniform(1, 999), datet.datetime.now()))