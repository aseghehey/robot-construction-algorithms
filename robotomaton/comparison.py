import random
# t1
# sprocket = [3, 11, 31, 29, 5]
# previous = [0, 0, 1, 2, 4]

#t2
# previous = [0,0,1,0,4]
# sprocket = [3,11,31,29,5]

#t3
# previous = [0, 1, 1, 3]
# sprocket = [3,2,10,7]

#t4
sprocket = [random.randrange(200)]
previous = [0]

for i in range(1,random.randrange(200)):
    sprocket.append(random.randrange(200))
    previous.append(random.randrange(i))


# print(len(sprocket) == len(previous))
# print(previous)

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


cache = [-1] * len(sprocket)
iter_var = iter(previous, sprocket)
memo = robotomaton(len(sprocket) - 1, cache, previous, sprocket)
print('result: \niter ', iter_var,'\nmemo ' ,memo)
print('Equal: ', memo == iter_var)

