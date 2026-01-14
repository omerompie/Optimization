T_MAX = 39.0

import pandas as pd
import math


df = pd.read_csv('wind_for_coordinates.csv')

"""
for interpolation by time, we have to make tables with time as rows and the coordinates as values for x and y wind
"""

u_table = df.pivot(index='time_hours', columns='waypoint_id', values='u_speed_ms').sort_index() #make a table for the x wind on every hour
v_table = df.pivot(index='time_hours', columns='waypoint_id', values='v_speed_ms').sort_index() #make a table for the y wind on every hour

t_max = T_MAX

def get_wind_kmh(waypoint_id, time, heading):
    t = float(time)
    if t > t_max:
        t = t_max #for the unlikely case that the total time exceeds the t_max. in the algorithm, you get a massive penalty fo exceeding the total time, so this is just to get no errors

    if t in u_table.index: #if t in hours is the same as a time in hours in de list, we don't have to interpolate
        u = float(u_table.at[t, waypoint_id])
        v = float(v_table.at[t, waypoint_id])

    else:



        h0 = math.floor(t) #the value of the nearest time in de table under t
        h1 = h0 + 1.0


        u0 = float(u_table.at[float(h0), waypoint_id])
        v0 = float(v_table.at[float(h0), waypoint_id])
        if h1 > t_max:
            u = u0
            v = v0
        else:
            u1 = float(u_table.at[float(h1), waypoint_id])
            v1 = float(v_table.at[float(h1), waypoint_id]) #get the speeds at h0 and h1

            u = u0 + (t-h0) * ((u1-u0)/(h1-h0))
            v = v0 + (t-h0) * ((v1-v0)/(h1-h0)) #this is linear interpolation

    """
    Now, we calculate the wind speed and direction. first the speed with pythagoras theorem.
    Then, #calculate the direction from which the wind comes.
    arctan 2 gives the angle with the x-axis. and gives the direction. so it gives to where the wind is going
    this has to be converted to from which direction the wind is going.
    if arctan gives 0, the wind GOES to east, because the angle with the x-axis is 0.
    so, to convert it, we must add '270 - outcome_arctan2' to this, so the wind COMES from west
    %360 is to prevent negative angles or angles above 360 degrees.
    """

    speed_ms = math.sqrt(u ** 2 + v ** 2)
    direction = (270 - math.degrees(math.atan2(v, u))) % 360

    # signed angle difference between heading and wind_FROM
    wind_to_deg = (direction + 180) % 360
    diff = (wind_to_deg - heading + 180) % 360 - 180  # berekening wind angle
    head_tail_kmh = speed_ms * 3.6 * math.cos(math.radians(diff))  # berekening wind speed met headwind als negatief component

    return head_tail_kmh
























