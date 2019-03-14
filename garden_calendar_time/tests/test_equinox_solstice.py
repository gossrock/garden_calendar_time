from garden_calendar_time.utcdatetime import UTCDateTime as DateTime
from garden_calendar_time.utcdatetime import UTCTime as Time

from garden_calendar_time.location import LatLong
import garden_calendar_time.equinox_solstice as es

LOC1 = LatLong(45, 45)
LOC2 = LatLong(-45, -45)

YEAR1 = es.YearEquinoxSolsticData(2000,
                                  DateTime(2000, 3, 20, 7, 35),
                                  DateTime(2000, 6, 21, 1, 47),
                                  DateTime(2000, 9, 22, 17, 27),
                                  DateTime(2000, 12, 21, 13, 37))

YEAR2 = es.YearEquinoxSolsticData(2001,
                                  DateTime(2001, 3, 20, 13, 30),
                                  DateTime(2001, 6, 21, 7, 37),
                                  DateTime(2001, 9, 22, 23, 4),
                                  DateTime(2001, 12, 21, 19, 21))


YEAR3 = es.YearEquinoxSolsticData(2002,
                                  DateTime(2002, 3, 20, 19, 16),
                                  DateTime(2002, 6, 21, 13, 24),
                                  DateTime(2002, 9, 23, 4, 55),
                                  DateTime(2002, 12, 22, 1, 14))

def test_year_data() -> None:
    assert es.year_data(YEAR1.year) == YEAR1
    assert es.year_data(YEAR2.year) == YEAR2

def test_march_equinox() -> None:
    assert es.march_equinox(YEAR1.year) == YEAR1.march_equinox
    assert es.march_equinox(YEAR2.year) == YEAR2.march_equinox

def test_june_solstice() -> None:
    assert es.june_solstice(YEAR1.year) == YEAR1.june_solstice
    assert es.june_solstice(YEAR2.year) == YEAR2.june_solstice

def test_septomber_equinox() -> None:
    assert es.september_equinox(YEAR1.year) == YEAR1.september_equinox
    assert es.september_equinox(YEAR2.year) == YEAR2.september_equinox

def test_decemeber_solstice() -> None:
    assert es.december_solstice(YEAR1.year) == YEAR1.december_solstice
    assert es.december_solstice(YEAR2.year) == YEAR2.december_solstice

def test_spring_equinox() -> None:
    assert es.spring_equinox(YEAR1.year, LOC1) == YEAR1.march_equinox
    assert es.spring_equinox(YEAR2.year, LOC2) == YEAR2.september_equinox

def test_summer_solstice() -> None:
    assert es.summer_solstice(YEAR1.year, LOC1) == YEAR1.june_solstice
    assert es.summer_solstice(YEAR2.year, LOC2) == YEAR2.december_solstice

def test_fall_equinox() -> None:
    assert es.fall_equinox(YEAR1.year, LOC1) == YEAR1.september_equinox
    assert es.fall_equinox(YEAR2.year, LOC2) == YEAR2.march_equinox

def test_winter_solstice() -> None:
    assert es.winter_solstice(YEAR1.year, LOC1) == YEAR1.december_solstice
    assert es.winter_solstice(YEAR2.year, LOC2) == YEAR2.june_solstice

def test_march_equinox_after() -> None:
    assert es.march_equinox_after(DateTime(YEAR1.year, 1, 1)) == YEAR1.march_equinox
    assert es.march_equinox_after(YEAR1.march_equinox) == YEAR1.march_equinox
    assert es.march_equinox_after(DateTime(YEAR1.year, 3, 31)) == YEAR2.march_equinox

def test_march_equinox_before() -> None:
    assert es.march_equinox_before(DateTime(YEAR2.year, 1, 1)) == YEAR1.march_equinox
    assert es.march_equinox_before(YEAR2.march_equinox) == YEAR1.march_equinox
    assert es.march_equinox_before(DateTime(YEAR2.year, 3, 31)) == YEAR2.march_equinox

def test_june_solstice_after() -> None:
    assert es.june_solstice_after(DateTime(YEAR1.year, 1, 1)) == YEAR1.june_solstice
    assert es.june_solstice_after(YEAR1.june_solstice) == YEAR1.june_solstice
    assert es.june_solstice_after(DateTime(YEAR1.year, 6, 30)) == YEAR2.june_solstice

