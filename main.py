import pandas as pd
import numpy as np
import json
from fastapi import FastAPI

app = FastAPI()

data1 = pd.read_csv('./data-jumlah-koleksi-perpustakaan-tahun-2017.csv')
data2 = pd.read_csv('./data-jumlah-koleksi-perpustakaan-tahun-2018.csv')
data3 = pd.read_csv('./data-jumlah-koleksi-perpustakaan-tahun-2019.csv')

data = pd.concat([data1, data2, data3])

@app.get('/')
def read_root():
    """return all library data"""
    
    return data.to_dict()

@app.get('/location')
def show_lokasi():
    """return aggregated total books on each library location per year"""
    
    df = data.groupby(['lokasi', 'tahun']).sum()
    df = df.astype({"jumlah_judul": object, "jumlah_eksemplar": object})

    loc_dict = {}
    tmp_dict = {}

    for i,j in df.iterrows():   
        tmp_dict[str(i[1])] = { 
                j.index[0]: j[0],
                j.index[1]: j[1]
            }    
        loc_dict[i[0]] = tmp_dict

    return loc_dict

@app.get('/location-total')
def show_location_total():
    """return aggregated total books on each library location"""
    
    df = data.groupby(['lokasi']).sum()
    df.drop(columns = ['tahun'], inplace = True)
    df = df.astype({"jumlah_judul": object, "jumlah_eksemplar": object})

    loc_dict = {}

    for i,j in df.iterrows():   
        loc_dict[i] = {
            j.index[0]: j[0],
            j.index[1]: j[1]
        }

    return loc_dict
        

@app.get('/year')
def show_year():
    """return aggregated total books each year in all library location"""
    
    df2 = data.groupby(['tahun']).sum()
    df2 = df2.astype({"jumlah_judul": object, "jumlah_eksemplar": object})

    year_dict = {}

    for i, j in df2.iterrows():
        year_dict[i] = {
            j.index[0]: j[0],
            j.index[1]: j[1]
        }

    return year_dict

@app.get('/year-growth')
def show_growth_per_year():
    """return annual total books growth in all library location"""
    
    df3 = data.groupby(['tahun']).sum()
    df3['jumlah_judul_growth_percent'] = round(df3['jumlah_judul'].pct_change()*1e2, 2)
    df3['jumlah_eksemplar_growth_percent'] = round(df3['jumlah_eksemplar'].pct_change()*1e2, 2)
    df3.replace(np.nan, 0, inplace=True)
    df3.drop(columns = ['jumlah_judul', 'jumlah_eksemplar'], inplace = True)

    year_growth_dict = {}
    for i, j in df3.iterrows():
        year_growth_dict[i] = {
            j.index[0]: j[0],
            j.index[1]: j[1]
        }

    return year_growth_dict
    
@app.get('/location-growth')
def show_location_growth_per_year():
    """return annual total books growth on each library location"""
    
    df4 = data.groupby(['lokasi', 'tahun']).sum()

    df4['jumlah_judul_growth_percent'] = round(df4.groupby('lokasi')['jumlah_judul'].pct_change()*1e2, 2)
    df4['jumlah_eksemplar_growth_percent'] = round(df4.groupby('lokasi')['jumlah_eksemplar'].pct_change()*1e2, 2)
    df4.drop(columns = ['jumlah_judul', 'jumlah_eksemplar'], inplace = True)
    df4.replace(np.nan, 0, inplace=True)

    loc_dict2 = {}
    tmp_dict2 = {}

    for i,j in df4.iterrows():   
        tmp_dict2[str(i[1])] = { 
                j.index[0]: j[0],
                j.index[1]: j[1]
            }    
        loc_dict2[i[0]] = tmp_dict2

    return loc_dict2