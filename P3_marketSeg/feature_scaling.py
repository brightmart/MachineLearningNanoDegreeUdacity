""" quiz materials for feature scaling clustering """

### FYI, the most straightforward implementation might 
### throw a divide-by-zero error, if the min and max
### values are the same
### but think about this for a second--that means that every
### data point has the same value for that feature!  
### why would you rescale it?  Or even use it at all?
def featureScaling(arr):
    import numpy
    #solution 1
    maxx=numpy.max(arr)
    minn=numpy.min(arr)
    arr2=[]
    for x in range(len(arr)):
        newValue=(numpy.float(arr[x])-minn)/(maxx-minn)
        arr2.append(newValue)
    
    #solution 2.
    from sklearn.preprocessing import MinMaxScaler
    weight=numpy.array(arr)
    scaler=MinMaxScaler()
    arr2=scaler.fit_transform(weight)
    return  arr2

# tests of your feature scaler--line below is input data
data = [115, 140, 175]
print featureScaling(data)

