import requests
import json
import numpy as np

csv_filename = 'fuel.csv'
url = 'https://www.racq.com.au/ajaxPages/FuelPricesapi.ashx'

params = dict(
    fueltype='37',
    location='4122',
    # location='4000',
    includesurrounding='1'
)

resp = requests.get(url=url, params=params)
data = resp.json()
# print(json.dumps(data, indent=4))
today_list = []
cnt = 0
for station in data['Stations']:
    # today_list.append(station["Price"])
    today_list.append(float(station["Price"]))
    if cnt < 5:
        print('{} {}'.format(station["Price"], station['Name']))

    cnt += 1

price_string = ', '.join([str(i) for i in today_list])
price_string = '{}, {}'.format(
data['Timestamp'].split('T')[0],
price_string)


with open(csv_filename, 'a') as f:
    f.write(price_string)
    f.write('\n')

# print(today_list)
print('{}, {}, {}, {}, {}, {}'.format(
    data['Timestamp'].split('T')[0],
    len(today_list),
    np.min(today_list),
    np.max(today_list),
    np.mean(today_list),
    np.std(today_list),
))