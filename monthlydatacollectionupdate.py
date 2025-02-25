import requests
import json
import pandas as pd
import os #this lets me use te secrets

#####code from her until the break is the same as the code in teh original data collection python file. Need it because we need the function again for get_bls_data##############

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

################################## start of new code

seriesId = ["CES0000000001", "LNS14000000", "CES0500000003", "LNS11000000", " CES0500000007 ",   ]  # This will find call on the series that i want data from using their given ID in the BLS API
startYear = "2022"
endYear = "2200" #make end year super far out so it can collect this data forevers

# Load existing data frame/ csv file (which should now be available in github repository after running orignal dara colection file) ######
existing_df = pd.read_csv("BLSdata.csv", index_col=0)

#now  going to grabs a new data fram using same function
new_df = get_bls_data(seriesId, startYear, endYear)

#might be having issues with boolean tuples because all of the colum data types arent the same?? across the new df and the existing one
#make them match. Do this first so that we dont run in to issue later

#year for both is an integer
new_df['year'] = new_df['year'].astype(int)
existing_df['year'] = existing_df['year'].astype(int)

#period for both is string
new_df['period'] = new_df['period'].astype(str)
existing_df['period'] = existing_df['period'].astype(str)

#series ID for both is a string
new_df['seriesID'] = new_df['seriesID'].astype(str)
existing_df['seriesID'] = existing_df['seriesID'].astype(str)




#this is meant to filter out any data that matches between the new data and the old data (matches them by year and period)

new_data_mask = ~new_df[[ 'year', 'period', "seriesID"]].apply(tuple, axis=1).isin(existing_df[[ 'year', 'period', 'seriesID']].apply(tuple, axis=1))


# the ~ means that True = unique and False = duplcate in the mask
# remvoving the ~ means that False = unique and True = duplicate
#in the case of the tuple if the boolean return false then that means it found a duplicate with another set of data in the batch (so the seriesID, year, and period mathced with the other data)
#dont want these to be duplicated which is why were looking for them, and store

#this filter should remove the false(duplicates) from the fitered data now so they dont get added
filtered_new_df = new_df[new_data_mask]

#filtered_new_df.dropna(how='any', inplace=True)

#filtered_new_df.dropna(axis=1, how='any', inplace=True)

# THis combines the original data frame and the new filtered one
#by ignore the index true, was able to make sure that the duplicated data didnt end up in the new merged set
#so it should end up adding unique data to the updated d_f
updated_df = pd.concat([existing_df, filtered_new_df], ignore_index=True)

#now if there are duplicates and they are filtered out this will leave empty spaces in our data frame which we want to get rid of

#this should remove the empty rows
updated_df.dropna(how='any', inplace=True)

#this should remove the empty columns
updated_df.dropna(axis=1, how='any', inplace=True)

#make sure to save the updated data back to a csv the BLSdata so then it updates the previous file
updated_df.to_csv("BLSdata.csv")

print(f"Updated DataFrame dumped to BLSdata.csv ")

if updated_df is not None:
    print("Updated BLS Data:")
    print(updated_df)

else:
    print("Failed to retrieve Updated BLS data.")

if existing_df.equals(updated_df) is True:
  print("There are no current updates in the data. Come back later")
else:
  print("There is new data! Check it out.")
#bls_df = updated_df  # = get_bls_data(seriesId, startYear, endYear)

#print(bool(existing_df = updated_df))
#bls_df.to_csv("BLSdata.csv")

#check to make sure we were actually able t get the data, no errors


#now should be goog


#print(existing_df)
#print(updated_df)
#print(filtered_new_df)
