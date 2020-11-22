import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('owid-covid-data.csv')
data_iso_code = data['iso_code']

sub_data_frame = pd.DataFrame(columns=['ds', 'y'])

for code in range(len(data_iso_code)):
    if data_iso_code[code] == 'ESP':
        sub_data_frame = sub_data_frame.append({'ds': data.iloc[code]['date'], 'y': data.iloc[code]['total_cases']},
                                               ignore_index=True)

m = Prophet()
m.fit(sub_data_frame)

future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)
fig = plot_plotly(m, forecast)
fig.show()

fig = plot_components_plotly(m, forecast)
fig.show()

