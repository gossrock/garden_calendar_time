from time import time as current_timestamp
from time import sleep

from garden_calendar_time import CalendarProperties, GardenDateTime
from garden_calendar_time.utcdatetime import UTCDateTime
from garden_calendar_time.location import LatLong
import garden_calendar_time.equinox_solstice as es


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



if __name__ == '__main__':
    calendar_properties = CalendarProperties('DS', es.december_solstice_before, 0)
    print(calendar_properties)
    garden_clock = GardenClock(LatLong(34, -85), calendar_properties)
    garden_clock.run(0.432)
