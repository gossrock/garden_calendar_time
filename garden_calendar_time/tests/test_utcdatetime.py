import pytest

from datetime import datetime, timezone, timedelta, date, time
from garden_calendar_time.utcdatetime import UTCDateTime, UTCTime


UTC = timezone(timedelta(0))

time_inputs = [{'hour': 1},
               {'hour': 2, 'minute': 3, 'second':4, 'microsecond': 5},
               {'hour': 23, 'minute': 59, 'second': 59, 'microsecond': 999999},
               {'hour': 12, 'minute': 30},
               {'hour': 0},
               {'hour': 6, 'minute': 15, 'second': 42}]

date_time_inputs = [{'year':2000, 'month':1, 'day':1},
                    {'year':2000, 'month':1, 'day':2, 'hour':3, 'minute':4, 'second':5, 'microsecond':5},
                    {'year':2000, 'month':1, 'day':31, 'hour':23, 'minute':59, 'second':59, 'microsecond':999999},
                    {'year':2000, 'month':12, 'day':31, 'hour':3, 'minute':4, 'second':5, 'microsecond':5}]

@pytest.mark.parametrize("initialization_data", time_inputs)
def test_UTCTime_init(initialization_data) -> None:
    test1 = UTCTime(**initialization_data)
    assert test1.tzinfo == UTC
    assert test1.hour == initialization_data['hour']
    if 'minute' in initialization_data:
        assert test1.minute == initialization_data['minute']
    else:
        assert test1.minute == 0
    if 'second' in initialization_data:
        assert test1.second == initialization_data['second']
    else:
        assert test1.second == 0
    if 'microsecond' in initialization_data:
        assert test1.microsecond == initialization_data['microsecond']
    else:
        assert test1.microsecond == 0


@pytest.mark.parametrize("initialization_data", date_time_inputs)
def test_UTCDateTime_init(initialization_data) -> None:
    test1 = UTCDateTime(**initialization_data)
    assert test1.tzinfo == UTC
    assert test1.year == initialization_data['year']
    assert test1.month == initialization_data['month']
    assert test1.day == initialization_data['day']
    if 'hour' in initialization_data:
        assert test1.hour == initialization_data['hour']
    else:
        assert test1.hour == 0
    if 'minute' in initialization_data:
        assert test1.minute == initialization_data['minute']
    else:
        assert test1.minute == 0
    if 'second' in initialization_data:
        assert test1.second == initialization_data['second']
    else:
        assert test1.second == 0
    if 'microsecond' in initialization_data:
        assert test1.microsecond == initialization_data['microsecond']
    else:
        assert test1.microsecond == 0

def test_TUCDateTime_now() -> None:
    assert UTCDateTime.now().tzinfo == UTC

def test_UTCDateTime_today() -> None:
    assert UTCDateTime.today().tzinfo == UTC

@pytest.mark.parametrize("initialization_data", date_time_inputs)
def test_UTCDateTime_add(initialization_data) -> None:
    utc_datetime = UTCDateTime(**initialization_data)
    td = timedelta(days=1)
    result = utc_datetime + td

    assert type(result) == UTCDateTime

    day_incremented = result.day == utc_datetime.day + 1
    month_incremented = result.month == utc_datetime.month + 1
    year_incremented = result.year == utc_datetime.year + 1

    assert day_incremented + month_incremented + year_incremented == 1

@pytest.mark.parametrize("initialization_data", date_time_inputs)
def test_UTCDateTime_time(initialization_data):
    utc_datetime = UTCDateTime(**initialization_data)
    id = initialization_data
    hour = 0
    minute = 0
    second = 0
    microsecond = 0
    if 'hour' in id: hour = id['hour']
    if 'minute' in id: minute = id['minute']
    if 'second' in id: second = id['second']
    if 'microsecond' in id: microsecond = id['microsecond']
    utc_time = UTCTime(hour, minute, second, microsecond)
    assert utc_datetime.time() == utc_time
    assert type(utc_datetime.time()) == UTCTime
    assert utc_datetime.time().tzinfo == UTC

@pytest.mark.parametrize("initialization_data", date_time_inputs)
def test_UTCDateTime_combine(initialization_data):
    utc_datetime = UTCDateTime(**initialization_data)
    year = initialization_data['year']
    month = initialization_data['month']
    day = initialization_data['day']
    date_ = date(year, month, day)
    hour = 0
    minute = 0
    second = 0
    microsecond = 0
    id = initialization_data
    if 'hour' in id:
        hour = id['hour']
    if 'minute' in id: minute = id['minute']
    if 'second' in id: second = id['second']
    if 'microsecond' in id: microsecond = id['microsecond']

    time_ = time(hour, minute, second, microsecond)
    utctime = UTCTime(hour, minute, second, microsecond)
    assert UTCDateTime.combine(date_, time_) == utc_datetime
    assert UTCDateTime.combine(date_, utctime) == utc_datetime

