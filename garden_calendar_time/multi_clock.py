from typing import List

from time import time as current_timestamp
from time import sleep

from garden_calendar_time import GardenDateTime, CalendarProperties
from garden_calendar_time.location import LatLong
import garden_calendar_time.equinox_solstice as es

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
    from datetime import timezone, timedelta, datetime
    now = datetime.now(tz=timezone(timedelta(hours=-4)))
    partial_day = now.hour/24 + now.minute/(24*60) + now.second/(24*60*60)
    location = LatLong(34, -60)
    AllGardenClocks(location, -0.25).run(0.432)


