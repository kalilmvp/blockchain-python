# 1 - Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
persons = [
    {
        'name': 'Max', 
        'age': 31,
        'hobbies': ['play something', 'read', 'football']
    },
    {
        'name': 'Kalil', 
        'age': 4,
        'hobbies': ['volley', 'read', 'football']
    },
    {
        'name': 'Lucas', 
        'age': 23,
        'hobbies': ['play something really cool', 'read', 'date']
    },
    {
        'name': 'Mariana', 
        'age': 10,
        'hobbies': ['video game', 'read', 'cinema']
    }
]

print(persons)
print('-' * 20)
# 2 - Use a list comprehension to convert this list of persons into a list of names (of the persons).
print([person['name'] for person in persons])
print('-' * 20)
# 3 - Use a list comprehension to check whether all persons are older than 20.
print(all([person['age'] > 20 for person in persons]))
print('-' * 20)
# 4 - Copy the person list such that you can safely edit the name of the first person (without changing the original list).
copied_persons = [person.copy() for person in persons]
copied_persons[0]['name'] = 'Max Other Copied'

print(copied_persons)
print('&' * 20)
print(persons)
print('-' * 20)
# 5 - Unpack the persons of the original list into different variables and output these variables.
pe1, pe2, pe3, pe4 = persons
print(pe1)
print(pe2)
print(pe3)
print(pe4)