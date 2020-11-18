import pandas as pd
from dateparser import *
import seaborn as sn
import matplotlib.pyplot as plt

def clean(survey,drop_nans=True):
    
    survey123 = pd.read_csv(survey)#convert survey123 data into dataframe
    df=pd.DataFrame()#create empty df for simplification

    #Read in Creation Date, convert to datetime object
    df['CreationDate'] = [parse(c) for c in survey123['CreationDate']]

    #Read in Lat and Long
    df['Latitude'] = [c for c in survey123['y']]
    df['Longitude'] = [c for c in survey123['x']]

    #Read in Coverage Density
    i=0
    for pt in survey123['Eelgrass coverage/density']:
        if str(pt) != 'other':
            df.loc[i,'Coverage Density'] = pt
        else:
            df.loc[i,'Coverage Density'] = survey123.loc[i,'Other - Eelgrass coverage/density']
        i+=1

    # Read in Bottom Type
    i=0
    for pt in survey123['Bottom Type']:
        if pt != 'other':
            df.loc[i,'Bottom Type'] = pt
        else:
            df.loc[i,'Bottom Type'] = survey123.loc[i,'Other - Bottom Type']
        i+=1
    
    #Clean coverage densities
    i = 0
    for density in df['Coverage Density']:
        if density == 'none':
            df.loc[i,'Coverage Density'] = 0
        if density == '1_solo_colonizing_plant':
            df.loc[i,'Coverage Density'] = 1
        if density == '25_':
            df.loc[i,'Coverage Density'] = 25
        if density == str(50):
            df.loc[i,'Coverage Density'] = 50
        if density == str(75):
            df.loc[i,'Coverage Density'] = 75
        if density == '100':
            df.loc[i,'Coverage Density'] = 100
        i+=1
    i=0
    for density in df['Coverage Density']:
        if type(density) != int:
            df.loc[i,'Coverage Density'] = float('NAN')
        i+=1
    
    #Clean Bottom Types
    i = 0
    for bottomtype in df['Bottom Type']:
        bottomtype = str(bottomtype).split(',')
        removals = ['solid_granite_rock','shells','clay_harder_than_mud','other']
        for x in removals:
            if x in bottomtype:
                bottomtype.remove(x)
        if len(bottomtype) == 1:
            if 'mud_more_slick_than_sand' in bottomtype:
                df.loc[i,'bottomtype_int'] = 0.0251
        if 'mud_more_slick_than_sand' in bottomtype:
            bottomtype.remove('mud_more_slick_than_sand')
        if len(bottomtype) == 1:
            if 'sand' in bottomtype:
                df.loc[i,'bottomtype_int'] = 0.375
            if 'gravel' in bottomtype:
                df.loc[i,'bottomtype_int'] = 12.5
            if 'stony_cobble' in bottomtype:
                df.loc[i,'bottomtype_int'] = 113
        if len(bottomtype)== 2:
            if all(x in bottomtype for x in ['sand', 'clay']) == True:
                df.loc[i,'bottomtype_int'] = 0.0251
            if all(x in bottomtype for x in ['sand', 'gravel']) == True:
                df.loc[i,'bottomtype_int'] = 3.5
            if all(x in bottomtype for x in ['gravel', 'stony_cobble']) == True:
                df.loc[i,'bottomtype_int'] = 48
        if len(bottomtype) > 2:
            if 'stony_cobble' in bottomtype:
                if 'gravel' in bottomtype:
                    df.loc[i,'bottomtype_int'] = 48
                else:
                    df.loc[i,'bottomtype_int'] = 113

        i+=1
    df['Coverage Density'] = [float(c) for c in df['Coverage Density']]
    df = df.drop('Bottom Type',axis=1)
    df = df.rename(columns={'bottomtype_int':'Bottom Type'})
    
    #Drop NaN values if drop_nans == True
    BottomDf=df.dropna(subset = ["Bottom Type"])
    BottomDf = BottomDf.drop('Coverage Density',axis=1)
    
    CovDensDf=df.dropna(subset = ["Coverage Density"])
    CovDensDf=CovDensDf.drop('Bottom Type',axis=1)
    
    #BottomDf.to_csv('bottomtype_survey.csv')
    #CovDensDf.to_csv('coveragedensity_survey.csv')
    
    if drop_nans == True:
        df = df.dropna()
    return df
df = clean('surveyPoint_1.csv')
df = df[(df['CreationDate'] > parse('2020-1-1 01:00:00')) & (df['CreationDate'] <= parse('2020-10-18 4:00:00'))]
corrMatrix = df.corr()
sn.heatmap(corrMatrix, annot=True)
plt.show()
