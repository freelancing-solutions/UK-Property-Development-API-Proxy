import os, random, string, time


def is_development() -> bool:
    try:
        if os.environ['SERVER_SOFTWARE'].lower().startswith('development'):
            return True
        return False
    except Exception as e:
        return False


def create_id(size: int = 64, chars: str = string.ascii_lowercase + string.digits) -> str:
    return ''.join(random.choice(chars) for x in range(size))


def timestamp() -> int:
    return int(float(time.time()) * 1000)


def timestamp_difference(stamp1, stamp2) -> int:
    return int(stamp1 - stamp2)
