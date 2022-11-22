def robotomaton(num, cache, previous, sprockets):
    if cache[num] != -1:
        return cache[num]

    if previous[num] == 0:
        return sprockets[num]
    
    cost = sprockets[num]
    for i in range(num - 1, num - previous[num] - 1, -1):
        cost += robotomaton(i, cache, previous, sprockets)

    cache[num] = cost
    return cache[num]

if __name__ == "__main__":
    previous = [0,1,1,3]
    sprockets = [3,2,10,7]
    cache = [-1] * len(previous)
    print(robotomaton(3, cache, previous, sprockets))
    print(cache)