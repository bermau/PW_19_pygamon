# Une fonction random rapide.
import random

SEED = 2
random.seed(SEED)
SIZE = 1024

proba_table = [random.random() for _ in range(SIZE)]
index = 0

def random():
    """return a random number between 0 and 1"""
    global index
    index = (index + 1) % SIZE
    return proba_table[index]


def randint(low, high):
    """return an integer between low and high"""
    global index
    index = (index + 1) % SIZE
    return low + int((high - low + 1) * random())


if __name__ == '__main__':
    for i in range(3):
        print(random())
    for i in range(3):
        print(randint(4, 6))
