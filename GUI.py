import tkinter as tk
from tkinter import ttk
import pycountry
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import wget
import datetime
import os
import warnings
import matplotlib.cbook
from fbprophet import Prophet
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.winfo_toplevel().title("Covid19 Stats by Diego Bonilla")

        self.info = tk.Label(text="Put any known location and choose info type:")
        self.info.grid(column=0, row=0)

        self.text = tk.Entry()
        self.text.grid(column=0, row=1)

        stat_list = ["Total Cases", "Total Deaths", "New Cases",
                     "New Deaths", "Total Population", "GPD per capita", "Mortality Percentage"]
        self.stat_encoder = dict(zip(stat_list, range(len(stat_list))))
        self.stat = ttk.Combobox(values=stat_list)
        self.stat.grid(column=0, row=2)

        self.commit = tk.Button(text="Launch!", command=self.launch)
        self.commit.grid(column=0, row=3)

        self.commit = tk.Button(text="Exit", command=self.parent.quit)
        self.commit.grid(column=1, row=3)

        self.commit = tk.Button(text="Next Year Prediction", command=self.prophet_prediction)
        self.commit.grid(column=1, row=2)

        self.download = tk.Button(text="Update Dataset", command=self.update_data)
        self.download.grid(column=1, row=1)

        filename = 'owid-covid-data.csv'
        if not os.path.isfile('./owid-covid-data.csv'):
            filename = wget.download('https://covid.ourworldindata.org/data/owid-covid-data.csv')
        self.data = pd.read_csv(filename)

    def prophet_prediction(self):
        data_iso_code = self.data['iso_code']
        sub_data_frame = pd.DataFrame(columns=['ds', 'y'])

        input_location = self.text.get()
        valid_location = pycountry.countries.search_fuzzy(input_location)[0]
        valid_location_iso_code = valid_location.alpha_3

        what = self.stat_encoder[self.stat.get()]
        data_columns = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'population', 'gdp_per_capita']

        for code in range(len(data_iso_code)):
            if data_iso_code[code] == valid_location_iso_code:
                sub_data_frame = sub_data_frame.append(
                    {'ds': self.data.iloc[code]['date'], 'y': self.data.iloc[code][data_columns[what]]},
                    ignore_index=True)

        m = Prophet()
        m.fit(sub_data_frame)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)

        m.plot(forecast)
        m.plot_components(forecast)
        plt.show()

    def update_data(self):
        if os.path.isfile('./owid-covid-data.csv'):
            os.remove('./owid-covid-data.csv')
        filename = wget.download('https://covid.ourworldindata.org/data/owid-covid-data.csv')
        self.data = pd.read_csv(filename)

    def launch(self):
        what = self.stat_encoder[self.stat.get()]
        input_location = self.text.get()
        valid_location = pycountry.countries.search_fuzzy(input_location)[0]
        valid_location_iso_code = valid_location.alpha_3
        valid_location_name = valid_location.name

        print("Searching in valid location:", valid_location_name)

        data_list = []
        data_columns = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'population', 'gdp_per_capita']

        data_iso_code = self.data['iso_code']

        if self.stat.get() == "Mortality Percentage":
            for idx, code in enumerate(data_iso_code):
                if code == valid_location_iso_code:
                    num = self.data.iloc[idx]['total_deaths'] / self.data.iloc[idx]['total_cases']
                    if num >= 0:
                        data_list.append(num)
        else:
            for idx, code in enumerate(data_iso_code):
                if code == valid_location_iso_code:
                    num = self.data.iloc[idx][data_columns[what]]
                    if num >= 0:
                        data_list.append(num)

        dates = pd.date_range(start="2019-12-31",
                              end=f"{datetime.datetime.strptime('2019-12-31', '%Y-%m-%d') + datetime.timedelta(len(data_list) - 1):%Y-%m-%d}")

        fig = plt.figure(figsize=(16, 6))
        plt.title(self.stat.get())
        ax = fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis_date()

        plt.plot(dates, data_list)
        plt.show()


sns.set()
root = tk.Tk()
app = Application(root)
root.mainloop()
