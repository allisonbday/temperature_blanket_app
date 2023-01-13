import pandas as pd
import numpy as np
import altair as alt

# todo: you only need


def alt_draw_chevron(filtered_df, palette_dict, width, mod, temp_unit):
    # todo: only generate peaks/dips to save time
    alt.data_transformers.disable_max_rows()
    filtered_df = filtered_df.sort_values("time", ascending=False)
    filtered_df["day"] = filtered_df["time"].rank(method="min")
    filtered_df["group"] = filtered_df["group"].astype(str)
    filtered_df["hex"] = filtered_df["group"].map(palette_dict)

    blanks = {}
    for i in range(1, len(filtered_df) + 1):
        blanks[i] = list(range(1, width))

    filtered_df["x"] = filtered_df["day"].map(blanks)
    filtered_df = filtered_df.explode("x")

    filtered_df["y"] = filtered_df.apply(
        # todo: vectorize
        lambda x: (x.x % mod if x.x % mod < (mod / 2) else mod - x.x % mod) + x.day,
        axis=1,
    )

    line = (
        alt.Chart(filtered_df)
        .mark_line()
        .encode(
            x="x",
            y="y",
            color=alt.Color("hex", scale=None),
            tooltip=["time", temp_unit, "group"],
        )
        .properties(width=width, height=width)
    )

    return line


def alt_draw_lines(filtered_df, palette_dict, width, temp_unit):
    # todo: only generate the 1st and last points
    alt.data_transformers.disable_max_rows()
    filtered_df = filtered_df.sort_values("time", ascending=False)
    filtered_df["day"] = filtered_df["time"].rank(method="min")
    filtered_df["group"] = filtered_df["group"].astype(str)
    filtered_df["hex"] = filtered_df["group"].map(palette_dict)

    blanks = {}
    for i in range(1, len(filtered_df) + 1):
        blanks[i] = list(range(1, width))

    filtered_df["x"] = filtered_df["day"].map(blanks)
    filtered_df = filtered_df.explode("x")

    filtered_df["y"] = filtered_df.apply(
        lambda x: x.day,
        axis=1,
    )

    line = (
        alt.Chart(filtered_df)
        .mark_line()
        .encode(
            x="x",
            y="y",
            color=alt.Color("hex", scale=None),
            tooltip=["time", temp_unit, "group"],
        )
        .properties(width=width, height=width)
    )

    return line


# palette_dict = {
#     "8.0": "#032333",
#     "7.0": "#11306a",
#     "6.0": "#3d349b",
#     "5.0": "#674296",
#     "4.0": "#8b528c",
#     "3.0": "#b05e80",
#     "2.0": "#d46c6b",
#     "1.0": "#f0834d",
#     "0.0": "#faa63e",
#     "-1.0": "#f6cf45",
#     "-0.0": "#e7fa5a",
# }

# filtered_df = pd.read_csv("filtered_df.csv")
# width = 300
# mod = 10

# # test = draw_chevron(filtered_df, palette_dict, width, mod)
# test = draw_lines(filtered_df, palette_dict, width)
# #%%
# test.show()

# # %%
