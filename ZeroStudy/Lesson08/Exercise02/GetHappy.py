import random

def gethappy():
    rand = random.randint(0,4)
    if rand == 0:
        return '爱国福'
    elif rand == 1:
        return '富强福'
    elif rand == 2:
        return '和谐福'
    elif rand == 3:
        return '友善福'
    elif rand == 4:
        return '敬业福'

if __name__ == '__name__':
    gethappy()