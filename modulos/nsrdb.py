import os
import sys
import time
import pathlib
import pandas as pd


email   = "felos@ciencias.unam.mx"
api_key = "gfYiPMGMLLOMK6h8PcSp2102kPZrFFwFIqp5vSM9"

def coordinate2filename(lat,lon,year):
    lat = round(lat,3)
    lon = round(lon,3)
    return f"{lat}__{lon}__{year}.csv"

def getdata(lat:float,lon:float,year:int,download_path:str="",tryagain:bool=False):
    """
    Download data from NSRDB
    See https://developer.nrel.gov/docs/solar/nsrdb/psm3-download/
    for more information.

    Parameters
    ----------
    lat : latitude of the point
    lon : longitud of the point
    year: year of the data to download
    download_path: Place to download the data. If a path is not specify, the data will not be saved.
    tryagain: Tryagain if the download fail after 5 seconds
    """
    if email is None or api_key is None:
        raise ValueError("Please specify an email and a valid api-key on the configuration file. If you dont have an api-key please sign up on https://developer.nrel.gov/signup/")

    output_filename = coordinate2filename(lat,lon,year)
    output_file = os.path.join(download_path,output_filename)

    # Check if file already exists
    if os.path.exists(output_file):
        data = pd.read_csv(output_file)
        return data

    interval = 60 # frequency in minutes of the data
    utc = "false" # false to use local time
    attributes = "air_temperature,ghi"

    base_url   = "https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?"
    parameters = f"wkt=POINT({lon}%20{lat})&names={year}&interval={interval}&utc={utc}&email={email}&api_key={api_key}&attributes={attributes}"

    url = base_url + parameters

    download_complete = False
    while not download_complete:
        try:
            data = pd.read_csv(url,skiprows=2)
            download_complete = True
        except Exception as err:
            print(f"Some error happend when downloading, see \n{url}")
            if  not tryagain:
                sys.exit()
            else:
                time.sleep(5)
    
    if download_path is not None:
        try:
            data.to_csv(os.path.join(download_path,output_filename))
        except KeyboardInterrupt as err:
            # Saving again to avoid ending with corrupted data.
            data.to_csv(os.path.join(download_path,output_filename))
            sys.exit()

    return data

def download_dataset(Latitude,Longitude,download_path="Downloads") :
    """
    Automatically download 20 years for each datapoint.

    Check download limitations at
    https://developer.nrel.gov/docs/solar/nsrdb/psm3-download/

    Parameters
    ----------
    Latitude: List or a np.array of latitudes
    Longitude: List of a np.array of longitudes
    download_path: Where the data will be store
    """

    # Create path if not exists
    if download_path != "":
        pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)

    num_downloaded = 0
    to_download    = len(Latitude)

    for lat,lon in zip(Latitude,Longitude):
        to = time.time()
        for year in range(2000,2021):
            getdata(lat,lon,year,download_path=download_path,tryagain=True)  
        tf = time.time()
        num_downloaded += 1

        download_time = round((tf - to)/60,1)
        print(f"{num_downloaded}/{to_download} Files downloaded in {download_time} min")

if __name__ == "__main__":
    import numpy as np

    Lat = np.linspace(18,20,5)
    Lon = np.linspace(-100,-98,5)

    Lat , Lon = np.meshgrid(Lat,Lon)
    Lat , Lon = Lat.reshape(-1) , Lon.reshape(-1)

    download_dataset(Lat,Lon)



    