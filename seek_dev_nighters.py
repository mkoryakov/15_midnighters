import requests
import pytz
from datetime import datetime, time


MIDNIGHT = time(0, 0, 0)
MORNING = time(6, 0, 0)


def load_attempts():
    devman_url = 'https://devman.org/api/challenges/solution_attempts'
    payload = {'page': 1}
    devman_data = requests.get(devman_url, payload).json()
    pages = devman_data['number_of_pages']
    for page in range(1, pages + 1):
        payload = {'page': page}
        devman_data = requests.get(devman_url, payload).json()
        yield from devman_data['records']


def get_midnighters():
    midnighters = set()
    for user_data in load_attempts():
        if not user_data['timestamp']:
            continue
        time_zone = pytz.timezone(user_data['timezone'])
        utc_datetime = datetime.utcfromtimestamp(user_data['timestamp'])
        localize_utc_datetime = pytz.utc.localize(utc_datetime)
        commit_time = localize_utc_datetime.astimezone(time_zone).time()
        if MIDNIGHT < commit_time < MORNING:
            midnighters.add(user_data['username'])
    return midnighters


def print_midnighters(midnighters):
    print('В ночное время сдавали задачи %d человек:' % len(midnighters))
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    midnighters = get_midnighters()
    print_midnighters(midnighters)
