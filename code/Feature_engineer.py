import pandas as pd
import numpy as np

class Feature_engineer():
    def __init__(self,firebox, pluto, year):
        self.year = year
        self.p_columns = ['LotArea','BldgArea',  'ComArea', 'ResArea', 'OfficeArea', 
                        'RetailArea', 'GarageArea', 'StrgeArea', 'FactryArea', 'OtherArea',
                        'LotFront', 'LotDepth', 'BldgFront', 'BldgDepth', 'NumBldgs', 
                        'NumFloors', 'UnitsRes', 'UnitsTotal','YearBuilt','AssessTot','nearest_id', 'vol_ct']

        feature = pluto[self.p_columns]
        feature.loc[feature.YearBuilt==0,'YearBuilt'] = np.median(feature[feature.YearBuilt>0]['YearBuilt'])


        self.aggs = [np.sum, np.min, np.max, np.median, np.mean, per20, per50, per80]
        fagg = feature.groupby(['nearest_id']).agg(self.aggs)

        fr = firebox[firebox.ALARM_BOX_BOROUGH=='MANHATTAN'].set_index('number')
        result = pd.concat([fagg, fr],axis=1)

        self.x = result.dropna().drop(columns=['ALARM_BOX_BOROUGH', 'ALARM_BOX_NUMBER', 'address', 'count', 'geometry'])
        self.y =  (result.dropna()['count_{0}'.format(self.year)]>0).astype(int)
        self.f_names = self.x.columns


    def drop(mask):
        self.x = self.x[self.f_names[mask]]



def per20(x):
    return np.percentile(x,20)

def per50(x):
    return np.percentile(x,50)

def per80(x):
    return np.percentile(x,80)


if __name__ == '__main__':
    print('Feature_engineer')