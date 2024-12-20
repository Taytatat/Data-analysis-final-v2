# i think this pip things helps to 1) create a requirments file
#2) the requirments.tx file will save crrent the versions of the exact packages
#im using here so that I dont have to specify each time, or somethin
#!pip install session-info <-comminting out these in repository file because done need them here in order to run code(they were just to help get requirments.txt file) if running code in colab outside of this you wll have to uncomments thses again
#!pip freeze > requirments.txt <-same

import requests
import json
import pandas as pd
import os #this lets me use te secrets

api_key = os.environ["api_key"]  #grabs env variable from yml file, to utilize the secret in the code
#checked and local api_key worked so if yml is configured correctly then api should run here

#trying to create a function that can retreave the requested data from the BLS database using their API key

#hoping to have it so that this first set of code only serves as the base data that is run first so we have the initial csv. Everything after should be auto updated by my other python
#scripts but we'll see!

def get_bls_data(series_ids, start_year, end_year):

    headers = {'Content-type': 'application/json'}

    bls_data = json.dumps({
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year,
        "registrationkey": api_key
    })

    try:
        response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data = bls_data, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        # Now i can check if the request was successful
        if json_data['status'] != 'REQUEST_SUCCEEDED':
            print(f"BLS API request failed: {json_data['message']}")
            return None


        all_series_data = []
        for series in json_data['Results']['series']:
            series_id = series['seriesID']
            for item in series['data']:
                all_series_data.append({
                    'seriesID': series_id,
                    'year': item['year'],
                    'period': item['period'],
                    'value': item['value']
                })

        # Convert to DataFrame
        df = pd.DataFrame(all_series_data)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error during BLS API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
    except KeyError as e:
        print(f"Error accessing data in JSON response: {e}")
        return None

#Total Nonfarm Employment - Seasonally Adjusted - CES0000000001

#Unemployment Rate (Seasonally Adjusted) - LNS14000000

#Total Private Average Hourly Earnings of All Employees - Seasonally Adjusted - CES0500000003

#Civilian Labor Force (Seasonally Adjusted) - LNS11000000

#Total Private Average Weekly Hours of Prod. and Nonsup. Employees - Seasonally Adjusted - CES0500000007

#defining variables going to use in function
seriesId = ["CES0000000001", "LNS14000000", "CES0500000003", "LNS11000000", " CES0500000007 ",   ]  # This will find call on the series that i want data from using their given ID in the BLS API
startYear = "2022"
endYear = "2024"

#call the function and assign the output to a dataframe
bls_df = get_bls_data(seriesId, startYear, endYear)

#trying to turn collected data into a csv
bls_df.to_csv("BLSdata.csv")

#helps to catch if thers an error collecting the df
if bls_df is not None:
    print("BLS Data:")
    print(bls_df)
else:
    print("Failed to retrieve BLS data.")
