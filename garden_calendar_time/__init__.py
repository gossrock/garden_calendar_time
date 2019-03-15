from typing import NamedTuple, Optional, Callable
from typing import Union

from time import time as current_timestamp

from garden_calendar_time.location import LatLong
from garden_calendar_time.utcdatetime import UTC, UTCDateTime, UTCTime, Date, TimeDelta

import garden_calendar_time.equinox_solstice as es

SECONDS_IN_DAY = 24*60*60




class CalendarProperties(NamedTuple):
    start_event_name: str
    start_event_function: Callable
    day_start_offset: float


class GardenDateTime:
    _timestamp: float  # seconds since the Epoch
    _location: LatLong
    _calendar_properties: CalendarProperties
    # cached calculations
    _year_start: UTCDateTime
    _days: float

    def __init__(self,
                 location: LatLong,
                 datetime: Union[float, UTCDateTime, 'GardenDateTime'],
                 calendar_properties: CalendarProperties = CalendarProperties('SE', es.spring_equinox_before, -0.25),
                 _year_start: Optional[UTCDateTime] = None) -> None:
        self.timestamp = datetime
        self._location = location
        self._calendar_properties = calendar_properties
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

    def refresh(self) -> None:
        self.timestamp = current_timestamp()

    @property
    def location(self) -> LatLong:
        return self._location

    @property
    def location_time_offset(self) -> float:
        return self.location.long/360

    @property
    def day_start_offset(self) -> float:
        return self._calendar_properties.day_start_offset

    @property
    def total_offset(self) -> float:
        return self.location_time_offset + self.day_start_offset

    @property
    def year(self) -> int:
        return self.year_start.year

    @property
    def year_start(self) -> UTCDateTime:
        if self._year_start is None:
            most_recent_year_start_event = self._calendar_properties.start_event_function(UTCDateTime.fromtimestamp(self._timestamp), self._location)
            time_after_offset = (UTCDateTime.combine(Date.today(), UTCTime(0)) - TimeDelta(days=self.total_offset)).time()
            date_time_of_start_of_current_year = es.nearest_day_at_time_to_datetime(time_after_offset, most_recent_year_start_event)
            self._year_start = date_time_of_start_of_current_year
        return self._year_start

    @property
    def days(self) -> float:
        if self._days is None:
            self._days = (self.timestamp - self.year_start.timestamp())/SECONDS_IN_DAY
        return self._days

    def days_place(self, place_exp) -> int:
        return int(((abs(self.days) * (10**(- place_exp))) % 10) // 1)

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
        return f'{self.year} {self._calendar_properties.start_event_name} {int(self.days):+}.{self.dec_day_hour}:{self.dec_day_min}:{self.dec_day_sec}'

    def __gt__(self, other) -> bool:
        return self.timestamp > other.timestamp