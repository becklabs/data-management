# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:02:51 2020

@author: beck
"""
import os
import dateparser
from datetime import datetime, timedelta
import shutil
import time
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

    return creationdate

def func(inputPath, outputPath):
    for file in os.listdir(inputPath):
        stat = os.stat(inputPath+file)
        downloadDate = dateparser.parse(str(stat.st_mtime))
        if abs((datetime.now() - downloadDate).total_seconds()) < 86400:
            if file.split('.')[-1] == 'MP4':
                creationdate = getCreationDate(inputPath+file)
                print(creationdate)
                print(file)
                outputFolder = creationdate.strftime("%d %B %Y")
                if outputFolder not in os.listdir(outputPath):
                    os.mkdir(outputPath+outputFolder)
                shutil.move(inputPath+file, outputPath+outputFolder+'/'+file)

def exec(inputPath ='C:/Users/beck/Downloads', outputPath = False):
        if inputPath[-1] != '/':
            inputPath += '/'
        if outputPath[-1] != '/':
            outputPath += '/'
        while True:
            func(inputPath, outputPath)
            time.sleep(1)
