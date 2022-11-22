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

if __name__ == "__main__":
    previous = [0,1,1,3]
    sprockets = [3,2,10,7]

    print(iter(previous, sprockets))