def test_june_solstice_before() -> None:
    assert es.june_solstice_before(DateTime(YEAR2.year, 1, 1)) == YEAR1.june_solstice
    assert es.june_solstice_before(YEAR2.june_solstice) == YEAR1.june_solstice
    assert es.june_solstice_before(DateTime(YEAR2.year, 6, 30)) == YEAR2.june_solstice

def test_september_equinox_after() -> None:
    assert es.september_equinox_after(DateTime(YEAR1.year, 1, 1)) == YEAR1.september_equinox
    assert es.september_equinox_after(YEAR1.september_equinox) == YEAR1.september_equinox
    assert es.september_equinox_after(DateTime(YEAR1.year, 9, 30)) == YEAR2.september_equinox

def test_september_equinox_before() -> None:
    assert es.september_equinox_before(DateTime(YEAR2.year, 1, 1)) == YEAR1.september_equinox
    assert es.september_equinox_before(YEAR2.september_equinox) == YEAR1.september_equinox
    assert es.september_equinox_before(DateTime(YEAR2.year, 9, 30)) == YEAR2.september_equinox

def test_december_solstice_after() -> None:
    assert es.december_solstice_after(DateTime(YEAR1.year, 1, 1)) == YEAR1.december_solstice
    assert es.december_solstice_after(YEAR1.december_solstice) == YEAR1.december_solstice
    assert es.december_solstice_after(DateTime(YEAR1.year, 12, 30)) == YEAR2.december_solstice

def test_december_solstice_before() -> None:
    assert es.december_solstice_before(DateTime(YEAR2.year, 1, 1)) == YEAR1.december_solstice
    assert es.december_solstice_before(YEAR2.december_solstice) == YEAR1.december_solstice
    assert es.december_solstice_before(DateTime(YEAR2.year, 12, 30)) == YEAR2.december_solstice


def test_spring_equinox_after() -> None:
    assert es.spring_equinox_after(DateTime(YEAR1.year, 1, 1), LOC1) == YEAR1.march_equinox
    assert es.spring_equinox_after(YEAR1.march_equinox, LOC1) == YEAR1.march_equinox
    assert es.spring_equinox_after(DateTime(YEAR1.year, 3, 31), LOC1) == YEAR2.march_equinox

    assert es.spring_equinox_after(DateTime(YEAR1.year, 1, 1), LOC2) == YEAR1.september_equinox
    assert es.spring_equinox_after(YEAR1.september_equinox, LOC2) == YEAR1.september_equinox
    assert es.spring_equinox_after(DateTime(YEAR1.year, 9, 30), LOC2) == YEAR2.september_equinox


def test_spring_equinox_before() -> None:
    assert es.spring_equinox_before(DateTime(YEAR2.year, 1, 1), LOC1) == YEAR1.march_equinox
    assert es.spring_equinox_before(YEAR2.march_equinox, LOC1) == YEAR1.march_equinox
    assert es.spring_equinox_before(DateTime(YEAR2.year, 3, 31), LOC1) == YEAR2.march_equinox

    assert es.spring_equinox_before(DateTime(YEAR2.year, 1, 1), LOC2) == YEAR1.september_equinox
    assert es.spring_equinox_before(YEAR2.september_equinox, LOC2) == YEAR1.september_equinox
    assert es.spring_equinox_before(DateTime(YEAR2.year, 9, 30), LOC2) == YEAR2.september_equinox


def test_summer_solstice_after() -> None:
    assert es.summer_solstice_after(DateTime(YEAR1.year, 1, 1), LOC1) == YEAR1.june_solstice
    assert es.summer_solstice_after(YEAR1.june_solstice, LOC1) == YEAR1.june_solstice
    assert es.summer_solstice_after(DateTime(YEAR1.year, 6, 30), LOC1) == YEAR2.june_solstice

    assert es.summer_solstice_after(DateTime(YEAR1.year, 1, 1), LOC2) == YEAR1.december_solstice
    assert es.summer_solstice_after(YEAR1.december_solstice, LOC2) == YEAR1.december_solstice
    assert es.summer_solstice_after(DateTime(YEAR1.year, 12, 31), LOC2) == YEAR2.december_solstice


