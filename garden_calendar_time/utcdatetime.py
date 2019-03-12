from typing import Optional

import datetime

from datetime import date as Date
from datetime import time as Time
from datetime import timedelta as TimeDelta

UTC = datetime.timezone(datetime.timedelta(0))

class UTCTime(datetime.time):
    def __new__(cls, hour: int, minute: int = 0, second: int = 0, microsecond: int = 0) -> 'UTCTime':
        return datetime.time.__new__(cls, hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=UTC)


class UTCDateTime(datetime.datetime):
    def __new__(cls, year: int, month: int, day: int,
                 hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0) -> 'UTCDateTime':
        return datetime.datetime.__new__(cls, year=year, month=month, day=day,
                                          hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=UTC)

    @classmethod
    def _convert(cls, dt: datetime.datetime):
        utc_dt_from_dt = UTCDateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        if dt.tzinfo is not None and dt.tzinfo is not UTC:
            utc_dt_from_dt = utc_dt_from_dt + dt.tzinfo.utcoffset(None)
        return utc_dt_from_dt


    @classmethod
    def now(cls):
        return cls._convert(datetime.datetime.now(tz=UTC))

    @classmethod
    def today(cls):
        return cls.now()

    def __add__(self, other):
        return UTCDateTime._convert(super(UTCDateTime, self).__add__(other))

    def __radd__(self, other):
        return UTCDateTime._convert(super(UTCDateTime, self).__radd__(other))

    def time(self) -> UTCTime:
        return UTCTime(self.hour, self.minute, self.second, self.microsecond)

    @classmethod
    def combine(cls, date: datetime.date, time: datetime.time, tzinfo: Optional[datetime.tzinfo] = ...) -> 'UTCDateTime':
        return cls._convert(datetime.datetime.combine(date, time))

    @classmethod
    def fromtimestamp(cls, timestamp: float, tzinfo: datetime.tzinfo = UTC) -> 'UTCDateTime':
        return cls._convert(datetime.datetime.fromtimestamp(timestamp, tzinfo))