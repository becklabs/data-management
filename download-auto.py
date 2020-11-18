# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:02:51 2020

@author: beck
"""
import os
import dateparser
from datetime import datetime
import shutil
import time
import pandas as pd
import gpxpy
import pytz
import sys
from tkinter.filedialog import askdirectory
from tkinter import *

def getCreationDate(file):
    #GET CREATEDATE FROM EXIFTOOL
    stream = os.popen('exiftool '+file)
    output = stream.read().split('\n')
    for item in output:
        item = item.replace(' ','')
        if item.split(':')[0] == 'CreateDate':
            break
    datelist=item.split(':')[1:]
    creationdate = ''
    for item in datelist:
        creationdate = creationdate+item
    creationdate = dateparser.parse(creationdate)
    return creationdate

def trackExtract(inputPath,gps_filename):
    ext = gps_filename.split('.')
    if ext[1] == 'csv':
        gps_telem = pd.read_csv(inputPath+gps_filename)
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
    if ext[1] == 'gpx':
        points = []
        with open(inputPath+gps_filename,'r') as gpxfile:
            gpx = gpxpy.parse(gpxfile)
            for track in gpx.tracks:
                for segment in track.segments:
                    sys.stdout.flush()
                    for point in segment.points:
                        dict = {'timestamp': point.time,
                                'latitude': point.latitude,
                                'longitude': point.longitude,
                                'elevation': point.elevation
                                    }
                        points.append(dict)
        gps_telem = pd.DataFrame.from_dict(points)
        i = 0
        for timestamp in gps_telem['timestamp']:
            gps_telem.loc[i,'timestamp'] = gps_telem.loc[i,'timestamp'].to_pydatetime().replace(tzinfo=pytz.UTC) #.astimezone(pytz.timezone(gp_timezone))
            i+=1
    return gps_telem

def move(inputPath, outputPath):
    exts = ['MP4', 'JPG', 'gpx', 'csv']
    for file in os.listdir(inputPath):
        stat = os.stat(inputPath+file)
        downloadDate = dateparser.parse(str(stat.st_mtime))
        if abs((datetime.now() - downloadDate).total_seconds()) < 86400:
            ext = file.split('.')[-1]
            if ext in exts:
                if ext == 'MP4' or ext == 'JPG':
                    creationdate = getCreationDate(inputPath+file)
                if ext == 'csv' or ext == 'gpx':
                    data = trackExtract(inputPath, file)
                    creationdate = data['timestamp'][1]
                outputFolder = creationdate.strftime("%d%B%Y")
                if outputFolder not in os.listdir(outputPath):
                    os.mkdir(outputPath+outputFolder)
                shutil.move(inputPath+file, outputPath+outputFolder+'/'+file)
                print('Moved '+file+' to '+outputPath+outputFolder)
                
def init(): 
        root = Tk()
        print('Input Path: ', end = ' ')
        root.update()
        inputPath = askdirectory()
        print(inputPath)
        
        print('Output Path: ', end = ' ')
        root.update()
        outputPath = askdirectory()
        print(outputPath)
        root.destroy()
        
        if inputPath[-1] != '/':
            inputPath += '/'
        if outputPath[-1] != '/':
            outputPath += '/'
        print('Running...')
        while True:
            move(inputPath, outputPath)
            time.sleep(1)

if __name__ == '__main__':
    init()
