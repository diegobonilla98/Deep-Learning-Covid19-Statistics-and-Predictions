import pycountry
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data_path = '/media/bonilla/HDD_2TB_basura/databases/owid-covid-data.csv'
input_location = 'Valencia'

valid_location = pycountry.countries.search_fuzzy(input_location)[0]
valid_location_iso_code = valid_location.alpha_3
valid_location_name = valid_location.name

print("Searching in valid location:", valid_location_name)

data = pd.read_csv(data_path)

location_total_cases = []
location_total_deaths = []
location_new_cases = []
location_new_deaths = []
location_population = []
location_gdp_per_capita = []

data_iso_code = data['iso_code']
for idx, code in enumerate(data_iso_code):
    if code == valid_location_iso_code:
        location_total_cases.append(data.iloc[idx]['total_cases'])
        location_total_deaths.append(data.iloc[idx]['total_deaths'])
        location_new_cases.append(data.iloc[idx]['new_cases'])
        location_new_deaths.append(data.iloc[idx]['new_deaths'])
        location_population.append(data.iloc[idx]['population'])
        location_gdp_per_capita.append(data.iloc[idx]['gdp_per_capita'])


plt.plot(np.array(location_total_cases))
plt.plot(np.array(location_total_deaths))

plt.show()
sns.set()
