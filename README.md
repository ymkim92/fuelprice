# Get fuel price of QLD, Australia

It collects data from [RACQ web site](https://www.racq.com.au/cars-and-driving/driving/fair-fuel-prices).

## Installation

```
pip install https://github.com/ymkim92/fuelprice/archive/master.zip
```

## Usage

```
usage: racq_fuel_price [-h] [-l {INFO,DEBUG,WARNING,ERROR}] [-o {stats,raw}]
                       {E10,91,95,98,Diesel,LPG} lat lon

Get fuel price from RACQ

positional arguments:
  {E10,91,95,98,Diesel,LPG}
                        Fuel type
  lat                   latitude
  lon                   longitude

optional arguments:
  -h, --help            show this help message and exit
  -l {INFO,DEBUG,WARNING,ERROR}, --log {INFO,DEBUG,WARNING,ERROR}
                        Log level, default=ERROR
  -o {stats,raw}, --output {stats,raw}
                        Output format: statistics only(default), raw data
```

## Example

```
$ racq_fuel_price 91 -27.5480097 153.09129859999996 -l INFO
INFO:fuel_price.racq_fuel_price:124.9 7-Eleven Pinelands Road
INFO:fuel_price.racq_fuel_price:124.9 7-Eleven Compton Rd
INFO:fuel_price.racq_fuel_price:125.9 COLES EXPRESS SUNNYBANK
INFO:fuel_price.racq_fuel_price:126.7 7-ELEVEN SALISBURY
INFO:fuel_price.racq_fuel_price:126.9 Caltex Starmart Sunnybank
INFO:fuel_price.racq_fuel_price:126.9 Caltex Sunnybank Hills
INFO:fuel_price.racq_fuel_price:127.5 Caltex Woolworths Macgregor
INFO:fuel_price.racq_fuel_price:127.5 Puma Eight Mile Plains
INFO:fuel_price.racq_fuel_price:127.5 PUMA WISHART
INFO:fuel_price.racq_fuel_price:127.5 7-Eleven Mackenzie
2019-08-09T15:44:27, 36, 124.9, 165.9, 137.26944444444442, 16.589401225622684
                     ^^                                    ^^^^^^^^^^^^^^^^^^^
                     Number of petrol stations             STD
                         ^^^^^
                         Lowest price
                                ^^^^^
                                Highest price
                                        ^^^^^^^^^^^^^^^^^^
                                        Mean
                                
```

```
$ racq_fuel_price 91 -27.5480097 153.09129859999996 -o raw
2019-08-09T15:45:49, 124.9, 124.9, 125.9, 126.7, 126.9, 126.9, 127.5, 127.5, 127.5, 127.5, 127.5, 127.5, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 127.9, 129.9, 134.9, 165.8, 165.9, 165.9, 165.9, 165.9, 165.9, 165.9, 165.9, 165.9
```