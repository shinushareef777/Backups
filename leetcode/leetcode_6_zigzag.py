import time

def perf(func):
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        speed = time.perf_counter() - t0
        print(f"{func.__name__} took {speed:0.8f}s to complete")
        return result
    return wrapper

@perf
def convert(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s

    res = [""] * numRows
    index, step = 0, 1

    for char in s:
        res[index] += char
        if index == 0:
            step = 1
        elif index == numRows - 1:
            step = -1
        index += step
    return "".join(res)

@perf
def another(s, numRows):
    if numRows == 1:
        return s
    
    res = ""
    for r in range(numRows):
        increment = (numRows - 1) * 2 #6

        for i in range(r, len(s), increment):
            res += s[i]
            j = i + increment - 2 * r # current index + increment - 2 * current row (if second row)
            if (r > 0 and r < numRows - 1 and j < len(s)):
                res += s[j]
    return res


            


if __name__ == "__main__":
    another("PAYPALISHIRING", 4)
    convert("PAYPALISHIRING", 4)
