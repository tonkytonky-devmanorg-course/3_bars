import json
import math
import sys
from functools import partial


def main():
    bars_json = load_json('bars.json')

    try:
        if sys.argv[1] == '-b':
            print(format_bar_output(get_biggest_bar(bars_json), 'Самый большой бар'))
        elif sys.argv[1] == '-s':
            print(format_bar_output(get_smallest_bar(bars_json), 'Самый маленький бар'))
        elif sys.argv[1] == '-c':
            longitude, latitude = float(sys.argv[2]), float(sys.argv[3])
            print(format_bar_output(get_closest_bar(bars_json, longitude, latitude), 'Самый близкий бар'))
        else:
            print_usage_tip()
    except (IndexError, ValueError):
        print_usage_tip()


def print_usage_tip():
    print(
        'Please, call the script with one of the following arguments:\n'
        '-b - to know the biggest bar\n'
        '-s - to know the smallest bar\n'
        '-c <your longitude> <your latitude> - to know the closest bar. '
        'Input longitude and latitude as a float point numbers.'
    )


def load_json(filepath):
    with open(filepath, encoding='windows-1251') as file_handler:
        return json.load(file_handler)


def get_biggest_bar(bars_json):
    return max(bars_json, key=lambda bar: bar['SeatsCount'])


def get_smallest_bar(bars_json):
    return min(bars_json, key=lambda bar: bar['SeatsCount'])


def get_closest_bar(bars_json, longitude, latitude):
    get_distance_to_bar_partial = partial(get_distance_to_bar, longitude=longitude, latitude=latitude)
    return min(bars_json, key=get_distance_to_bar_partial)


def get_distance_to_bar(bar, longitude, latitude):
    bar_longitude, bar_latitude = bar['geoData']['coordinates'][0], bar['geoData']['coordinates'][1]
    return math.sqrt((longitude - bar_longitude) ** 2 + (latitude - bar_latitude) ** 2)


def format_bar_output(bar, label):
    return '{}: {} ({})'.format(label, bar['Name'], bar['Address'])


if __name__ == '__main__':
    main()
