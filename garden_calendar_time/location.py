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