def print_name_and_age():
    name = input("Name: ")
    age = input("Age ")

    print(name + ' ' + age)


def print_any_data(data1, data2): 
    print(repr(data1) + repr(data2))


def print_decades_lived(age):
    print(age//10)

#print_name_and_age()
#print_any_data(45, 'teste')
print_decades_lived(31)