def Parametres(shareFetureData):
    # the data set which is passed in the function is the one we choose after selecting
    # the feature, when we do this 'nsdataHCImr = nsdataHCI['MonthReturn']'
    # https://www.youtube.com/watch?v=bqvZL8Ww3aA have used this video as a basis
    # for selecting the best pdq values
    # this function spits out only one value each but in our program we will
    # give a range to the user eg. 'p-values range (3-5)' some shit like that
    # you will need these libraries: 
    #  from statsmodels.tsa.stattools import pacf
    #  from statsmodels.tsa.stattools import acf
    
    pVal=0
    dVal=0 # should not be more then 2
    qVal=0
    count1 = 0
    count2 = 0
    check = 0
    acfArray = acf(data, nlags=30)
    pacfArray = pacf(data, nlags=30)
    
    for i in range(0,30) :
        if acfArray[i]>=0.24 and acfArray[i]<=0.25:
            count = i+1
            print(acfArray[count-1])
            pVal = count
        
    while check !=-1:
        for i in range(0,30):
            if pacfArray[i]<0:
                count2 = i
                check =-1
                qVal = count2
                break
        
    values=[pVal,dVal,qVal]
    
    
    return values