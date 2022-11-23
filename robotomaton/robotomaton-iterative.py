def iter(previous, sprocket):
    cache = [-1] * len(sprocket)
    total = [-1] * len(sprocket)

    cache[0] = sprocket[0]
    total[0] = sprocket[0]

    for i in range(1, len(sprocket)):
        if previous[i] == 0:
            cache[i] = sprocket[i]

        elif previous[i] == i:
            cache[i] = sprocket[i] + total[i - 1]

        else:
            cache[i] = sprocket[i] + total[i - 1] - total[i - previous[i] - 1]

        total[i] = cache[i] + total[i - 1]

    return cache[-1]

def iter_better(previous, sprocket):
    cache = [0] * len(sprocket)
    total = sprocket[0]
    cache[0] = sprocket[0]

    for i in range(1, len(sprocket)):
        total = sprocket[i]

        if previous[i] == i:
            total += cache[i - 1]
        else:
            total += cache[i-1] - cache[i - 1 - previous[i]]
        cache[i] = cache[i - 1] + total

    return total


if __name__ == "__main__":
    previous = [0,1,1,3]
    sprockets = [3,2,10,7]

    print(iter(previous, sprockets) == iter_better(previous, sprockets))