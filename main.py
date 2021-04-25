import pandas as pd
import numpy as np
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

data1 = pd.read_csv('./data-jumlah-koleksi-perpustakaan-tahun-2017.csv')
data2 = pd.read_csv('./data-jumlah-koleksi-perpustakaan-tahun-2018.csv')
data3 = pd.read_csv('./data-jumlah-koleksi-perpustakaan-tahun-2019.csv')

data = pd.concat([data1, data2, data3])

@app.get('/')
def read_root():
    """return home page"""
    
    string = """
        <html>
            <body>
                <h1>
                    Selamat datang di data perpustakaan wilayah Jakarta!
                </h1>
                <h2>
                    Data-data yang dapat diperoleh:
                </h2>
                <ul>
                        <li><b>/location/</b> : data jumlah buku di setiap perpustakaan tiap tahunnya</li>
                        <li><b>/year/</b> : data total jumlah buku di semua lokasi tiap tahunnya</li>
                        <li><b>/location-growth/</b> : pertumbuhan jumlah buku di setiap lokasi tiap tahunnya</li>
                        <li><b>/year-growth/</b> : pertumbuhan jumlah buku total di semua lokasi tiap tahunnya</li>
                </ul>
            </body>
        </html>
    """
    
    return HTMLResponse(content=string, status_code=200)

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