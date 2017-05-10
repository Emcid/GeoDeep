# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:37:05 2017

@author: dids
"""

from netCDF4 import Dataset

rootgrp=Dataset('text.nc', 'w', format='NETCDF4')

fcstgrp = rootgrp.createGroup('forecasts')
analgrp = rootgrp.createGroup('analyses')
fcstgrp1 = rootgrp.createGroup('/forecasts/model1')

time = rootgrp.createDimension('time', None)
lat = rootgrp.createDimension('lat', 2)
lon = rootgrp.createDimension('lon', 2)

times = rootgrp.createVariable('time','f8',('time',))
latitudes = rootgrp.createVariable('lat','f4',('lat',))
longitudes = rootgrp.createVariable('lon','f4',('lon',))
heights=rootgrp.createVariable('hght', 'f4', ('lat','lon',))
river=rootgrp.createVariable('riv','f4',('time','lat','lon'))
weather=rootgrp.createVariable('wthr','f4',('time','lat','lon'))

print(times.shape, latitudes.shape, longitudes.shape)
rootgrp.close()