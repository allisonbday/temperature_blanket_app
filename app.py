import pandas as pd
import numpy as np
import re
import streamlit as st
import datetime

import plotly.express as px
from get_weather_json import get_weather_json
from draw import draw_lines

# FUNCTIONS -------------------------------------------------------------------


@st.cache
def read_json():
    #! remember to delete!!!
    import json

    with open("raw_response.json", "r") as openfile:
        # Reading from json file
        raw_response = json.load(openfile)

    return raw_response


@st.cache
def get_data(lat, long):
    raw_response = get_weather_json(lat, long, temp_unit)
    return raw_response


@st.cache
def get_daily(raw_response, temp_unit):
    hourly_df = pd.DataFrame.from_dict(raw_response["hourly"])
    hourly_df["time"] = (
        pd.to_datetime(hourly_df["time"])
        .dt.tz_localize(raw_response["timezone"])
        .dt.tz_convert(None)
    )
    daily_df = (
        hourly_df.groupby(pd.Grouper(key="time", axis=0, freq="D"))
        .mean()
        .round(0)
        .reset_index()
        .rename(columns={"temperature_2m": temp_unit})
        .dropna()
    )
    daily_df["group"] = (
        daily_df[temp_unit].apply(lambda x: x / 10).apply(np.floor).astype(str)
    )

    return daily_df


# PAGE SET UP -----------------------------------------------------------------
st.set_page_config(page_icon="🧶", page_title="Temperature Blanket")  # , layout="wide")
st.image(
    "https://emojipedia-us.s3.amazonaws.com/source/microsoft-teams/337/yarn_1f9f6.png",
    width=100,
)
st.title("Temperature Blanket Calculator")

# SESSION STATES --------------------------------------------------------------

# Initialization
if "raw_response" not in st.session_state:
    st.session_state["raw_response"] = False

if "daily_df" not in st.session_state:
    st.session_state["daily_df"] = False

if "palette" not in st.session_state:
    st.session_state["palette"] = []


# COORDINATES -----------------------------------------------------------------


with st.sidebar:
    lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=67.55)
    long = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=133.38)

    temp_unit = st.radio("Units", ("fahrenheit", "celsius"))

    if st.button("Fetch New Data:"):
        raw_response = get_data(lat, long)
        st.session_state["raw_response"] = raw_response

        daily_df = get_daily(raw_response, temp_unit)
        st.session_state["daily_df"] = daily_df

    st.write(
        '<a href="https://open-meteo.com/">Weather data by Open-Meteo.com</a>',
        unsafe_allow_html=True,
    )

if not st.session_state["raw_response"]:
    st.info("Please input your data in the sidebar, then hit 'Fetch New Data' button")
    st.stop()

daily_df = st.session_state["daily_df"]

# fig_df = daily_df.sort_values("group", ascending=False)
# fig_df["group"] = fig_df["group"].astype(str)
# fig_df = fig_df.loc[(fig_df["time"] >= "2018-01-01")]


def rgb_to_hex(rgb):
    actual_values = re.sub("[() rgb]", "", rgb).split(",")
    hex = "#"
    for i in actual_values:
        hex += format(int(i), "02x")

    return hex


with st.expander("📆 Date Selection"):
    with st.container():
        sub1, sub2 = st.columns(2)

        with sub1:

            # todo: set default to this year
            st.number_input(
                "Select Year",
                min_value=1971,
                max_value=2022,
                value=2022,
                step=1,
                key="selected_year",
            )

        with sub2:

            start_default = datetime.datetime(st.session_state["selected_year"], 1, 1)
            end_default = datetime.datetime(st.session_state["selected_year"], 12, 31)

            start_date = st.date_input(
                "Start Date",
                min_value=datetime.datetime(1970, 1, 2),
                value=start_default,
            )
            end_date = st.date_input(
                "End Date", min_value=start_date, value=end_default
            )

