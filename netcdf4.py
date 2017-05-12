# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:37:05 2017

@author: dids
"""

from netCDF4 import Dataset
import pandas as pd
import numpy as np

rootgrp=Dataset('text.nc', 'w', format='NETCDF4')

fcstgrp = rootgrp.createGroup('forecasts')
analgrp = rootgrp.createGroup('analyses')
fcstgrp1 = rootgrp.createGroup('/forecasts/model1')

time = rootgrp.createDimension('time', None)
lat = rootgrp.createDimension('lat', 2)
lon = rootgrp.createDimension('lon', 2)

times = rootgrp.createVariable('time','f8',('time',))
times.units = 'hours since 0001-01-01 00:00:00.0'
times.calendar = 'gregorian'
latitudes = rootgrp.createVariable('lat','f4',('lat',))
longitudes = rootgrp.createVariable('lon','f4',('lon',))
heights=rootgrp.createVariable('hght', 'f4', ('lat','lon',))
river=rootgrp.createVariable('riv','f4',('time','lat','lon'))
weather=rootgrp.createVariable('wthr','f4',('time','lat','lon'))

print(times.shape, latitudes.shape, longitudes.shape, time.group)
rootgrp.weather=np.random.uniform(low=-1, high=1, size=24)

from datetime import datetime, timedelta
from netCDF4 import num2date, date2num, date2index
dates = [datetime(2001,3,1)+n*timedelta(hours=12) for n in range(324)]
times[:] = date2num(dates,units=times.units,calendar=times.calendar)
print('time values (in units %s): ' % times.units+'\\n',times[0:10])
dates = num2date(times[:],units=times.units,calendar=times.calendar)
print('corresponding dates:',dates[0:10])
dates_pd=pd.to_datetime(dates)
print('corresponding padas dates:',dates_pd[0:10])
periods=dates_pd.to_period(freq='12H')


test=pd.DataFrame(rootgrp.variables['riv'][:,0], index=rootgrp.variables['time'])
rootgrp.close()