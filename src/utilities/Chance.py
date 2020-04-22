import random


def get_random(chance):
    return random.random() < chance


if __name__ == '__main__':
    get_random(5)

