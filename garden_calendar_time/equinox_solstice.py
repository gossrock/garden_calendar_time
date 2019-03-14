import csv
from pathlib import Path
from typing import NamedTuple
from typing import Dict, Callable
from functools import partial

from garden_calendar_time.location import LatLong
from garden_calendar_time.utcdatetime import UTCDateTime, Time, TimeDelta

class YearEquinoxSolsticData(NamedTuple):
    year: int
    march_equinox: UTCDateTime
    june_solstice: UTCDateTime
    september_equinox: UTCDateTime
    december_solstice: UTCDateTime


def parse_iso_date(iso_str) -> UTCDateTime:
    date, time = iso_str.split('T')
    year, month, day = date.split('-')
    hour, min, sec = time.split(':')
    return UTCDateTime(int(year), int(month), int(day), int(hour), int(min), int(sec))

def nearest_day_at_time_to_datetime(time: Time, target_datetime: UTCDateTime) -> UTCDateTime:
    half_day_in_seconds = 12 * 60 * 60
    target_date = target_datetime.date()

    choice1 = UTCDateTime.combine(target_date, time)
    choice1_diff = abs(target_datetime - choice1)
    if choice1_diff.days == 0 and choice1_diff.seconds <= half_day_in_seconds:
        return choice1

    choice2 = choice1 + TimeDelta(1)
    choice2_diff = abs(target_datetime - choice2)
    if choice2_diff.days == 0 and choice2_diff.seconds <= half_day_in_seconds:
        return choice2

    choice3 = choice1 - TimeDelta(1)
    choice3_diff = abs(target_datetime - choice3)
    if choice3_diff.days == 0 and choice3_diff.seconds <= half_day_in_seconds:
        return choice3


DATABASE: Dict[int, YearEquinoxSolsticData] = {}

DEFAULT_DATA_FILE = Path(__file__).parent.joinpath('data/equinox_solstice_data.csv')
# csv columns
YEAR = 0
MARCH_EQUINOX = 1
JUNE_SOLSTICE = 2
SEPTEMBER_EQUINOX = 3
DECEMBER_SOLSTICE = 4


def load_data_from_csv(csv_file_name: str = DEFAULT_DATA_FILE) -> None:
    with open(csv_file_name) as data_file:
        csv_reader = csv.reader(data_file)
        for row in csv_reader:
            year = int(row[YEAR])
            march_equinox = parse_iso_date(row[MARCH_EQUINOX])
            june_solstice = parse_iso_date(row[JUNE_SOLSTICE])
            september_equinox = parse_iso_date(row[SEPTEMBER_EQUINOX])
            december_solstice = parse_iso_date(row[DECEMBER_SOLSTICE])
            DATABASE[year] = YearEquinoxSolsticData(year,
                                                    march_equinox,
                                                    june_solstice,
                                                    september_equinox,
                                                    december_solstice)


def year_data(year: int) -> YearEquinoxSolsticData:
    if DATABASE == {}:
        load_data_from_csv()

    return DATABASE[year]


# specific equinoxes and solstices
def march_equinox(year: int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return year_data(year).march_equinox


def june_solstice(year: int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return year_data(year).june_solstice


def september_equinox(year: int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return year_data(year).september_equinox


def december_solstice(year:int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return year_data(year).december_solstice


# seasonal equinoxes and solstices
def spring_equinox(year: int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    if location.lat >= 0:
        return march_equinox(year)
    else:
        return september_equinox(year)


def summer_solstice(year: int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    if location.lat >= 0:
        return june_solstice(year)
    else:
        return december_solstice(year)


def fall_equinox(year: int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    if location.lat >= 0:
        return september_equinox(year)
    else:
        return march_equinox(year)


def winter_solstice(year: int, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    if location.lat >= 0:
        return december_solstice(year)
    else:
        return june_solstice(year)


# reletive specific equnoxes and solstices
def _after(datetime:UTCDateTime, event_function: Callable, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    if (event_function(datetime.year, location) - datetime).days >= 0:
        return event_function(datetime.year, location)
    else:
        return event_function(datetime.year + 1, location)


def _before(datetime:UTCDateTime, event_function: Callable, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    if (event_function(datetime.year, location) - datetime).days < 0:
        return event_function(datetime.year, location)
    else:
        return event_function(datetime.year - 1, location)


def march_equinox_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, march_equinox, location)


def march_equinox_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, march_equinox, location)


def june_solstice_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, june_solstice, location)


def june_solstice_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, june_solstice, location)


def september_equinox_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, september_equinox, location)


def september_equinox_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, september_equinox, location)


def december_solstice_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, december_solstice, location)


def december_solstice_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, december_solstice, location)


# reletive seasonal equinoxes and solstices
def spring_equinox_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, spring_equinox, location)


def spring_equinox_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, spring_equinox, location)


def summer_solstice_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, summer_solstice, location)


def summer_solstice_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, summer_solstice, location)


def fall_equinox_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, fall_equinox, location)


def fall_equinox_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, fall_equinox, location)


def winter_solstice_after(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _after(datetime, winter_solstice, location)


def winter_solstice_before(datetime: UTCDateTime, location: LatLong = LatLong(0,0)) -> UTCDateTime:
    return _before(datetime, winter_solstice, location)


