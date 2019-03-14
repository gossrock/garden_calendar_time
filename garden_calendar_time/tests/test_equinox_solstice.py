import pytest

from garden_calendar_time.utcdatetime import UTCDateTime
from garden_calendar_time.utcdatetime import UTCTime

from garden_calendar_time.location import LatLong
import garden_calendar_time.equinox_solstice as es

LOC1 = LatLong(45, 45)
LOC2 = LatLong(-45, -45)

location_data = [LOC1, LOC2]

YEAR1 = es.YearEquinoxSolsticData(2000,
                                  UTCDateTime(2000, 3, 20, 7, 35),
                                  UTCDateTime(2000, 6, 21, 1, 47),
                                  UTCDateTime(2000, 9, 22, 17, 27),
                                  UTCDateTime(2000, 12, 21, 13, 37))

YEAR2 = es.YearEquinoxSolsticData(2001,
                                  UTCDateTime(2001, 3, 20, 13, 30),
                                  UTCDateTime(2001, 6, 21, 7, 37),
                                  UTCDateTime(2001, 9, 22, 23, 4),
                                  UTCDateTime(2001, 12, 21, 19, 21))


YEAR3 = es.YearEquinoxSolsticData(2002,
                                  UTCDateTime(2002, 3, 20, 19, 16),
                                  UTCDateTime(2002, 6, 21, 13, 24),
                                  UTCDateTime(2002, 9, 23, 4, 55),
                                  UTCDateTime(2002, 12, 22, 1, 14))

year_data = [YEAR1,YEAR2, YEAR3]

year_2_dates = [UTCDateTime(YEAR2.year, 3, 15),
                UTCDateTime(YEAR2.year, 3, 30),
                UTCDateTime(YEAR2.year, 6, 15),
                UTCDateTime(YEAR2.year, 6, 30),
                UTCDateTime(YEAR2.year, 9, 15),
                UTCDateTime(YEAR2.year, 9, 30),
                UTCDateTime(YEAR2.year, 12, 15),
                UTCDateTime(YEAR2.year, 12, 30),
                ]

@pytest.mark.parametrize('year_data', year_data)
def test_year_data(year_data) -> None:
    assert es.year_data(year_data.year) == year_data


@pytest.mark.parametrize('year_data', year_data)
def test_march_equinox(year_data) -> None:
    assert es.march_equinox(year_data.year) == year_data.march_equinox


@pytest.mark.parametrize('year_data', year_data)
def test_june_solstice(year_data) -> None:
    assert es.june_solstice(year_data.year) == year_data.june_solstice


@pytest.mark.parametrize('year_data', year_data)
def test_septomber_equinox(year_data) -> None:
    assert es.september_equinox(year_data.year) == year_data.september_equinox


@pytest.mark.parametrize('year_data', year_data)
def test_decemeber_solstice(year_data) -> None:
    assert es.december_solstice(year_data.year) == year_data.december_solstice


@pytest.mark.parametrize('loc_data', location_data)
@pytest.mark.parametrize('year_data', year_data)
def test_spring_equinox(loc_data, year_data) -> None:
    if loc_data.long >= 0:
        assert es.spring_equinox(year_data.year, loc_data) == year_data.march_equinox
    else:
        assert es.spring_equinox(year_data.year, loc_data) == year_data.september_equinox


@pytest.mark.parametrize('loc_data', location_data)
@pytest.mark.parametrize('year_data', year_data)
def test_summer_solstice(loc_data, year_data) -> None:
    if loc_data.long >= 0:
        assert es.summer_solstice(year_data.year, loc_data) == year_data.june_solstice
    else:
        assert es.summer_solstice(year_data.year, loc_data) == year_data.december_solstice


@pytest.mark.parametrize('loc_data', location_data)
@pytest.mark.parametrize('year_data', year_data)
def test_fall_equinox(loc_data, year_data) -> None:
    if loc_data.long >= 0:
        assert es.fall_equinox(year_data.year, loc_data) == year_data.september_equinox
    else:
        assert es.fall_equinox(year_data.year, loc_data) == year_data.march_equinox


@pytest.mark.parametrize('loc_data', location_data)
@pytest.mark.parametrize('year_data', year_data)
def test_winter_solstice(loc_data, year_data) -> None:
    if loc_data.long >= 0:
        assert es.winter_solstice(year_data.year, loc_data) == year_data.december_solstice
    else:
        assert es.winter_solstice(year_data.year, loc_data) == year_data.june_solstice


