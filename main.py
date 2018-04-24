import pandas as pd
import numpy as np
import flask
import datetime


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
        now = datetime.datetime.now()
        a_minute_ago = now - datetime.timedelta(minutes=1)
        mask = (self.data[self._col('ts')] > a_minute_ago) & (self.data[self._col('ts')] <= now)
        return self.data.loc[mask][self._col('int')].median()


class MedianService(object):
    pass

if __name__ == "__main__":
    # TODO: flask server
    pass