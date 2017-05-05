# -*- coding: utf-8 -*-
"""
Created on Fri May  5
Last update: 05/05/2017 17:28
Version: v0.01

@author: jurczynskim
"""

import pandas as pd
import numpy as np

class WeatherFrame(pd.DataFrame):
    """
    Pandas DataFrame with weather forecasting columns
    River: only initial river matters (to add: random propagation of rivers?)
    Weather: column of random numbers (propagation of weathers?)
    Height: one number (height doesn't change), IS NOT a column of DataFrame
    rng: date range
    x,y: coordinates in grid, probably will be useful later
    """
    def __init__(self, river=10,
                 weather=10*np.random.rand(len(rng)),
                 height=10*np.random.rand(1)[0],\
                 rng=pd.date_range('1/1/2017', periods=24, freq='H'),\
                 x=0,y=0):
        super(WeatherFrame, self).__init__(index=rng)
        self['river']=0
        self['river'].iloc[0]=river
        self['weather']=weather
        self.height=height
        self.rng=rng
        
    def set_initial_river(self, river):
        self['river'].iloc[0]=river
    
    def set_river(self, river):
        self['river']=river

    def set_weather(self, weather):
        self['weather']=weather
        
    def set_height(self, height):
        self.height=height

    def timesteps(self):
        for timestep in self.index:
            yield timestep
            
        
class GridFrame(list):
    """
    Grid of Weather Frames
    cf. Weather Frame
    """
    def __init__(self, x=1,y=1, river=10,\
                 weather=10*np.random.rand(len(rng)),\
                 height=10*np.random.rand(1)[0],\
                 rng=pd.date_range('1/1/2017',periods=24,freq='H')):
        super(list, self).__init__()
        self.rng=rng
        self.x=x
        self.y=y
        for j in range(y):
            self.append([WeatherFrame(river, weather, height,rng,i,j)\
                         for i in range(x)]) 
            
    def timesteps(self):
        """
        An iterable over the timesteps across the entire Grid
        """
        for timestep in self.rng:
            yield timestep
            
    def lower_neighbours(self, x, y):
        """
        Function to find neighbours at a lower 
        height than at current position in the Grid
        """
        nhb=[]
        indices=[]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if x+i in range(self.x) and y+j in range(self.y) and\
                   self[x][y].height>self[x+i][y+j].height and i*j==0:
                    nhb.append(self[x+i][y+j])
                    indices.append((x+i, y+j))
        return nhb, indices
            
    def progress_rivers(self):
        """
        Rivers flow at a rate of difference of heights to 
        orthogonally adjacent grids of lower height
        The value of 'weather' at previous timestep gets added 
        to the value of 'river' 
        *.loc used to avoid SettingWithCopy pandas error
        Currently fully deterministic
        """
        for timestep in self.rng[1:]:
            for i in range(self.x):
                for j in range(self.y):
                    self[i][j].loc[timestep,'river']=\
                                self[i][j].loc[timestep-1, 'river']
                    for neighbour in self.lower_neighbours(i,j)[0]:
                        delta=self[i][j].height-neighbour.height
                        if self[i][j]['river'][timestep]>=delta:
                            self[i][j].loc[timestep,'river']-=delta
                            neighbour.loc[timestep,'river']=\
                                neighbour.loc[timestep-1,'river']+delta
                    self[i][j].loc[timestep, 'river']+=\
                                self[i][j]['weather'][timestep-1]

    
    """
    TO ADD:
         - methods to initialise a grid of variables across the entire grid
         - more complicated topography rather than "height" (slope directions)
         - more than one river in a grid?
         - progress_weathers?
         - modify progress_rivers to allow some randomness
         - method to display the grid at a timepoint (__str__)
    """

#A test run                            
x=GridFrame(x=2,y=2)
for i in range(len(x)):
    for j in range(len(x[i])):
        x[i][j].set_initial_river(12)
        x[i][j].set_height(1)
        x[i][j]['weather']=0
x[0][1].height=0 #This ensures all rivers flow to x[0][1] and no weather

x.progress_rivers()
import matplotlib as plt

x[0][1]['river'].plot() #Everything flows here!