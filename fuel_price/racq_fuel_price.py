#!/usr/bin/env python3
import sys
import requests
import json
import numpy as np
from argparse import ArgumentParser
import logging

logging.basicConfig()
log = logging.getLogger(__name__)

# url = 'https://www.racq.com.au/ajaxPages/FuelPricesapi.ashx'

url = 'https://www.racq.com.au/ajaxPages/fuelprice/FuelPricesapi.ashx'

params = dict(
    fueltype='37',  # 91
    lat='-27.5480097',
    lng='153.09129859999996',
    includesurrounding='1'
)

fuel_dict = {
    'E10': "40",
    '91': "37",
    '95': "38",
    '98': "39",
    'Diesel': "1",
    'LPG': "41",
}

def get_list(fueltype, lat, lon):
    params['fueltype'] = fueltype
    params['lat'] = lat 
    params['lng'] = lon 
    log.debug('send requests')
    resp = requests.get(url=url, params=params)
    log.debug('received requests')
    data = resp.json()
    # print(json.dumps(data, indent=4))
    today_list = [ data['Timestamp'].split('.')[0]]
    cnt = 0
    for station in data['Stations']:
        today_list.append(float(station["Price"]))
        if cnt < 10:
            log.info('{} {}'.format(station["Price"], station['Name']))

        cnt += 1

    return today_list

def convert_pricelist_to_string(prices):
    price_string = prices[0] + ', '
    price_string += ', '.join([str(i) for i in prices[1:]])

    return price_string

def convert_statistics_to_string(plist, stats):
    string = plist[0] + ', '
    string += ', '.join([str(i) for i in stats])
    return string


def get_stats(price_list):
    flist = [float(x) for x in price_list[1:]]
    return ( len(flist), np.min(flist), np.max(flist), np.mean(flist), np.std(flist) )

def get_arguments():
    parser = ArgumentParser(description='Get fuel price from RACQ')
    parser.add_argument('fuel_type', type=str, 
        choices=list(fuel_dict.keys()), 
        help='Fuel type')
    parser.add_argument('lat', type=str, help='latitude')
    parser.add_argument('lon', type=str, help='longitude')
    parser.add_argument('-l', '--log', type=str, 
        choices=['INFO', 'DEBUG', "WARNING", "ERROR"],    
        default='ERROR',
        help='Log level, default=ERROR')
    parser.add_argument('-o', '--output', type=str, 
        choices=['stats', 'raw'],    
        default='stats',
        help='Output format: statistics only(default), raw data')
    
    return parser.parse_args(sys.argv[1:])

def set_log_level(log_level):
    if log_level == 'DEBUG':
        logl = logging.DEBUG
    elif log_level == 'INFO':
        logl = logging.INFO
    elif log_level == 'WARNING':
        logl = logging.WARNING
    else:
        logl = logging.ERROR

    log.setLevel(logl)

def main():
    log.debug('started..')
    args = get_arguments()
    
    set_log_level(args.log)

    fuel = fuel_dict[args.fuel_type]
    plist = get_list(fuel, args.lat, args.lon)
    if args.output == 'raw':
        pstr = convert_pricelist_to_string(plist)
        print(pstr)
    else:
        stats = get_stats(plist)
        sstr = convert_statistics_to_string(plist, stats)
        print(sstr)

if __name__ == '__main__':
    main()