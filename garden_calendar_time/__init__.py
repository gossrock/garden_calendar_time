from typing import NamedTuple, Optional, Callable, List
from typing import Union

from time import time as current_timestamp
from time import sleep

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



class GardenClock:
    location: LatLong
    _year_start: UTCDateTime
    _calendar_properties: CalendarProperties
    _current_time: GardenDateTime

    def __init__(self, location: LatLong, calendar_properties: CalendarProperties) -> None:
        self.location = location
        self._calendar_properties = calendar_properties
        self._current_time = GardenDateTime(location, current_timestamp(), calendar_properties)
        self._year_start = self._current_time.year_start


    @property
    def current_time(self) -> GardenDateTime:
        if self._current_time is None:
            self._current_time = GardenDateTime(self.location, current_timestamp(), self._calendar_properties, _year_start=self._year_start)
            return self._current_time
        else:
            self._current_time.refresh()
            return self._current_time

    def run(self, refresh_time: float) -> None:
        print()
        while True:
            print(f'\r{self.current_time}', end='')
            sleep(refresh_time)

class AllGardenClocks:
    location: LatLong
    clocks: List[GardenDateTime]

    def __init__(self, location: LatLong, day_start_offset: int):
        self.location = location
        clocks = []
        cp = CalendarProperties('SE+', es.spring_equinox_before, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        cp = CalendarProperties('SS+', es.summer_solstice_before, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        cp = CalendarProperties('FE+', es.fall_equinox_before, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        cp = CalendarProperties('WS+', es.winter_solstice_before, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        cp = CalendarProperties('SE-', es.spring_equinox_after, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        cp = CalendarProperties('SS-', es.summer_solstice_after, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        cp = CalendarProperties('FE-', es.fall_equinox_after, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        cp = CalendarProperties('WS-', es.winter_solstice_after, day_start_offset)
        clocks.append(GardenDateTime(self.location, current_timestamp(), cp))
        self.clocks = clocks

    def refresh_clocks(self) -> None:
        for clock in self.clocks:
            clock.refresh()
        self.clocks.sort()


    def run(self, refresh_time: float = 1) -> None:
        while True:
            self.refresh_clocks()
            for clock in self.clocks:
                print(f'{clock}')
            sleep(refresh_time)
            print('\033[F' * len(self.clocks), end='')



if __name__ == '__main__':
    '''
    from garden_calendar_time.equinox_solstice import winter_solstice_before
    calendar_properties = CalendarProperties('DS', es.december_solstice_before, 0)
    print(calendar_properties)
    garden_clock = GardenClock(LatLong(34, -85), calendar_properties)
    garden_clock.run(0.432)
    '''
    from datetime import timezone, timedelta, datetime
    now = datetime.now(tz=timezone(timedelta(hours=-4)))
    partial_day = now.hour/24 + now.minute/(24*60) + now.second/(24*60*60)
    location = LatLong(34, -60)
    AllGardenClocks(location, -0.25).run(0.432)


