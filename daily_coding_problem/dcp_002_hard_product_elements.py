'''
Given an array of integers, return a new array such that each element at index i of the new array 
is the product of all the numbers in the original array except the one at i.

For example, if our input was [1, 2, 3, 4, 5], the expected output would be [120, 60, 40, 30, 24]. 
If our input was [3, 2, 1], the expected output would be [2, 3, 6].

Follow-up: what if you can't use division?

Asked by: Uber
'''


def solve_original(inp):
   # Original solution with complexity O(2*n)
   m = 1
   for i in range(len(inp)):
      m *= inp[i]
      
   r = []
   for i in range(len(inp)):
      r.append(int(m / inp[i]))
   
   return r


def solve_follow_up(inp):
   # Follow-up solution with complexity O(n^2)
   r = [1] * len(inp)
   for i in range(len(inp)):
      for j in range(len(inp)):
         if i != j:
            r[j] *= inp[i]
   
   return r

# Input
a = [1, 2, 3, 4, 5]

solve_original(a)

solve_follow_up(a)
