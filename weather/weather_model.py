T_MAX = 39.0 #we have data for wind 39.0 hours after 1-13-2026 18.00 UTC.

import pandas as pd
import math
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
csv_path = project_root / 'weather' / 'wind_for_coordinates.csv' #again, this so that i dont have to copypaste CSVs later in other directories
df = pd.read_csv(csv_path) #read the wind data

"""
for interpolation by time, we have to make tables with time as rows and the coordinates as values for u and v wind
"""

u_table = df.pivot(index='time_hours', columns='waypoint_id', values='u_speed_ms').sort_index() #make a table for the x wind on every hour
v_table = df.pivot(index='time_hours', columns='waypoint_id', values='v_speed_ms').sort_index() #make a table for the y wind on every hour

t_max = T_MAX


def get_wind_kmh(waypoint_id, time, heading): #make a function to determine wind
    t = float(time) #we work with floats, so making sure everything is in a float
    if t > t_max:
        t = t_max #for the unlikely case that the total time exceeds the t_max. but if so, the weather at that time is equal to t_max weather

    if t in u_table.index: #if t in hours is the same as a time in hours in de list, we don't have to interpolate
        u = float(u_table.at[t, waypoint_id]) #look up in the table the u speed for that t and waypoint id
        v = float(v_table.at[t, waypoint_id]) #look up in the table the v speed for that t and waypoint id

    #now the interpolation begins.

    else:
        h0 = math.floor(t) #the value of the nearest time in the table under t
        h1 = h0 + 1.0 #because we have a time resolution of 1 hour. thee nearest timestamp above t is h0 + 1.0


        u0 = float(u_table.at[float(h0), waypoint_id]) #find the u speed for h0 and that waypoint id
        v0 = float(v_table.at[float(h0), waypoint_id]) #find te v speed for h0 and that waypoint id
        if h1 > t_max: #only the case if t == t_max
            u = u0
            v = v0
        else:
            u1 = float(u_table.at[float(h1), waypoint_id]) #find the u speed for h1 and that waypoint id
            v1 = float(v_table.at[float(h1), waypoint_id]) #find the u speed for h1 and that waypoint id

            u = u0 + (t-h0) * ((u1-u0)/(h1-h0))
            v = v0 + (t-h0) * ((v1-v0)/(h1-h0)) #this is linear interpolation

    """
    Now, we calculate the wind speed and direction. first the speed with pythagoras theorem.
    Then, calculate the direction where  the wind goes to.
    arctan 2 gives the angle with the x-axis. So if the wind is going east, it gives 0. 
    this has to be converted to 
    """

    speed_ms = math.sqrt(u ** 2 + v ** 2) #wind speed
    wind_to_deg = (90 - math.degrees(math.atan2(v, u))) % 360 #calculate where the wind is going, not from


    diff = (wind_to_deg - heading + 180) % 360 - 180  #wind angle between aircraft heading and wind
    head_tail_kmh = speed_ms * 3.6 * math.cos(math.radians(diff))  #calculating head or tail wind. if it is a tail wind. it gives a positive number. if it is a headwind, a negative one

    return head_tail_kmh #retun the head or tail wind

























