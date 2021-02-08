def genNums():
    nums = []
    for i in range(20):
        nums.append(random.randint(1,100))
    return nums

def insertionSort(nums):
    comps = 0 
    for i in range(1, len(nums)):
        current = nums[i]
        position = i
        while position > 0 and nums[position-1] > current:
            nums[position] = nums[position-1]
            position -= 1
            comps += 1
        nums[position] = current
    return nums , comps

def selectionSort():
    for i in range(len(alist)):

        #Find the minimum element in remaining
        minPosition = i

        for j in range(i+1, len(alist)):
            if alist[minPosition] > alist[j]:
                minPosition = j
                    
        # Swap the found minimum element with minPosition       
        temp = alist[i]
        alist[i] = alist[minPosition]
        alist[minPosition] = temp

def bubbleSort(nums):
    passes = 0
    comps = 0
    swap = True
    while swap:
        swap = False
        for i in range(len(nums)-1-passes):
            if nums[i] > nums[i+1]:
                temp = nums[i]
                nums[i] = nums[i+1]
                nums[i+1] = temp
                swap = True
            comps += 1
        passes += 1
    return nums, comps

# Merges two subarrays of arr[]. 
# First subarray is arr[l..m] 
# Second subarray is arr[m+1..r] 
def merge(arr, l, m, r): 
    n1 = m - l + 1
    n2 = r - m 
  
    # create temp arrays 
    L = [0] * (n1) 
    R = [0] * (n2) 
  
    # Copy data to temp arrays L[] and R[] 
    for i in range(0 , n1): 
        L[i] = arr[l + i] 
  
    for j in range(0 , n2): 
        R[j] = arr[m + 1 + j] 
  
    # Merge the temp arrays back into arr[l..r] 
    i = 0     # Initial index of first subarray 
    j = 0     # Initial index of second subarray 
    k = l     # Initial index of merged subarray 
  
    while i < n1 and j < n2 : 
        if L[i] <= R[j]: 
            arr[k] = L[i] 
            i += 1
        else: 
            arr[k] = R[j] 
            j += 1
        k += 1
  
    # Copy the remaining elements of L[], if there 
    # are any 
    while i < n1: 
        arr[k] = L[i] 
        i += 1
        k += 1
  
    # Copy the remaining elements of R[], if there 
    # are any 
    while j < n2: 
        arr[k] = R[j] 
        j += 1
        k += 1
  
# l is for left index and r is right index of the 
# sub-array of arr to be sorted 
def mergeSort(arr,l,r): 
    if l < r: 
  
        # Same as (l+r)/2, but avoids overflow for 
        # large l and h 
        m = (l+(r-1))/2
  
        # Sort first and second halves 
        mergeSort(arr, l, m) 
        mergeSort(arr, m+1, r) 
        merge(arr, l, m, r) 
  
  
# Driver code to test above 
arr = [12, 11, 13, 5, 6, 7] 
n = len(arr) 
print ("Given array is") 
for i in range(n): 
    print ("%d" %arr[i]), 
  
mergeSort(arr,0,n-1) 
print ("\n\nSorted array is") 
for i in range(n): 
    print ("%d" %arr[i]), 
