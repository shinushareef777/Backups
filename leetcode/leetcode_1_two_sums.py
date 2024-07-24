from typing import List

def twoSums(nums: List[int], target: int) -> List[int]:
  """
    return indices such that it adds up to target
  """
  d = {} # dict to store indices

  for i, val in enumerate(nums):
    diff = target - val
    if diff in d:
      return [d[diff], i]
    d[val] = i


if __name__ == "__main__":
  print(twoSums([2, 7, 11, 15], 11))