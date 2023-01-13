#%%
import requests
import pandas as pd
from datetime import date
import numpy as np

import json

#%%
def get_forecast_json(lat, long, temp_unit):
    url = "https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&hourly=temperature_2m&start_date=2022-06-08&end_date={2}&temperature_unit={3}".format(
        lat, long, date.today(), temp_unit
    )
    response = requests.get(url)
    return response.json()


# test = get_forecast_json(67.55, 133.38, "fahrenheit")
# #%%
# test

# #%%
# hourly_df = pd.DataFrame.from_dict(test["hourly"])

# hourly_df["time"] = (
#     pd.to_datetime(hourly_df["time"])
#     .dt.tz_localize(test["timezone"])
#     .dt.tz_convert(None)
# )
# daily_df = (
#     hourly_df.groupby(pd.Grouper(key="time", axis=0, freq="D"))
#     .mean()
#     .round(0)
#     .reset_index()
#     .dropna()
# )

# # %%
# daily_df
# # # %%
