import requests
import pandas as pd

# Function to get unique prizes and categories
def get_unique_prizes(lst, field):
    unique_prizes = set([])
    for prizes in lst:
        unique_prizes.add(prizes[field])
    
    return str(unique_prizes)

# Detching the data
r = requests.get('https://api.nobelprize.org/v1/laureate.json', 
                 headers={'Accept': 'application/json'})

json_data = r.json()

df_laureates = pd.DataFrame(json_data['laureates'])

r = requests.get('https://api.nobelprize.org/v1/country.json', 
                 headers={'Accept': 'application/json'})

json_data = r.json()

df_countries = pd.DataFrame(json_data['countries'])

# Creating the output dataframe
result = pd.DataFrame(columns = ['id', 'name', 'dob', 'unique_prize_years', 'unique_prize_categories', 'gender', 'bornCountry'])

result['id'] = df_laureates['id']
result['name'] = df_laureates['firstname'] + ' ' + df_laureates[pd.isnull(df_laureates['surname']) == False]['surname']
result['dob'] = df_laureates['born']
result['unique_prize_years'] = df_laureates['prizes'].apply(get_unique_prizes, args=('year',))
result['unique_prize_categories'] = df_laureates['prizes'].apply(get_unique_prizes, args=('category',))
result['gender'] = df_laureates['gender']
result['bornCountry'] = df_laureates['bornCountryCode'].apply(lambda code: df_countries['name'][(df_countries['code'] == code)].values.any())

result = result.fillna('Not available')
result = result.replace(False, "Not available")

# Saving to CSV
result.to_csv('output.csv', index=False)