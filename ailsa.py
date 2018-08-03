def find_field(list, value):
    try:
        return list.index(value)
    except ValueError as identifier:
        return -1
    
    # index = 0
    # for e in list:
    #     #print(e)
    #     if e == value:
    #         return index
    #     index += 1
    # return -1



print(find_field([1,2,3], 3))
print(find_field(['alpha', 'beta'], 'gamma'))
print(find_field([10,5,7,432,1], 10))