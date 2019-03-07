from typing import NamedTuple
from typing import Union

from datetime import datetime as DateTime
from time import time as current_timestamp


class LatLong:
    _lat: float
    _long: float

    def __init__(self, lat: float, long: float) -> None:
        # adjust long to be -180 < long <= 180
        fixed_long = long % 360
        if fixed_long > 180:
            fixed_long -= 360
        self._long = fixed_long

        # adjust lat to be -90 <= lat <= 90
        fixed_lat = lat % 360
        if 90 < fixed_lat <= 180:
            # move horizotally to quadrent I
            fixed_lat = abs(fixed_lat - 180)
        elif 180 < fixed_lat < 360:
            # make negitive representation
            fixed_lat -= 360
            if -180 < fixed_lat < -90:
                # move horizontally to quadernt IV (negitive representation)
                fixed_lat = -(fixed_lat + 180)
        self._lat = fixed_lat

    @property
    def lat(self):
        return self._lat

    @property
    def long(self):
        return self._long


'''
class YearStartType(int): ...


SAME_AS_GREGORIAN = YearStartType(0)
# these will change based on which hemisphere (north v. south)
SPRING_EQUINOX = YearStartType(1)
SUMMER_SOLSTICE = YearStartType(2)
FALL_EQUINOX = YearStartType(3)
WINTER_EQUINOX = YearStartType(4)

# these will not change based on hemisphere (north v. south)
MAR_EQUINOX = YearStartType(-1)
JUN_SOLSTICE = YearStartType(-2)
SEPT_EQUINOX = YearStartType(-3)
DEC_SOLSTICE = YearStartType(-4)

class CalendarSettings(NamedTuple):
    start_of_day: float # value  >=0 and <1, represents fraction of from midnight to consider start of day
    year_start_type: YearStartType
    year_start_offset_days: int


# Default: Year starts at 6 AM closest to moment of spring equinox
DEFALUT_CALENDAR_SETTINGS = CalendarSettings(start_of_day=0.25, # 6AM 
                                             year_start_type=SPRING_EQUINOX, 
                                             year_start_offset_days=0)
'''



class GardenDateTime:
    _timestamp: float # seconds since the Epoch
    _location: LatLong
    _year: int
    _day: float

    def __init__(self,
                 location: LatLong,
                 datetime: Union[float, DateTime, 'GardenDateTime'] = current_timestamp()) -> None:
        self.timestamp = datetime
        self._location = location

    @property
    def timestamp(self):
        return self.timestamp

    @timestamp.setter
    def timestamp(self, datetime = Union[float, DateTime, 'GardenDateTime']) -> None:
        if isinstance(datetime, float):
            self._timestamp = datetime
        elif isinstance(datetime, datetime):
            self._timestamp = datetime.timestamp()
        elif isinstance(datetime, GardenDateTime):
            self._timestamp = datetime._timestamp

        self._calc_garden_time_values()

    @property
    def year(self): ...
    def day(self): ...

    def _calc_garden_time_values(self):
        pass