col1, col2 = st.columns(2)
with col1:

    chosen_palette = st.selectbox(
        "Choose a Color Palette",
        (
            "Aggrnyl",
            "Agsunset",
            "Blackbody",
            "Bluered",
            "Blues",
            "Blugrn",
            "Bluyl",
            "Brwnyl",
            "BuGn",
            "BuPu",
            "Burg",
            "Burgyl",
            "Cividis",
            "Darkmint",
            "Electric",
            "Emrld",
            "GnBu",
            "Greens",
            "Greys",
            "Hot",
            "Inferno",
            "Jet",
            "Magenta",
            "Magma",
            "Mint",
            "OrRd",
            "Oranges",
            "Oryel",
            "Peach",
            "Pinkyl",
            "Plasma",
            "Plotly3",
            "PuBu",
            "PuBuGn",
            "PuRd",
            "Purp",
            "Purples",
            "Purpor",
            "Rainbow",
            "RdBu",
            "RdPu",
            "Redor",
            "Reds",
            "Sunset",
            "Sunsetdark",
            "Teal",
            "Tealgrn",
            "Turbo",
            "Viridis",
            "YlGn",
            "YlGnBu",
            "YlOrBr",
            "YlOrRd",
            "algae",
            "amp",
            "deep",
            "dense",
            "gray",
            "haline",
            "ice",
            "matter",
            "solar",
            "speed",
            "tempo",
            "thermal",
            "turbid",
        ),
        help="See Sequential Color Scales: [link](https://plotly.com/python/builtin-colorscales/)",
    )

    reverse = st.radio(
        "◀️ Reverse Colors",
        ("default", "reverse"),
        horizontal=True,
    )

    num_groups = daily_df["group"].nunique()
    palette = px.colors.sample_colorscale(
        chosen_palette, [n / (num_groups - 1) for n in range(num_groups)]
    )
    palette = [rgb_to_hex(i) for i in palette]
    st.session_state["palette"] = palette

    gs = sorted(daily_df["group"].unique(), reverse=True)
    # gs = [f"{x*10}° to  {x*10+9}°" if x >= 0 else f"{x*10+9}° to {x*10}°" for x in gs]
    palette_dict = dict(zip(gs, st.session_state["palette"]))

    with st.expander("Customize Color Palette"):
        for index, key in enumerate(palette_dict):
            color = st.color_picker(f"{key}", palette_dict[key])
            st.session_state["palette"][index] = color

with col2:
    palette = st.session_state["palette"]
    if reverse == "reverse":
        palette.reverse()
    filtered_df = daily_df.loc[
        (daily_df["time"] >= pd.to_datetime(start_date))
        & (daily_df["time"] <= pd.to_datetime(end_date))
    ]
    img = draw_lines(palette, filtered_df)

    st.image(img, caption="Temperature Blanket")


# # st.dataframe(filtered_df)

# fig_df = daily_df.sort_values("group", ascending=False)
# fig_df["hex"] = fig_df["group"].map(palette_dict)
# fig_df["group"] = fig_df["group"].astype(str)

# fig_df
# palette_dict

# fig = px.histogram(
#     fig_df,
#     # x=temp_unit,
#     x="group",
#     color="group",
#     color_discrete_sequence=palette,
# )
# st.plotly_chart(fig)

# fig = px.scatter(
#     fig_df, x="time", y=temp_unit, color="group", color_discrete_sequence=fig_df["hex"]
# )


# st.plotly_chart(fig)

# # fig_df["month"] = fig_df["time"].dt.month
# # fig = px.density_heatmap(fig_df, x="month", y=temp_unit)
# # st.plotly_chart(fig)

info_text = """
UPCOMING FEATURES: 
- graphs
- manual grouping 
- select to see all time or selected time range
- wave patterns
- estimates for how much yarn you will need 

All suggestions welcome!
"""

st.info(body=info_text, icon="🔜")
