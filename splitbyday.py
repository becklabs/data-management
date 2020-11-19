import pandas as pd
import os
import dateparser
import pytz
import datetime

def trackExtract(gps_filename):
    ext = gps_filename.split('.')
    if ext[1] == 'csv':
        gps_telem = pd.read_csv(gps_filename)
        if 'esrignss_latitude' in list(gps_telem.columns):
            gps_telem = gps_telem.rename(columns={'esrignss_latitude': 'latitude', 'esrignss_longitude': 'longitude','esrignss_altitude':'elevation','esrignss_fixdatetime':'timestamp'})
            gps_telem1 = pd.DataFrame()
            gps_telem1['latitude'] = gps_telem['latitude']
            gps_telem1['longitude'] = gps_telem['longitude']
            gps_telem1['elevation'] = gps_telem['elevation']
            gps_telem1['timestamp'] = gps_telem['timestamp']
            gps_telem = gps_telem1
        if 'lat' in list(gps_telem.columns):
            gps_telem = gps_telem.rename(columns={'lat': 'latitude', 'lon': 'longitude','ele':'elevation','time':'timestamp'})
        i = 0
        for timestamp in gps_telem['timestamp']:
            gps_telem.loc[i,'timestamp'] = dateparser.parse(gps_telem.loc[i,'timestamp']).replace(tzinfo=pytz.UTC)
            i+=1
        i = 0
        for ts in gps_telem['timestamp']:
           gps_telem.loc[i,'timestamp'] = dateparser.parse(str(ts.year)+' '+str(ts.month)+' '+str(ts.day))
           i+=1
    return gps_telem

def split_by_day(csv):
    df = trackExtract(csv)
    daylist = []
    for timestamp in df['timestamp']:
        if str(timestamp) not in daylist:
            daylist.append(str(timestamp))   
    df = df.set_index(df['timestamp'])
    df = df.sort_index()
    if 'split_csvs' not in os.listdir():
        os.mkdir('split_csvs/')  
    for i in range(len(daylist)):
        data = pd.DataFrame()
        data = df[daylist[i]:daylist[i]]
        data.to_csv('split_csvs/'+daylist[i][:10]+'.csv')

#split_by_day(csv)