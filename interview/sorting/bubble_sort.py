import random

def bubble_sort(arr):
  n = len(arr)
  for i in range(n):
    for j in range(n-1):
      if arr[j] > arr[j+1]:
        arr[j], arr[j+1] = arr[j+1], arr[j]

  return arr

arr = [random.randint(0, 10000) for _ in range(50)]


def merge_sort(arr):
  if len(arr) <= 1:
    return arr
  
  mid = len(arr)//2
  left = arr[:mid]
  right = arr[mid:]

  def merge(left, right):
    l = 0
    r = 0
    result = []
    while l < len(left) and r < len(right):
      if left[l] < right[r]:
        result.append(left[l])
        l += 1
      else:
        result.append(right[r])
        r += 1
    result.extend(left[l:])
    result.extend(right[r:])
    return result
  
  return merge(merge_sort(left), merge_sort(right))
 

# print(merge_sort(arr))


def isValidParenthesis(s):
  parenthesis = {")":"(", "}":"{", "]":"["}
  stack = []

  for i in s:
    if i in parenthesis:
      if stack and stack[-1] == parenthesis[i]:
        stack.pop()
      else:
        return False
    else:
      stack.append(i)

  return not stack


def commonPrefix(arr):
  res = ""
  for i in range(len(arr[0])):
    for j in arr:
      if len(j) == i or j[i] != arr[0][i]:
        return res
    res += arr[0][i]

  return res

def reverse_num(num: int):
  sign = -1 if num < 0 else 1
  reversed_num = 0

  num = abs(num)

  while num != 0:
    # newNum = (num % 10)
    digit = num % 10
    reversed_num = reversed_num * 10 + digit 
    num //= 10

  return sign * reversed_num


def isPalindromeNum(num):
  if num < 0: return False

  div = 1

  while num >= 10 * div:
    div *= 10

  while num:
    if num % 10 != num // div: return False

    num = (num%div) // 10
    div //= 100

  return True


def fibonacci(n):
  if n <= 1: return n

  a, b = 0, 1

  for i in range(2, n+1):
    a, b = b, a + b 

  return b


# print(isPalindromeNum(2332))

print(fibonacci(6))

# print(reverse_num(25977899234))
# arr = ["flower", "floor", "flour"]

# print(commonPrefix(arr))