@pytest.mark.parametrize('date', year_2_dates)
def test_march_equinox_after(date) -> None:
    m = YEAR2.march_equinox.month
    d = YEAR2.march_equinox.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.march_equinox_after(date) == YEAR2.march_equinox
    else:
        assert es.march_equinox_after(date) == YEAR3.march_equinox

@pytest.mark.parametrize('date', year_2_dates)
def test_march_equinox_before(date) -> None:
    m = YEAR2.march_equinox.month
    d = YEAR2.march_equinox.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.march_equinox_before(date) == YEAR1.march_equinox
    else:
        assert es.march_equinox_before(date) == YEAR2.march_equinox


@pytest.mark.parametrize('date', year_2_dates)
def test_june_solstice_after(date) -> None:
    m = YEAR2.june_solstice.month
    d = YEAR2.june_solstice.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.june_solstice_before(date) == YEAR1.june_solstice
    else:
        assert es.june_solstice_before(date) == YEAR2.june_solstice


@pytest.mark.parametrize('date', year_2_dates)
def test_june_solstice_before(date) -> None:
    m = YEAR2.june_solstice.month
    d = YEAR2.june_solstice.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.june_solstice_after(date) == YEAR2.june_solstice
    else:
        assert es.june_solstice_after(date) == YEAR3.june_solstice


@pytest.mark.parametrize('date', year_2_dates)
def test_september_equinox_after(date) -> None:
    m = YEAR2.september_equinox.month
    d = YEAR2.september_equinox.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.september_equinox_after(date) == YEAR2.september_equinox
    else:
        assert es.september_equinox_after(date) == YEAR3.september_equinox


@pytest.mark.parametrize('date', year_2_dates)
def test_september_equinox_before(date) -> None:
    m = YEAR2.september_equinox.month
    d = YEAR2.september_equinox.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.september_equinox_before(date) == YEAR1.september_equinox
    else:
        assert es.september_equinox_before(date) == YEAR2.september_equinox

@pytest.mark.parametrize('date', year_2_dates)
def test_december_solstice_after(date) -> None:
    m = YEAR2.december_solstice.month
    d = YEAR2.december_solstice.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.december_solstice_after(date) == YEAR2.december_solstice
    else:
        assert es.december_solstice_after(date) == YEAR3.december_solstice

@pytest.mark.parametrize('date', year_2_dates)
def test_december_solstice_before(date) -> None:
    m = YEAR2.december_solstice.month
    d = YEAR2.december_solstice.day
    if date.month < m or (date.month == m and date.day < d):
        assert es.december_solstice_before(date) == YEAR1.december_solstice
    else:
        assert es.december_solstice_before(date) == YEAR2.december_solstice

@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_spring_equinox_after(loc, date) -> None:
    m = YEAR2.march_equinox.month
    d = YEAR2.march_equinox.day
    year_2_equinox = YEAR2.march_equinox
    year_3_equinox = YEAR3.march_equinox
    if loc.long < 0:
        m = YEAR2.september_equinox.month
        d = YEAR2.september_equinox.day
        year_2_equinox = YEAR2.september_equinox
        year_3_equinox = YEAR3.september_equinox
    if date.month < m or (date.month == m and date.day < d):
        assert es.spring_equinox_after(date, loc) == year_2_equinox
    else:
        assert es.spring_equinox_after(date, loc) == year_3_equinox


@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_spring_equinox_before(loc, date) -> None:
    m = YEAR2.march_equinox.month
    d = YEAR2.march_equinox.day
    year_1_equinox = YEAR1.march_equinox
    year_2_equinox = YEAR2.march_equinox
    if loc.long < 0:
        m = YEAR2.september_equinox.month
        d = YEAR2.september_equinox.day
        year_1_equinox = YEAR1.september_equinox
        year_2_equinox = YEAR2.september_equinox
    if date.month < m or (date.month == m and date.day < d):
        assert es.spring_equinox_before(date, loc) == year_1_equinox
    else:
        assert es.spring_equinox_before(date, loc) == year_2_equinox

@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_summer_solstice_after(loc, date) -> None:
    m = YEAR2.june_solstice.month
    d = YEAR2.june_solstice.day
    year_2_solstice = YEAR2.june_solstice
    year_3_solstice = YEAR3.june_solstice
    if loc.long < 0:
        m = YEAR2.december_solstice.month
        d = YEAR2.december_solstice.day
        year_2_solstice = YEAR2.december_solstice
        year_3_solstice = YEAR3.december_solstice
    if date.month < m or (date.month == m and date.day < d):
        assert es.summer_solstice_after(date, loc) == year_2_solstice
    else:
        assert es.summer_solstice_after(date, loc) == year_3_solstice

