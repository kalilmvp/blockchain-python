with open('filetest.txt', mode='r') as f:


# file.write('manyyy manyyy lines \n')
# file.write('manyyy manyyy lines \n')
# file.write('manyyy manyyy lines \n')
# file.write('manyyy manyyy lines \n')

# file_content = file.readlines()

# for line in file_content:
#     print(line)

    line = f.readline()

    while line:
        print(line)
        line = f.readline()

print('Done')

# file.close()
