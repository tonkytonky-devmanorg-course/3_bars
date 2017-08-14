import json
import math
import sys


def main():
    bars_json = load_json('bars.json')

    try:
        if sys.argv[1] == '-b':
            print(get_biggest_bar(bars_json))
        elif sys.argv[1] == '-s':
            print(get_smallest_bar(bars_json))
        elif sys.argv[1] == '-c':
            longitude, latitude = float(sys.argv[2]), float(sys.argv[3])
            print(get_closest_bar(bars_json, longitude, latitude))
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
    with open(filepath, encoding='windows-1251') as input_file:
        return json.load(input_file)


def get_biggest_bar(bars_json):
    biggest_bar = max(bars_json, key=lambda bar: bar['SeatsCount'])
    return 'Самый большой бар: {} ({})'.format(biggest_bar['Name'], biggest_bar['Address'])


def get_smallest_bar(bars_json):
    smallest_bar = min(bars_json, key=lambda bar: bar['SeatsCount'])
    return 'Самый маленький бар: {} ({})'.format(smallest_bar['Name'], smallest_bar['Address'])


def get_closest_bar(bars_json, longitude, latitude):
    def get_distanse_to_bar(bar):
        bar_longitude, bar_latitude = bar['geoData']['coordinates'][0], bar['geoData']['coordinates'][1]
        return math.sqrt((longitude - bar_longitude) ** 2 + (latitude - bar_latitude) ** 2)

    closest_bar = min(bars_json, key=get_distanse_to_bar)
    return 'Самый близкий бар: {} ({})'.format(closest_bar['Name'], closest_bar['Address'])


if __name__ == '__main__':
    main()
