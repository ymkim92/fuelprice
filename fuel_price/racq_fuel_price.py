#!/usr/bin/env python3
"""get petrol price from RACQ"""
import logging
import sys
from argparse import ArgumentParser

import numpy as np
import requests

logging.basicConfig()
log = logging.getLogger(__name__)


URL = "https://www.racq.com.au/ajaxPages/fuelprice/FuelPricesapi.ashx"

PARAMS = {
    "fueltype": "37",  # 91
    "lat": "-27.5480097",
    "lng": "153.09129859999996",
    "includesurrounding": "1",
}

FUEL_DICT = {
    "E10": "40",
    "91": "37",
    "95": "38",
    "98": "39",
    "Diesel": "1",
    "LPG": "41",
}


def get_list(fueltype: str, lat: str, lon: str) -> list:
    """get list of fuel prices from RACQ API

    Args:
        fueltype (str): Fuel type code from FUEL_DICT
        lat (str): Latitude coordinate
        lon (str): Longitude coordinate

    Returns:
        list: First element is timestamp, followed by fuel prices
    """
    PARAMS["fueltype"] = fueltype
    PARAMS["lat"] = lat
    PARAMS["lng"] = lon

    log.debug("send requests")
    resp = requests.get(url=URL, params=PARAMS, timeout=3)
    log.debug("received requests")

    data = resp.json()
    today_list = [data["Timestamp"].split(".")[0]]

    cnt = 0
    for station in data["Stations"]:
        today_list.append(float(station["Price"]))
        if cnt < 10:
            log.info("%s %s", station["Price"], station["Name"])
        cnt += 1

    return today_list


def convert_pricelist_to_string(prices):
    """convert"""
    price_string = prices[0] + ","
    price_string += ",".join([str(i) for i in prices[1:]])

    return price_string


def convert_statistics_to_string(plist, stats):
    """convert"""
    string = plist[0] + ","
    string += ",".join([str(i) for i in stats])
    return string


def get_stats(price_list):
    """get stats"""
    flist = [float(x) for x in price_list[1:]]
    return (len(flist), np.min(flist), np.max(flist), np.mean(flist), np.std(flist))


def get_arguments():
    """get arguments from command line"""
    parser = ArgumentParser(description="Get fuel price from RACQ")
    parser.add_argument("fuel_type", type=str, choices=list(FUEL_DICT.keys()), help="Fuel type")
    parser.add_argument("lat", type=str, help="latitude")
    parser.add_argument("lon", type=str, help="longitude")
    parser.add_argument(
        "-l",
        "--log",
        type=str,
        choices=["INFO", "DEBUG", "WARNING", "ERROR"],
        default="ERROR",
        help="Log level, default=ERROR",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        choices=["stats", "raw"],
        default="stats",
        help="Output format: statistics only(default), raw data",
    )

    return parser.parse_args(sys.argv[1:])


def set_log_level(log_level):
    """set log level"""
    if log_level == "DEBUG":
        logl = logging.DEBUG
    elif log_level == "INFO":
        logl = logging.INFO
    elif log_level == "WARNING":
        logl = logging.WARNING
    else:
        logl = logging.ERROR

    log.setLevel(logl)


def main():
    """main"""
    log.debug("started..")
    args = get_arguments()

    set_log_level(args.log)

    fuel = FUEL_DICT[args.fuel_type]
    plist = get_list(fuel, args.lat, args.lon)
    if args.output == "raw":
        pstr = convert_pricelist_to_string(plist)
        print(pstr)
    else:
        stats = get_stats(plist)
        sstr = convert_statistics_to_string(plist, stats)
        print(sstr)


if __name__ == "__main__":
    main()