def test_summer_solstice_before() -> None:
    assert es.summer_solstice_before(DateTime(YEAR2.year, 1, 1), LOC1) == YEAR1.june_solstice
    assert es.summer_solstice_before(YEAR2.june_solstice, LOC1) == YEAR1.june_solstice
    assert es.summer_solstice_before(DateTime(YEAR2.year, 6, 30), LOC1) == YEAR2.june_solstice

    assert es.summer_solstice_before(DateTime(YEAR2.year, 1, 1), LOC2) == YEAR1.december_solstice
    assert es.summer_solstice_before(YEAR2.december_solstice, LOC2) == YEAR1.december_solstice
    assert es.summer_solstice_before(DateTime(YEAR2.year, 12, 31), LOC2) == YEAR2.december_solstice


def test_fall_equinox_after() -> None:
    assert es.fall_equinox_after(DateTime(YEAR1.year, 1, 1), LOC1) == YEAR1.september_equinox
    assert es.fall_equinox_after(YEAR1.september_equinox, LOC1) == YEAR1.september_equinox
    assert es.fall_equinox_after(DateTime(YEAR1.year, 9, 30), LOC1) == YEAR2.september_equinox

    assert es.fall_equinox_after(DateTime(YEAR1.year, 1, 1), LOC2) == YEAR1.march_equinox
    assert es.fall_equinox_after(YEAR1.march_equinox, LOC2) == YEAR1.march_equinox
    assert es.fall_equinox_after(DateTime(YEAR1.year, 3, 30), LOC2) == YEAR2.march_equinox


def test_fall_equinox_before() -> None:
    assert es.fall_equinox_before(DateTime(YEAR2.year, 1, 1), LOC1) == YEAR1.september_equinox
    assert es.fall_equinox_before(YEAR2.september_equinox, LOC1) == YEAR1.september_equinox
    assert es.fall_equinox_before(DateTime(YEAR2.year, 9, 30), LOC1) == YEAR2.september_equinox

    assert es.fall_equinox_before(DateTime(YEAR2.year, 1, 1), LOC2) == YEAR1.march_equinox
    assert es.fall_equinox_before(YEAR2.march_equinox, LOC2) == YEAR1.march_equinox
    assert es.fall_equinox_before(DateTime(YEAR2.year, 3, 30), LOC2) == YEAR2.march_equinox


def test_winter_solstice_after() -> None:
    assert es.winter_solstice_after(DateTime(YEAR1.year, 1, 1), LOC1) == YEAR1.december_solstice
    assert es.winter_solstice_after(YEAR1.december_solstice, LOC1) == YEAR1.december_solstice
    assert es.winter_solstice_after(DateTime(YEAR1.year, 12, 30), LOC1) == YEAR2.december_solstice

    assert es.winter_solstice_after(DateTime(YEAR1.year, 1, 1), LOC2) == YEAR1.june_solstice
    assert es.winter_solstice_after(YEAR1.june_solstice, LOC2) == YEAR1.june_solstice
    assert es.winter_solstice_after(DateTime(YEAR1.year, 6, 30), LOC2) == YEAR2.june_solstice


def test_winter_solstice_before() -> None:
    assert es.winter_solstice_before(DateTime(YEAR2.year, 1, 1), LOC1) == YEAR1.december_solstice
    assert es.winter_solstice_before(YEAR2.december_solstice, LOC1) == YEAR1.december_solstice
    assert es.winter_solstice_before(DateTime(YEAR2.year, 12, 30), LOC1) == YEAR2.december_solstice

    assert es.winter_solstice_before(DateTime(YEAR2.year, 1, 1), LOC2) == YEAR1.june_solstice
    assert es.winter_solstice_before(YEAR2.june_solstice, LOC2) == YEAR1.june_solstice
    assert es.winter_solstice_before(DateTime(YEAR2.year, 6, 30), LOC2) == YEAR2.june_solstice


def test_nearest_day_at_time_to_datetime() -> None:
    assert es.nearest_day_at_time_to_datetime(Time(6), DateTime(2000, 1, 1, 12, 00)) == DateTime(2000, 1, 1, 6, 0)
    assert es.nearest_day_at_time_to_datetime(Time(6), DateTime(2000, 1, 1, 3, 00)) == DateTime(2000, 1, 1, 6, 0)
    assert es.nearest_day_at_time_to_datetime(Time(6), DateTime(2000, 1, 1, 23, 00)) == DateTime(2000, 1, 2, 6, 0)
    assert es.nearest_day_at_time_to_datetime(Time(23), DateTime(2000, 1, 1, 2, 00)) == DateTime(1999, 12, 31, 23, 0)
