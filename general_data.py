import pycountry
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_path = '/media/bonilla/HDD_2TB_basura/databases/owid-covid-data.csv'

data = pd.read_csv(data_path)

countries_total_cases = {}
countries_gpt = {}
countries_total_deaths = {}
countries_population = {}

data_iso_code = data['iso_code']
for idx, code in enumerate(data_iso_code):
    countries_total_cases[code] = data.iloc[idx]['total_cases']
    countries_gpt[code] = data.iloc[idx]['gdp_per_capita']
    countries_total_deaths[code] = data.iloc[idx]['total_deaths']
    countries_population[code] = data.iloc[idx]['population']

plt.scatter(x=np.log(list(countries_total_cases.values())), y=countries_gpt.values())
for lab, x, y in zip(list(countries_total_cases.keys()), np.log(list(countries_total_cases.values())), countries_gpt.values()):
    plt.annotate(lab, (x, y))

plt.show()
sns.set()
