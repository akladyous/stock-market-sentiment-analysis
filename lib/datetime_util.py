import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class DateTime_Validator(object):
    def __init__(self, start_date, end_date):
        # Date in US format
        self._us_fmt = "%m-%d-%Y"
        # Date in ISO-8601 format
        self._date_regx = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        self._date_len  = len("YYYY-MM-DD")
        self._date_fmt  = "%Y-%m-%d"
        # Datetime in ISO-8601 format
        self._datetime_regx = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')
        self._datetime_len  = len("YYYY-MM-DDTHH:MM:SS")
        self._datetime_fmt  = "%Y-%m-%dT%H:%M:%S"

        self._start_date = self.validate_date(start_date)
        self._end_date   = self.validate_date(end_date)
        DateTime_Validator._check_delta_dates(self._start_date, self._end_date)
        self.start_date  = start_date
        self.end_date    = end_date

    def validate_date(self, dt_str):
        if DateTime_Validator._validate_string(dt_str):
            if len(dt_str) == self._date_len:
                if self._validate_date_fmt(dt_str):
                    return datetime.strptime(dt_str, self._date_fmt)
            elif len(dt_str) == self._datetime_len:
                if self._validate_datetime_fmt(dt_str):
                    return datetime.strptime(dt_str, self._datetime_fmt)
            else:
                raise ValueError("Format Error: date should be formated eighter YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")
            return True
        else:
            raise ValueError("Date imput should be in string format")

    def convert_2_us_fmt(self, date):
        """
        convert datetime STR object from ISO-8601 format to US format.
        """
        return self.validate_date(date).strftime(self._us_fmt)

    def get_date_range(self, step=7, date_format='ISO-8601'):
        diff_days = (self._end_date - self._start_date).days
        date_chunk = []
        if diff_days // step >= 2:
            step = timedelta(step)
            dt = self._start_date.date() - step
            while (self._end_date.date() - dt ).days >= 7 :
                dt += step
                date_chunk.append(dt)
        else:
            date_chunk.extend([self._start_date, self._end_date])

        for idx, dt in enumerate(date_chunk):
            if date_format == 'ISO-8601':
                date_chunk[idx]=dt.strftime(self._date_fmt)
            elif date_format == 'US':
                date_chunk[idx]=dt.strftime(self._us_fmt)
            else:
                raise ValueError("date_format should be eighter US or 'ISO-8601'")
        return date_chunk

    @staticmethod
    def _validate_string(string):
        if isinstance(string, str):
            return True
        else:
            return False
    def _validate_date_fmt(self, date_str):
        if not self._date_regx.match(date_str):
            raise ValueError("Incorrect data format. Date input should be in format of YYYY-MM-DD")
        else:
            return True
    def _validate_datetime_fmt(self, datetime_str):
        if not self._datetime_regx.match(datetime_str):
            raise ValueError("Incorrect data format. Date input should be in format of YYYY-MM-DDTHH:MM:SS")
        else:
            return True

    # assert start date not older than 2 year
    @staticmethod
    def _check_delta_dates(start_date, end_date):
        if start_date > end_date:
            raise Exception("Start_Date is older than End_Date")
        if (start_date <= (datetime.now() - relativedelta(years=3))) :
            raise Exception("Start_Date shouldn't be older than 2 year")

def timestamp2datetime(value):
    """convert Epoch & Unix Timestamp  to datetime object"""
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

def datetime2timestamp(value):
    """convert datetime object to Epoch & Unix TimeStamp"""
    return int(datetime.timestamp(datetime.fromisoformat(value)))

def str2datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def str2date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')
