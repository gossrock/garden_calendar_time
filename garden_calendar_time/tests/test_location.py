import pytest

from garden_calendar_time.location import LatLong

lat_cases = [(0, 0),
             (45, 45),
             (90, 90),
             (135, 45),
             (-45, -45),
             (-90, -90),
             (-135, -45),
             (180, 0),
             (-180, 0),
             (-225, 45),
             (225, -45),
             (360, 0),
             (-360, 0)]

long_cases = [(0, 0),
             (45, 45),
             (90, 90),
             (135, 135),
             (-45, -45),
             (-90, -90),
             (-135, -135),
             (180, 180),
             (-180, 180),
             (-225, 135),
             (225, -135),
             (360, 0),
             (-360, 0)]

@pytest.mark.parametrize('init_lat, after_lat', lat_cases)
def test_LatLong_init_lat(init_lat, after_lat):
    assert LatLong(init_lat, 0).lat == after_lat


@pytest.mark.parametrize('init_long, after_long', long_cases)
def test_LatLong_init_long(init_long, after_long):
    assert LatLong(0, init_long).long == after_long