#!/usr/bin/env python3
import requests
import json
import numpy as np
import pathlib
import shutil
import slack
from configparser import ConfigParser


csv_path = '/home/ykim/log/'
csv_filename = 'fuel.csv'
log_filename = 'fuel.log'
csv_prev_prices = 'prevprices.csv'
csv_curr_prices = 'currprices.csv'

url = 'https://www.racq.com.au/ajaxPages/FuelPricesapi.ashx'

params = dict(
    fueltype='37',
    location='4122',
    # location='4000',
    includesurrounding='1'
)

def get_list():
    resp = requests.get(url=url, params=params)
    data = resp.json()
    # print(json.dumps(data, indent=4))
    today_list = [ data['Timestamp'].split('.')[0]]
    cnt = 0
    for station in data['Stations']:
        # today_list.append(station["Price"])
        today_list.append(float(station["Price"]))
        if cnt < 5:
            print('{} {}'.format(station["Price"], station['Name']))

        cnt += 1

    return today_list

def save_list(prices):
    price_string = prices[0] + ', '
    price_string += ', '.join([str(i) for i in prices[1:]])

    with open(csv_path+csv_filename, 'a') as f:
        f.write(price_string)
        f.write('\n')

    path = pathlib.Path(csv_path+csv_curr_prices)
    if path.exists():
        shutil.copy(csv_path+csv_curr_prices, csv_path+csv_prev_prices)

    with open(csv_path+csv_curr_prices, 'w') as f:
        f.write(price_string)
        f.write('\n')


def is_price_up():
    ret = False
    cause = []
    with open(csv_path+csv_curr_prices, 'r') as f:
        curr_prices = f.readline()
        curr_stats = get_stats(curr_prices.split(','))

    with open(csv_path+csv_prev_prices, 'r') as f:
        prev_prices = f.readline()
        prev_stats = get_stats(prev_prices.split(','))

    if curr_stats[1] > prev_stats[1]:
        ret = True
        cause.append('min')

    if curr_stats[2] > prev_stats[2]:
        ret = True
        cause.append('max')

    if curr_stats[3] > prev_stats[3]:
        ret = True
        cause.append('avg')

    if curr_stats[4] > prev_stats[4]:
        ret = True
        cause.append('std')

    return ret, cause, prev_stats, curr_stats

    

def get_stats(price_list):
    flist = [float(x) for x in price_list[1:]]
    return ( len(flist), np.min(flist), np.max(flist), np.mean(flist), np.std(flist) )

def send_notification(msg):
    parser = ConfigParser()
    parser.read('/home/ykim/devel/python/fuelprice/token.cfg')
    token = parser.get('slack', 'token')

    client = slack.WebClient(token)

    response = client.chat_postMessage(
        channel='#notification',
        text=msg)
    assert response["ok"]

if __name__ == '__main__':
    plist = get_list()
    save_list(plist)
    ret, cause_list, prev, curr = is_price_up()
    if ret:
        msg = '{}\n{}\n{}\n'.format(cause_list, prev, curr)
        send_notification(msg)
