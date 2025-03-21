def maj_element(nums: list[int]) -> int:
    counts = {}
    for num in nums:
        if num not in counts:
            counts[num] = 0
        counts[num] += 1
    
    n = len(nums)
    for num, count in counts.items():
        if count >= n // 2:
            return num
