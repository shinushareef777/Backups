import random


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


arr = [random.randint(0, 10000) for _ in range(50)]


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
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
    parenthesis = {")": "(", "}": "{", "]": "["}
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
    if num < 0:
        return False

    div = 1

    while num >= 10 * div:
        div *= 10

    while num:
        if num % 10 != num // div:
            return False

        num = (num % div) // 10
        div //= 100

    return True


def fibonacci(n):
    if n <= 1:
        return n

    a, b = 0, 1

    for i in range(2, n + 1):
        a, b = b, a + b

    return b


def cipher_wheel(txt, shift):
    decoded_msg = []
    for char in txt:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            msg = chr((ord(char) - start - shift) % 26 + start)
            decoded_msg.append(msg)
        else:
            decoded_msg.append(char)
    return "".join(decoded_msg)

def get_min_moves(s, i):
    if i > len(s) - 1 or i < 0: return 0
    char = s[i] 
    l, r = i - 1, i + 1
    print(s)

    while l >= 0:
        if s[l] == char:
            s = s[:l] + s[l+1:]
            break
        l -= 1

    while r < len(s):
        if s[r] == char:
            s = s[:r] + s[r + 1 :]
            break
        r += 1

    num_moves = (i-l) + (r - i - 1)
    return num_moves


def validParenthesis(s):
    close_open = {")": "(", "]":"[", "}":"{"}
    stack = []

    for i in s:
        if i in close_open:
            if stack and stack[-1] == close_open[i]:
                stack.pop()
            else:
                return False
        else:
            stack.append(i)
    
    return len(stack) == 0


def countOneBits(n):
    res = 0
    while n:
        res += 1
        n = n & (n-1)

    return res

def singleNumber(nums):
    res = 0
    for n in nums:
        res = n ^ res
    return res

def reverseBits(n):
    res = 0
    for _ in range(32):
        res = res << 1
        res = res | (n&1)
        n = n >> 1
    return res

def sumOfTwoNumbers(a, b):
    for _ in range(32):
        a, b = a ^ b, (a&b) << 1
        if not b:
            break
    return a


def print_char():
    char = "a10b2c5d11"
    l, r = 0, 1

    char_count = ""
    while r < len(char):
        if ord(char[r]) in range(ord('0'), ord('9') + 1):
            char_count += char[r]
        else:
            if char_count:
                print(char[l] * int(char_count))
            l = r
            char_count = ""
        r += 1
        if char_count and r == len(char):
            print(char[l] * int(char_count))


def coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)

    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a-c])

    return dp[amount] if dp[amount] != amount + 1 else -1


def ways_coin(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1

    for a in range(1, amount+1):
        for c in coins:
            if a - c >= 0:
                dp[a] = dp[a] +  dp[a-c]
    # print(dp)
    return dp[amount]

def second_largest(arr):

    largest = second = float("-inf")

    for n in arr:
        if n > largest:
            second, largest = largest, n
        elif largest > n > second:
            second = n

    return second


# give an example for dynamic programming

# print(coin_change([1, 2, 5], 11))

# create a function that read from two txt files and write content to another file   using append

def merge_files(file1, file2, outfile):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(outfile, 'w') as out:
        out.write(f1.read() + f2.read())

# create a function that uses the 3d dynamic programming approach


def alternatCount():
    ip = "aaabbbaabbcdeeeeeeeee"

    l, r = 0, 1

    char_count = 1
    res = ""

    while l <= r and r < len(ip):
        if ip[l] == ip[r]:
            char_count += 1
        else:
            res += str(char_count) + ip[l]
            char_count = 1
        if r == len(ip) - 1:
            res += str(char_count) + ip[r]
        l += 1
        r += 1

    return res


# print(ways_coin([1, 4, 5], 5))
print(alternatCount())

x = {'a': 3, 'b':2, 'c':1, 'd':4}
print(dict(sorted(x.items(), key=lambda x: x[1])))