import logging
import datetime
import re
import zoneinfo
import astral
from astral.sun import sun


UTC_TIME_ZONE: zoneinfo.ZoneInfo = zoneinfo.ZoneInfo('UTC')

logger = logging.getLogger(__name__)


class Time:
    def __init__(self, timezone: str, latitude: float, longitude: float,
                 on_date: str | datetime.datetime | None = None):
        try:
            self.timezone = zoneinfo.ZoneInfo(timezone)
        except Exception as exp_timezone:
            self.timezone = timezone
            logger.exception(f'Error: {exp_timezone}')
        self.latitude = latitude
        self.longitude = longitude
        if isinstance(on_date, datetime.datetime):
            self.on_date = on_date
        elif isinstance(on_date, str):
            if regex := re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', on_date):
                self.on_date = datetime.datetime.strptime(regex.group(0), '%Y-%m-%dT%H:%M')
            elif regex := re.search(r'\d{4}-\d{2}-\d{2}', on_date):
                self.on_date = datetime.datetime.strptime(regex.group(0), '%Y-%m-%d')
            else:
                raise ValueError('on_date date format is invalid')
        else:
            self.on_date = None

    def utc_offset(self) -> dict:
        if not isinstance(self.timezone, zoneinfo.ZoneInfo):
            return {'hours': None, 'minutes': None, 'repr': None}
        else:
            if self.on_date:
                utc_offset = self.on_date.replace(tzinfo=self.timezone).strftime("%z")
            else:
                utc_offset = datetime.datetime.now(tz=self.timezone).strftime("%z")
            utc_offset = 'UTC' + utc_offset[:-2] + ':' + utc_offset[-2:]
        return {'hours': utc_offset[:-2], 'minutes': utc_offset[-2:], 'repr': utc_offset}

    def get_sunrise(self) -> str:
        return self.get_sun_time(True)

    def get_sunset(self) -> str:
        return self.get_sun_time(False)

    def get_current_utc(self) -> list[int]:
        now = self.on_date if self.on_date else datetime.datetime.now(tz=UTC_TIME_ZONE)
        return [now.day, now.month, now.year]

    def get_sun_time(self, is_sunrise: bool) -> str:
        """ Method to get sunrise and sunset time by latitude and longitude, timezone

        :param is_sunrise:

        :return: if is_sunrise == True, returns sunrise time, else returns sunset
                time in format (example: 08:34-"%H:%M")
        """
        day, month, year = self.get_current_utc()
        try:
            location = astral.LocationInfo("", "", self.timezone, self.latitude, self.longitude)
            sun_time_information = sun(location.observer, datetime.date(year, month, day), tzinfo=self.timezone)
            if is_sunrise:
                return sun_time_information["sunrise"].strftime("%H:%M")
            else:
                return sun_time_information["sunset"].strftime("%H:%M")
        except Exception as e:
            logger.exception(f'Error getting {"sunrise" if is_sunrise else "sunset"}, for timezone - {self.timezone}, '
                             f'error message: {e}')
            return '00:00'
