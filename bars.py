import argparse
import json
import math
from functools import partial


def _main():
    parser = argparse.ArgumentParser()
    args = get_args(parser)
    bars_json = load_json(args.filename)

    if args.mode == 'b':
        print(format_bar_output(get_biggest_bar(bars_json), 'Самый большой бар'))
    elif args.mode == 's':
        print(format_bar_output(get_smallest_bar(bars_json), 'Самый маленький бар'))
    elif args.mode == 'c':
        if not all((args.lon, args.lat)):
            parser.error("for `c` option --lon and --lat values are required")

        longitude, latitude = float(args.lon), float(args.lat)
        print(format_bar_output(get_closest_bar(bars_json, longitude, latitude), 'Самый близкий бар'))


def get_args(parser):
    parser.add_argument('filename', help='Path to JSON file from https://data.mos.ru/opendata/7710881420-bary')
    parser.add_argument(
        'mode', choices=['b', 's', 'c'],
        help='Choose the bar you want to find: `b` for biggest, `s` for smallest, `c` for closest '
             '(--lon and --lat values are required).'
    )
    parser.add_argument('--lon', help='Current longitude (float point number)', type=float, default=None)
    parser.add_argument('--lat', help='Current latitude (float point number)', type=float, default=None)

    return parser.parse_args()


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
    _main()
