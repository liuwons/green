import random

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def randid(length):
    result = ''
    for i in range(length):
        idx = random.randint(0, len(alphabet)-1)
        result += alphabet[idx]