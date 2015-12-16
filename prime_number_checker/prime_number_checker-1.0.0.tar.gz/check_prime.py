def primesList(N):
    '''
    N: an integer
    '''
    list1 = [2]
    for ele in range(3, N+1):
        count = 0
        for denom in range(2, ele):
            if ele%denom == 0:
                count += 1
        if count > 0:
            pass
        else:
            list1.append(ele)
    return list1