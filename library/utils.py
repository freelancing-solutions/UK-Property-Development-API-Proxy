import os, random, string, time


def is_development():
    if os.environ['SERVER_SOFTWARE'].lower().startswith('development'):
        return True
    return False


def create_id(size=64, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def timestamp():
    return int(float(time.time()) * 1000)


def timestamp_difference(stamp1, stamp2):
    return int(stamp1 - stamp2)