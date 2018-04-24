import datetime

import pandas as pd
import numpy as np
from flask import Flask, request
from flask_autodoc.autodoc import Autodoc



class MedianData(object):

    columns = ['ts', 'int']

    def __init__(self):
        self.data = pd.DataFrame(columns=self.columns)
        self.data.ts = pd.to_datetime(self.data.ts)

    def _col(self, which):
        return self.columns.index(which)

    def put_integer(self, value):
        self.data = pd.DataFrame(
            np.insert(self.data.values, len(self.data.values), 
            values=[datetime.datetime.now(), value], 
            axis=0)
        )

    def get_median_last_min(self):
        result = None
        try:
            now = datetime.datetime.now()
            a_minute_ago = now - datetime.timedelta(minutes=1)
            mask = (self.data[self._col('ts')] > a_minute_ago) & (self.data[self._col('ts')] <= now)
            result = self.data.loc[mask][self._col('int')].median()
        except:
            pass
        return result

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


service = Flask(__name__)
service_auto = Autodoc(service)
data = MedianData()


@service.route('/')
@service.route('/documentation')
def documentation():
    return service_auto.html()

@service.route('/put', methods=['POST'])
@service_auto.doc()
def put_integer():
    """
    takes any integer
    """
    try: 
        value = np.int('%s' % request.get_data())
        data.put_integer(value)
        return ""
    except:
        return InvalidUsage("Invalid input.")

@service.route('/median', methods=['GET'])
@service_auto.doc()
def median():
    """
    returns the median for all the values for the last minute. 
    """
    median = data.get_median_last_min()
    return "No data yet." if not median else '%s' % median

if __name__ == "__main__": 
    service.run(port=5005)