import argparse
import json
import math
from functools import partial


def _main():
    parser = argparse.ArgumentParser()
    args = get_args(parser)

    longitude, latitude = args.lon, args.lat
    bars = load_json(args.filename)
    if not bars:
        parser.error(
            'file with bars not found, '
            'specify existing path in `filename` argument'
        )

    print(format_bar_output(get_biggest_bar(bars), 'Самый большой бар'))
    print(format_bar_output(get_smallest_bar(bars), 'Самый маленький бар'))
    print(format_bar_output(get_closest_bar(
        bars, longitude, latitude), 'Самый близкий бар'))


def get_args(parser):
    parser.add_argument(
        'filename',
        help='Path to JSON file from'
             'https://data.mos.ru/opendata/7710881420-bary'
    )
    parser.add_argument(
        '--lat', help='Current latitude (float point number)',
        type=float, required=True, metavar='latitude'
    )
    parser.add_argument(
        '--lon', help='Current longitude (float point number)',
        type=float, required=True, metavar='longitude'
    )

    return parser.parse_args()


def load_json(filepath):
    try:
        with open(filepath, encoding='windows-1251') as file_handler:
            return json.load(file_handler)
    except FileNotFoundError:
        return None


def get_biggest_bar(bars):
    return max(bars, key=lambda bar: bar['SeatsCount'])


def get_smallest_bar(bars):
    return min(bars, key=lambda bar: bar['SeatsCount'])


def get_closest_bar(bars, longitude, latitude):
    get_distance_to_bar_partial = partial(
        get_distance_to_bar, longitude=longitude, latitude=latitude)
    return min(bars, key=get_distance_to_bar_partial)


def get_distance_to_bar(bar, longitude, latitude):
    bar_longitude = bar['geoData']['coordinates'][0]
    bar_latitude = bar['geoData']['coordinates'][1]
    return math.sqrt(
        (longitude - bar_longitude) ** 2 + (latitude - bar_latitude) ** 2)


def format_bar_output(bar, label):
    return '{}: {} ({})'.format(label, bar['Name'], bar['Address'])


if __name__ == '__main__':
    _main()
