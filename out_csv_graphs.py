import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from wind_turbine import WindTurbine


#USING PANDAS TO OPEN AND READ THE 'out.csv' FILE CONTAINING THE GENERATED SIMULATION DATA, LENGTH: 17522
df = pd.read_csv('out.csv')

#INPUT FOR INDICES OF THE DATA THAT ARE PLOTTED, TIME AXIS, AND 'n' VALUE FOR NUMBER OF CONSECUTIVE VALUES TO BE AVERAGED
time = np.array(list(range(0,17522)))
n = 1
i1 = 0
i2 = 17522

"""Each variable for columns in the dataframe are generally stored in individual variables as arrays. Averages of every 
consecutive 'n' number of values are taken in the 'variable_averages' variable. 
For hourly values of a variable: n = 1, time = (0...17522)
For daily averages of a variable: n = 24, time = (0...730)
For monthly averages of a variable: n = 720, time = (0...24)"""

#FUNCTION TO GET AVERAGE OF A LIST (TO BE USED IN THE BAR GRAPHS OR FOR GENERAL STATISTICS PULLS)
def calc_average(lst):
    return sum(lst) / len(lst)

#NET POWER
net_power = df['NET POWER'][i1:i2]
net_power_averages = [sum(net_power[i:i + n]) / n
          for i in range(len(net_power) - n + 1)]
net_power_graph = net_power_averages[0::n]

"""#TURBINE POWER
turbine_power = df['TURBINE POWER'][i1:i2]
turbine_power_averages = [sum(turbine_power[i:i + n]) / n
          for i in range(len(turbine_power) - n + 1)]
turbine_power_graph = turbine_power_averages[0::n]"""

"""Graphs are plotted in either their own figures or in a figure with closely related graphs. 
Parameters that are set include axis variables, graph title, axis labels, and plot colour.
Scatter plots will have extra lines of code to generate best fit lines."""

#NET POWER VS TIME
fig_1, axes = plt.subplots(1,1,figsize=(30, 10))
axes.plot(time, net_power_graph)
axes.set_title('Variation of Net Power Over Time In Months')
axes.set_xlabel('Time (months)')
axes.set_ylabel('Net Power (W)')
axes.set_ylim([0,10000000])
m, b = np.polyfit(time, net_power_graph, 1)
axes.plot(time, m*time + b)
plt.close()

"""For the CHARGED/DISCHARGED bar graphs values from the 'STATE' column of the 'out.csv' file are first filtered so 
that only CHARGED or DISCHARGED values remain. They are stored in a list in 'number_of_...' as groups. Each group
contains consecutive instances of the desired 'STATE' value.
Even though these groups can be printed out in a table format they are stored as 'str' values, containing a line for 
every row(index) of the desired 'STATE' value and 2 additional lines (blank spaces). So, to get the number of 
consecutive hours in a group (essentially the number of rows) the number of lines ('\n') are counted and the 2 extra 
lines are subtracted. This is done for every group and the final values are stored as a list in 'hours_at_...'."""

#DURATION OF TIME AT WHICH SYSTEM REMAINS CHARGED

state = df['STATE']

number_of_CHARGED = []
for k, v in df[df['STATE'] == 'CHARGED'].groupby((df['STATE'] != 'CHARGED').cumsum()):
    number_of_CHARGED.append(f'[group{v}]')

hours_at_CHARGED = []
for i in range(len(number_of_CHARGED)):
    hours_at_CHARGED.append(number_of_CHARGED[i].count('\n') - 2)

average_CHARGED = str(round(calc_average(hours_at_CHARGED), 1))
median_CHARGED = np.median(hours_at_CHARGED)
number_of_instances_CHARGED = len(hours_at_CHARGED)
max_CHARGED = max(hours_at_CHARGED)

fig_3, axes = plt.subplots(1,1,figsize=(30, 10))
axes.bar(range(0,number_of_instances_CHARGED), hours_at_CHARGED, color='seagreen')
axes.set_title('Number of Consecutive Hours Spent At Charged State - 16000 Blocks')
axes.set_xlabel('Instance')
axes.set_ylabel('Time (h)')
axes.set_ylim([0, max_CHARGED + 1])
axes.text(8, 50, r'Median of ' + str(median_CHARGED) + ' hours', fontsize=12)
plt.show()

#DURATION OF TIME AT WHICH SYSTEM REMAINS DISCHARGED
number_of_DISCHARGED = []
for k, v in df[df['STATE'] == 'DISCHARGED'].groupby((df['STATE'] != 'DISCHARGED').cumsum()):
    number_of_DISCHARGED.append(f'[group{v}]')

hours_at_DISCHARGED = []
for i in range(len(number_of_DISCHARGED)):
    hours_at_DISCHARGED.append(number_of_DISCHARGED[i].count('\n') - 2)

average_DISCHARGED = str(round(calc_average(hours_at_DISCHARGED), 1))
median_DISCHARGED = np.median(hours_at_DISCHARGED)
number_of_instances_DISCHARGED = len(hours_at_DISCHARGED)
max_DISCHARGED = max(hours_at_DISCHARGED)

fig_4, axes = plt.subplots(1,1,figsize=(30, 10))
axes.bar(range(0,number_of_instances_DISCHARGED), hours_at_DISCHARGED, color='firebrick')
axes.set_title('Number of Consecutive Hours Spent At Discharged State - 16000 Blocks')
axes.set_xlabel('Instance')
axes.set_ylabel('Time (h)')
axes.set_ylim([0, max_DISCHARGED + 1])
axes.text(0, 55, r'Median of ' + str(median_DISCHARGED) + ' hours', fontsize=12)
plt.close()

#IDEAL SITUATION - WIND TURBINE POWER IN 4-5 MW RANGE (INDEX 95999-9623 or 14175-14187)
fig_5, axes = plt.subplots(1,1,figsize=(14, 7))
axes.scatter(time, net_power_graph)
axes.set_title('Net Power Over Time In Hours')
axes.set_xlabel('Time (hours)')
axes.set_ylabel('Net Power (W)')
axes.set_ylim([0,9000000])
m, b = np.polyfit(time, net_power_graph, 1)
axes.plot(time, m*time + b)
plt.close()

#IDEAL SITUATION - WIND TURBINE POWER IN 2-3 MW RANGE (INDEX 720-732, or 118-130)
fig_6, axes = plt.subplots(1,1,figsize=(14, 7))
axes.scatter(time, net_power_graph)
axes.set_title('Net Power Over Time In Hours')
axes.set_xlabel('Time (hours)')
axes.set_ylabel('Net Power (W)')
axes.set_ylim([0,9000000])
m, b = np.polyfit(time, net_power_graph, 1)
axes.plot(time, m*time + b)
plt.close()

#RANDOM EDGE CASES
fig_7, axes = plt.subplots(1,1,figsize=(30, 10))
axes.plot(time, net_power_graph)
axes.set_title('Random Sample of Net Power Over Time In Hours')
axes.set_xlabel('Time (hours)')
axes.set_ylabel('Net Power (W)')
axes.set_ylim([0,9000000])
m, b = np.polyfit(time, net_power_graph, 1)
axes.plot(time, m*time + b)
plt.close()


