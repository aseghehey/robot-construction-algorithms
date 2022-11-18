# Emanuel Aseghehey
from collections import defaultdict

def readInput(filename):
    f_in = open(filename, 'r')

    clean_input = []
    for line in f_in.readlines():
        cur_line = line.replace('\n','').split(' ')
        tmp = []
        for x in cur_line:
            if x.isalpha(): # skipping the 'omnidroid' line since this program is only for omnidroid anyways
                continue
            tmp.append(int(x))
        clean_input.append(tmp)

    clean_input.pop(0) # for now cause we can ignore it since we know what it means
    # print(clean_input)
    n, m = clean_input[0]

    dep = {num: [] for num in range(n)}

    for i in range(1, m + 1):
        need, needfor = clean_input[i]
        dep[needfor].append(need)

    sprockets = []
    for i in range(m + 1, len(clean_input)):
        sprockets.append(clean_input[i][0])
    
    # print(dep, sprockets)

    return dep, sprockets
    
def omnidroid(num, cache, use, sprockets):
    if num in cache: # memoization
        return cache[num]
    
    if use[num] == []:
        return sprockets[num]
    
    added_use = 0
    for t in use[num]:
        added_use += omnidroid(t, cache, use, sprockets)
    
    cache[num] = sprockets[num] + added_use
    return cache[num]

if __name__ == "__main__":

    uset1, sprocketst1 = readInput('input.txt')
    uset2, sprocketst2 = readInput('small-omni-input.txt')

    print(omnidroid(len(sprocketst1) - 1, {}, uset1, sprocketst1))
    print(omnidroid(len(sprocketst2) - 1, {}, uset2, sprocketst2))
    