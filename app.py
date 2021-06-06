# From Template
# pip install pandas hvplot==0.7.1 holoviews==1.14.3 bokeh panel==0.11.3
# panel serve holoviz_linked_brushing.py --auto --show
import hvplot.pandas
import holoviews as hv
import panel as pn
from bokeh.sampledata.iris import flowers

pn.extension(sizing_mode="stretch_width")
hv.extension("bokeh")

accent_color = "#00286e"

from augmentedbondingcurve import abc_debug_app

pn.template.FastListTemplate(
    site="Commons Upgrade",
    title="Augmented Bonding Curve",
    header_background=accent_color,
    main=[
        *abc_debug_app()
    ],

).servable()
