from PIL import Image, ImageDraw
import pandas as pd


def draw_lines(palette: list, filtered_df):
    gs = sorted(filtered_df["group"].unique(), reverse=True)
    dictionary = dict(zip(gs, palette))
    scale = 2

    img = Image.new("RGB", (300, (len(filtered_df))), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    i = 0
    for row in filtered_df["group"].to_list():
        draw.line((0, i, 300, i), fill=dictionary[row], width=1)
        i += 1

    return img


def draw_circles(palette: list, filtered_df):
    gs = sorted(filtered_df["group"].unique(), reverse=True)
    dictionary = dict(zip(gs, palette))

    img = Image.new("RGB", (len(filtered_df), len(filtered_df)), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    i = 0
    for row in filtered_df["group"].to_list():
        draw.ellipse((0 - i, 0 - i, 0 + i, 0 + i), outline=dictionary[row], width=1)
        i += 1

    return img


# # TESTING ---------------------------------------------------------------------


# palette = [
#     "#e7fa5a",
#     "#f7cb44",
#     "#f99e40",
#     "#e87a58",
#     "#c56576",
#     "#9a5888",
#     "#734892",
#     "#47379a",
#     "#163070",
#     "#032333",
# ]

# daily_df = pd.read_csv("daily_df.csv")

# daily_df["time"] = (
#     pd.to_datetime(daily_df["time"]).dt.tz_localize("GMT").dt.tz_convert(None)
# )
# filtered_df = daily_df.loc[daily_df["time"].dt.year == 2002]
# filtered_df

# # test = draw_image(palette, filtered_df)
# # test.show()


# # test = draw_circles(palette, filtered_df)
# # test.show()
