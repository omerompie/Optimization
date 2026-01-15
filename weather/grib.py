from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


from weather.coordinates import build_graph
nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

"""
first, we create a latitude and longitude list for all out waypoints that can be used by xarray
"""
point_ids = sorted(node_coords.keys())
points = [node_coords[nid] for nid in point_ids]
lat_list = [lat for (lat, lon) in points]
lon_list = [lon for (lat, lon) in points]


lats = xr.DataArray(lat_list, dims="point")
lons = xr.DataArray(lon_list, dims="point")

"""
Next, we want to create a dataframe for every grib 2 file. 
every file contains the weather information for coordinates at a specific time.
we want weather direction and speed for every waypoint at given times.
"""

def get_wind_from_grib(grib_path):

    ds = xr.open_dataset(grib_path, engine = 'cfgrib', backend_kwargs = {'indexpath': ''}) #open the grib file with cfgrib and ensure that the engine writes the indices inside the grib

    ds = ds.sortby('latitude')
    ds = ds.sortby('longitude') #for the bilinear interpolation the values should be ascending

    u = ds['u'] #wind from west to east
    v = ds['v'] #wind from south to north

    valid_time = pd.Timestamp(ds['valid_time'].values) #to create a timestamp. later used to assign a time to the coordinates and wind condtions


    u_wp = u.interp(latitude=lats, longitude=lons, method='linear') #interpolate the west to east wind at every waypoint
    v_wp = v.interp(latitude=lats, longitude=lons, method='linear') #interpolate the south to north wind at every waypoint


    """
    Lastly, we are going to make the dataframe
    """

    df = pd.DataFrame({
        'waypoint_id': point_ids,
        'latitude': lat_list,
        'longitude': lon_list,
        'u_speed_ms': u_wp,
        'v_speed_ms': v_wp,
        'time': valid_time
    })
    return df

"""
Now we have the function to make the dataframe, we have to do this for all our grib2 files.
we also have to merge the dataframes with a new column named time. so we have our coordinates 
with all our values for a given time.
"""

location = Path(__file__).resolve().parent #help call the grib2 files with Path library

files = [ #make a list for all our GRIB2 files
    "gfs.t18z.pgrb2.0p25.f000", #weather at t = 0
    "gfs.t18z.pgrb2.0p25.f001",
    "gfs.t18z.pgrb2.0p25.f002",
    "gfs.t18z.pgrb2.0p25.f003",
    "gfs.t18z.pgrb2.0p25.f004",
    "gfs.t18z.pgrb2.0p25.f005",
    "gfs.t18z.pgrb2.0p25.f006",
    "gfs.t18z.pgrb2.0p25.f007",
    "gfs.t18z.pgrb2.0p25.f008",
    "gfs.t18z.pgrb2.0p25.f009", #weather at t = 9 hours after start
    "gfs.t18z.pgrb2.0p25.f009",
    "gfs.t18z.pgrb2.0p25.f010",
    "gfs.t18z.pgrb2.0p25.f011",
    "gfs.t18z.pgrb2.0p25.f012",
    "gfs.t18z.pgrb2.0p25.f013",
    "gfs.t18z.pgrb2.0p25.f014",
    "gfs.t18z.pgrb2.0p25.f015",
    "gfs.t18z.pgrb2.0p25.f016",
    "gfs.t18z.pgrb2.0p25.f017",
    "gfs.t18z.pgrb2.0p25.f018",
    "gfs.t18z.pgrb2.0p25.f019",
    "gfs.t18z.pgrb2.0p25.f020",
    "gfs.t18z.pgrb2.0p25.f021",
    "gfs.t18z.pgrb2.0p25.f022",
    "gfs.t18z.pgrb2.0p25.f023",
    "gfs.t18z.pgrb2.0p25.f024",
    "gfs.t18z.pgrb2.0p25.f025",
    "gfs.t18z.pgrb2.0p25.f026",
    "gfs.t18z.pgrb2.0p25.f027",
    "gfs.t18z.pgrb2.0p25.f028",
    "gfs.t18z.pgrb2.0p25.f029",
    "gfs.t18z.pgrb2.0p25.f030",
    "gfs.t18z.pgrb2.0p25.f031",
    "gfs.t18z.pgrb2.0p25.f032",
    "gfs.t18z.pgrb2.0p25.f033",
    "gfs.t18z.pgrb2.0p25.f034",
    "gfs.t18z.pgrb2.0p25.f035",
    "gfs.t18z.pgrb2.0p25.f036",
    "gfs.t18z.pgrb2.0p25.f037",
    "gfs.t18z.pgrb2.0p25.f038",
    "gfs.t18z.pgrb2.0p25.f039",
]

dataframes = {} #make a dictionary with the files as key and dataframe as values

for name in files:
    path = location / name #for reading the grib2 file in the next statement
    df_name = get_wind_from_grib(path) #create all the dataframes
    dataframes[name] = df_name #put all the dataframes in the dictionary

whole_dataframe = pd.concat(list(dataframes.values()), ignore_index=True) #make 1 big dataframe for all grib files
whole_dataframe = whole_dataframe.sort_values(['time', 'waypoint_id']).reset_index(drop = True) #sort so that the time is ascending for each waypoint id

"""
the last step is to make a column with the time in hours. 
because the calculate edge costs function uses total flight time, 
the UTC time cannot be used. 
we have to create the start time first, which is the first timestamp in the dataframe.
"""

t0 = whole_dataframe['time'].min()

whole_dataframe['time_hours'] = (whole_dataframe['time'] - t0) / pd.Timedelta(hours = 1) #make a new column which shows the total flight time that corresponds with the timestamp. and creates a float

whole_dataframe.to_csv('wind_for_coordinates.csv', index = False)





























