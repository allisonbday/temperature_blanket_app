#%%
# https://open-meteo.com/en/docs/historical-weather-api
import requests
import pandas as pd
from datetime import date
import numpy as np

import json

#%%
def get_location_json(town):
    url = "https://geocoding-api.open-meteo.com/v1/search?name={0}".format(town)
    response = requests.get(url)
    return response.json()


# test = get_weather_json("Chicago")
# #%%
# if "results" not in test:
#     print("NOTHING")
# else:
#     test_df = pd.DataFrame.from_dict(test["results"])
# #%%
# test_df["search"] = test_df.apply(lambda x: f"{x.admin1}, {x.country}", axis=1)


# # %%
# locations = pd.read_csv("wikipedia-iso-country-codes.csv")
# locations

# # %%
# country_code = test_df.iloc[0]["country_code"].lower()
# print(country_code)
# URL = "https://hatscripts.github.io/circle-flags/flags/{0}.svg".format(country_code)
