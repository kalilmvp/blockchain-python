# 1) Create a list of names and use a for loop to output the length of each name (len() ).
names = ['Kalil', 'Andreia', 'Ailsa', 'Leonardo']

for name in names:
    print(len(name))

print('*' * 20)
# 2) Add an if  check inside the loop to only output names longer than 5 characters.
for name in names:
    if len(name) > 5:
        print(name)

print('*' * 20)
# 3) Add another if  check to see whether a name includes a “n”  or “N”  character.
for name in names:
    if 'n' in name or 'N' in name:
        print(name)

print('*' * 20)
# 4) Use a while  loop to empty the list of names (via pop() )
contain_names = True
while len(names) >= 1:
    names.pop()

    if len(names) == 0:
        contain_names = False
else:
    print('Names empty')