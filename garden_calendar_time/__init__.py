from typing import NamedTuple, Optional
from typing import Union

from time import time as current_timestamp
from time import sleep

from garden_calendar_time.utcdatetime import UTC, UTCDateTime, UTCTime, Date, TimeDelta

from garden_calendar_time.equinox_solstice import spring_equinox_before, nearest_day_at_time_to_datetime

SECONDS_IN_DAY = 24*60*60


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


class GardenDateTime:
    _timestamp: float  # seconds since the Epoch
    _location: LatLong
    _day_start_offset: float
    # cached calculations
    _year_start: UTCDateTime
    _days: float

    def __init__(self,
                 location: LatLong,
                 datetime: Union[float, UTCDateTime, 'GardenDateTime'],
                 day_start_offset: float = -0.25,
                 _year_start: Optional[UTCDateTime] = None) -> None:
        self.timestamp = datetime
        self._location = location
        self._day_start_offset = day_start_offset
        self._year_start = _year_start

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, datetime = Union[float, UTCDateTime, 'GardenDateTime']) -> None:
        # clear cached calculations because they may no longer be valid
        self._year_start = None
        self._days = None

        # set _timestamp
        if isinstance(datetime, float):
            self._timestamp = datetime
        elif isinstance(datetime, datetime):
            self._timestamp = datetime.timestamp()
        elif isinstance(datetime, GardenDateTime):
            self._timestamp = datetime._timestamp

    @property
    def location(self) -> LatLong:
        return self._location

    @property
    def location_time_offset(self) -> float:
        return self.location.long/360

    @property
    def day_start_offset(self) -> float:
        return self._day_start_offset

    @property
    def total_offset(self) -> float:
        return self.location_time_offset + self.day_start_offset

    @property
    def year(self) -> int:
        return self.year_start.year

    @property
    def year_start(self) -> UTCDateTime:
        if self._year_start is None:
            most_recent_spring_equinox = spring_equinox_before(UTCDateTime.fromtimestamp(self._timestamp), self._location.lat)
            time_after_offset = (UTCDateTime.combine(Date.today(), UTCTime(0)) + TimeDelta(days=self.total_offset)).time()

            date_time_of_start_of_current_year = nearest_day_at_time_to_datetime(time_after_offset, most_recent_spring_equinox)

            self._year_start = date_time_of_start_of_current_year
        return self._year_start

    @property
    def days(self) -> float:
        if self._days is None:
            self._days = (self.timestamp - self.year_start.timestamp())/SECONDS_IN_DAY
        return self._days

    def days_place(self, place_exp) -> int:
        return int(((self.days * (10**(- place_exp))) % 10) // 1)

    @property
    def dec_day_hour(self) -> str:
        return f'{self.days_place(-1)}'

    @property
    def dec_day_min(self) -> str:
        return f'{self.days_place(-2)}{self.days_place(-3)}'

    @property
    def dec_day_sec(self) -> str:
        return f'{self.days_place(-4)}{self.days_place(-5)}'


    def __str__(self) -> str:
        return f'{self.year} SE +{int(self.days)}.{self.dec_day_hour}:{self.dec_day_min}:{self.dec_day_sec}'



class GardenClock:
    location: LatLong
    _year_start: UTCDateTime

    def __init__(self, location: LatLong) -> None:
        self.location = location
        self._year_start = GardenDateTime(location, current_timestamp()).year_start

    @property
    def current_time(self) -> GardenDateTime:
        return GardenDateTime(self.location, datetime=current_timestamp(), _year_start=self._year_start)

    def run(self, refresh_time: float) -> None:
        print()
        while True:
            print(f'\r{self.current_time}', end='')
            sleep(refresh_time)


if __name__ == '__main__':
    garden_clock = GardenClock(LatLong(34, -85))
    garden_clock.run(0.432)


