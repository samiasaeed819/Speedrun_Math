## CODE - Sorting Algorithms ##
##Let the war BEGIN##

#Numpy
import numpy as np
import time

start_time = time.time()
one_array = np.random.randint(0, 100000, size=100000)
one_array = list(one_array)
end_time = time.time()

print(f"Time taken: {end_time - start_time} seconds")

# BEGIN THE SORTING
# Bubble Sort
def bubbleSort(my_array):
    n=len(my_array)
    for i in range(n-1):
        for j in range(n-i-1):
            if my_array[j] > my_array[j+1]:
                my_array[j], my_array[j+1] = my_array[j+1], my_array[j]
    return my_array
start = time.time()
bubbleSort(one_array)
end = time.time()
print(end-start)

#Selection Sort
def selection_sort(my_array):
    n = len(my_array)
    for i in range(n-1):
        min_index = i
        for j in range(i+1,n):
            if my_array[j] < my_array[min_index]:
                min_index = j
        min_value = my_array.pop(min_index)
        my_array.insert(i,min_value)
    return my_array
start = time.time()
selection_sort(one_array)
end = time.time()
print(end-start)


#Insertion Sort
def insertion_sort(my_array):
    n = len(my_array)
    for i in range(1,n):
        insert_index = i
        current_value = my_array.pop(i)
        for j in range(i-1, -1, -1):
            if my_array[j] > current_value:
                insert_index = j
        my_array.insert(insert_index, current_value)
start = time.time()
insertion_sort(one_array)
end = time.time()
print(end-start)

#Quick Sort
def quick_sort(arr):
    if len(arr) <=1:
        return arr
    p = arr[-1]
    left = [
        x for x in arr[:-1] if x <= p
        ]
    right = [
        x for x in arr[:-1] if x > p
        ]

    left = quick_sort(left)
    right = quick_sort(right)

    return left + [p] + right

start = time.time()
quick_sort(one_array)
end = time.time()
print(end-start)

#Merge Sort
def merge_sort(arr):
  n = len(arr)
  
  if n == 1:
    return arr
  m = len(arr) // 2
  L = arr[:m]
  R = arr[m:]
  L = merge_sort(L)
  R = merge_sort(R)
  l, r = 0, 0
  L_len = len(L)
  R_len = len(R)

  sorted_arr = [0] * n
  i = 0
  while l < L_len and r < R_len:
    if L[l] < R[r]:
      sorted_arr[i] = L[l]
      l += 1
    else:
      sorted_arr[i] = R[r]
      r += 1

    i += 1
  while l < L_len:
    sorted_arr[i] = L[l]
    l += 1
    i += 1

  while r < R_len:
    sorted_arr[i] = R[r]
    r += 1
    i += 1
  return sorted_arr

start = time.time()
merge_sort(one_array)
end = time.time()
print(end-start)


#Counting Sort
def counting_sort(arr):
    n =len(arr)
    maxx = max(arr)
    counts = [0] * (maxx +1)

    for x in arr:
        counts[x] += 1
    
    i = 0
    for c in range(maxx+1):
        while counts[c] > 0:
            arr[i] = c
            i+=1
            counts[c] -=1

start = time.time()
counting_sort(one_array)
end = time.time()
print(end-start)
