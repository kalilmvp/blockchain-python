import functools

# 1 -  Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
# def normal_function(function):
#     print(function(10))

# 2 -  Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.
# def normal_function(function):
#     print(function(10))

# normal_function(lambda a: a / 2)

# 3 -  Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.     
# def normal_function2(function, *args):
#     for arg in args:
#         print(function(arg))

#normal_function2(lambda a: a / 2, 10, 15, 20, 22, 35, 40)

# 4 -  Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.
def normal_function2(function, *args):
     for arg in args:
         print('{:^20.2f}'.format(function(arg)))

normal_function2(lambda a: a / 2, 10, 15, 20, 22, 35, 40)