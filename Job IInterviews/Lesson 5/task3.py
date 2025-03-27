def last_stone(stones):
    stones.sort()
    while len(stones) > 1:
        x = stones[-2]
        y = stones[-1]
        stones = stones[:-2]
        if x == y:
            continue
        else:
            stones.append(y - x)
            stones.sort()
    if len(stones) == 0:
        return 0
    else:
        return stones[0]
