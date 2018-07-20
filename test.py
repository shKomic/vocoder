import numpy as np

arr = np.array([1,2,3])
arr = np.append(arr, [4])

print(arr)
for i in range(5):
    arr = np.append(arr, [i+5])
    print(arr)