@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_summer_solstice_before(loc, date) -> None:
    m = YEAR2.june_solstice.month
    d = YEAR2.june_solstice.day
    year_1_solstice = YEAR1.june_solstice
    year_2_solstice = YEAR2.june_solstice
    if loc.long < 0:
        m = YEAR2.december_solstice.month
        d = YEAR2.december_solstice.day
        year_1_solstice = YEAR1.december_solstice
        year_2_solstice = YEAR2.december_solstice
    if date.month < m or (date.month == m and date.day < d):
        assert es.summer_solstice_before(date, loc) == year_1_solstice
    else:
        assert es.summer_solstice_before(date, loc) == year_2_solstice

@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_fall_equinox_after(loc, date) -> None:
    m = YEAR2.september_equinox.month
    d = YEAR2.september_equinox.day
    year_2_equinox = YEAR2.september_equinox
    year_3_equinox = YEAR3.september_equinox
    if loc.long < 0:
        m = YEAR2.march_equinox.month
        d = YEAR2.march_equinox.day
        year_2_equinox = YEAR2.march_equinox
        year_3_equinox = YEAR3.march_equinox
    if date.month < m or (date.month == m and date.day < d):
        assert es.fall_equinox_after(date, loc) == year_2_equinox
    else:
        assert es.fall_equinox_after(date, loc) == year_3_equinox

@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_fall_equinox_before(loc, date) -> None:
    m = YEAR2.september_equinox.month
    d = YEAR2.september_equinox.day
    year_1_equinox = YEAR1.september_equinox
    year_2_equinox = YEAR2.september_equinox
    if loc.long < 0:
        m = YEAR2.march_equinox.month
        d = YEAR2.march_equinox.day
        year_1_equinox = YEAR1.march_equinox
        year_2_equinox = YEAR2.march_equinox
    if date.month < m or (date.month == m and date.day < d):
        assert es.fall_equinox_before(date, loc) == year_1_equinox
    else:
        assert es.fall_equinox_before(date, loc) == year_2_equinox

@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_winter_solstice_after(loc, date) -> None:
    m = YEAR2.december_solstice.month
    d = YEAR2.december_solstice.day
    year_2_solstice = YEAR2.december_solstice
    year_3_solstice = YEAR3.december_solstice
    if loc.long < 0:
        m = YEAR2.june_solstice.month
        d = YEAR2.june_solstice.day
        year_2_solstice = YEAR2.june_solstice
        year_3_solstice = YEAR3.june_solstice
    if date.month < m or (date.month == m and date.day < d):
        assert es.winter_solstice_after(date, loc) == year_2_solstice
    else:
        assert es.winter_solstice_after(date, loc) == year_3_solstice

@pytest.mark.parametrize('loc', location_data)
@pytest.mark.parametrize('date', year_2_dates)
def test_winter_solstice_before(loc, date) -> None:
    m = YEAR2.december_solstice.month
    d = YEAR2.december_solstice.day
    year_1_solstice = YEAR1.december_solstice
    year_2_solstice = YEAR2.december_solstice
    if loc.long < 0:
        m = YEAR2.june_solstice.month
        d = YEAR2.june_solstice.day
        year_1_solstice = YEAR1.june_solstice
        year_2_solstice = YEAR2.june_solstice
    if date.month < m or (date.month == m and date.day < d):
        assert es.winter_solstice_before(date, loc) == year_1_solstice
    else:
        assert es.winter_solstice_before(date, loc) == year_2_solstice


time_target_answers = [(UTCTime(6), UTCDateTime(2000, 1, 1, 12, 00),UTCDateTime(2000, 1, 1, 6, 0)),
                       (UTCTime(6), UTCDateTime(2000, 1, 1, 3, 00), UTCDateTime(2000, 1, 1, 6, 0)),
                       (UTCTime(6), UTCDateTime(2000, 1, 1, 23, 00), UTCDateTime(2000, 1, 2, 6, 0)),
                       (UTCTime(23), UTCDateTime(2000, 1, 1, 2, 00), UTCDateTime(1999, 12, 31, 23, 0))]


@pytest.mark.parametrize('time, target, answer', time_target_answers)
def test_nearest_day_at_time_to_datetime(time, target, answer) -> None:
    assert es.nearest_day_at_time_to_datetime(time, target) == answer
