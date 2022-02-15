import random
import string


def get_random_text(length=8):
    randomList = string.ascii_lowercase + string.digits
    result = ""
    for i in range(length):
        result += random.choice(randomList)

    return result
