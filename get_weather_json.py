#%%
# https://open-meteo.com/en/docs/historical-weather-api
import requests
import pandas as pd
from datetime import date
import numpy as np

import json

#%%
def get_weather_json(lat, long, temp_unit):
    url = "https://archive-api.open-meteo.com/v1/archive?latitude={0}&longitude={1}&start_date=1970-01-02&end_date={2}&hourly=temperature_2m&temperature_unit={3}".format(
        lat, long, date.today(), temp_unit
    )
    response = requests.get(url)
    return response.json()


test = get_weather_json(67.55, 133.38, "fahrenheit")
#%%
test

#%%
test_df = pd.DataFrame.from_dict(test["hourly"])

# test_df["time"] = pd.to_datetime(test_df["time"]).dt.tz_localize(test["timezone"])
test_df["time"] = (
    pd.to_datetime(test_df["time"]).dt.tz_localize(test["timezone"]).dt.tz_convert(None)
)
pd.set_option("precision", 0)
daily_df = (
    test_df.groupby(pd.Grouper(key="time", axis=0, freq="D"))
    .mean()
    .round()
    .reset_index()
)
daily_df["group"] = daily_df["temperature_2m"].apply(lambda x: x / 10).apply(np.floor)
daily_df
# %%
json_object = json.dumps(test)

# Writing to sample.json
with open("raw_response.json", "w") as outfile:
    outfile.write(json_object)

# %%
