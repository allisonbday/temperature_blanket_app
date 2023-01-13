#%%

# import the modules
import inspect
import plotly.express as px
from textwrap import fill

# iterating over color module
colorscale_names = []
colors_modules = ["sequential"]
for color_module in colors_modules:
    colorscale_names.extend(
        [
            name
            for name, body in inspect.getmembers(getattr(px.colors, color_module))
            if isinstance(body, list)
        ]
    )


# %%
colorscale_names

final_colorscales = [x for x in colorscale_names if "_r" not in x]
final_colorscales
# %%
