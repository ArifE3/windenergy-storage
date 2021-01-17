import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from wind_turbine import WindTurbine
from wind_turbine import calc_air_density


#USING PANDAS TO OPEN AND READ THE 'inp.csv' FILE CONTAINING THE KNMI DATA, LENGTH: 17522
ds = pd.read_csv('inp.csv')

#INPUT FOR INDICES OF THE DATA THAT ARE PLOTTED, TIME AXIS, AND 'n' VALUE FOR NUMBER OF CONSECUTIVE VALUES TO BE AVERAGED
time = list(range(0,24))
n = 1
i1 = 4543
i2 = 4567

"""Each variable for columns in the dataframe are generally stored in individual variables as arrays. Averages of every 
consecutive 'n' number of values are taken in the 'variable_averages' variable. 
For hourly values of a variable: n = 1, time = (0...17522)
For daily averages of a variable: n = 24, time = (0...730)
For monthly averages of a variable: n = 720, time = (0...24)"""

#WIND SPEED
wind_speed_float64 = np.array(ds['WIND SPEED'][i1:i2], dtype=np.float64)
wind_speed = wind_speed_float64.astype(np.int)
wind_speed_averages = [sum(wind_speed[i:i + n]) / n
          for i in range(len(wind_speed) - n + 1)]
wind_speed_graph = wind_speed_averages[0::n]

#AIR PRESSURE
air_pressure = ds['AIR PRESSURE'][i1:i2]
air_pressure_averages = [sum(air_pressure[i:i + n]) / n
          for i in range(len(air_pressure) - n + 1)]
air_pressure_graph = air_pressure_averages[0::n]

#AIR TEMPERATURE
air_temperature = ds['TEMPERATURE'][i1:i2]
air_temperature_averages = [sum(air_temperature[i:i + n]) / n
          for i in range(len(air_temperature) - n + 1)]
air_temperature_graph = air_temperature_averages[0::n]

#RELATIVE HUMIDITY
relative_humidity = ds['RELATIVE HUMIDITY'][i1:i2]
relative_humidity_averages = [sum(relative_humidity[i:i + n]) / n
          for i in range(len(relative_humidity) - n + 1)]
relative_humidity_graph = relative_humidity_averages[0::n]

#DATA FROM "wind_turbine.py"
turbine = WindTurbine('SG', height=167, swept_area=21900)

#AIR DENSITY (with functions from 'wind_turbine.py')
air_density = []
for i in range(len(time)):
    air_density.append(calc_air_density(air_pressure_graph[i], air_temperature_graph[i], relative_humidity_graph[i]))

#POWER (with functions from 'wind_turbine.py')
power = []
for i in range(len(time)):
    power.append(turbine.calc_wind_turbine_power(air_pressure_graph[i], air_temperature_graph[i], relative_humidity_graph[i], wind_speed[i]))

"""Graphs are plotted in either their own figures or in a figure with closely related graphs. 
Parameters that are set include axis variables, graph title, axis labels, and plot colour."""

#WIND SPEED VS TIME
fig_1, axes = plt.subplots(1,1,figsize=(30, 10))
axes.plot(time, wind_speed_graph)
axes.set_title('Variation of Wind Speeds Over Time In Hours')
axes.set_xlabel('Time (hours)')
axes.set_ylabel('Wind speed (m/s)')

#POWER VS TIME
fig_3, axes = plt.subplots(1,1,figsize=(30, 10))
axes.plot(time, power)
axes.set_title('Variation of Power Generated Over Time In Hours')
axes.set_xlabel('Time (hours)')
axes.set_ylabel('Power ($W$)')
plt.show()
