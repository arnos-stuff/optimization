import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import logging
import sys
from pathlib import Path

import grideval as gev
import functions as fns

logger = logging.getLogger(__name__)

logger.setLevel(logging.ERROR)

template = requests.get('https://storage.googleapis.com/open.data.arnov.dev/static/plots/optimization/plotply-purple-opacity-low.json')

template = json.loads(template.text)


def plot_2DFunction_along_coord(
    xs=None,
    ys=None,
    grid=None,
    func=None,
    title=None,
    ):  # sourcery skip: use-fstring-for-concatenation
    
    df = gev.make_ray_slice(
        xs=xs, ys=ys, grid=grid, func=func
    )
    sliceaxis = "x-filter" if gev.is_more_truthy(df["x-filter"].values, df["y-filter"].values) else "y-filter"
    varaxis = "x-values" if sliceaxis == "y-filter" else "y-values"

    df["slicing"] = sliceaxis + " = "
    df["slicing"] += df[sliceaxis].round(2).astype(str)
    

    df.sort_values(by=varaxis, inplace=True)
    fig = px.line(
        df, x=varaxis, y="z-values", color="slicing", title=title,
        markers=True, hover_name="slicing", facet_col="slicing", facet_col_wrap=2,
        facet_col_spacing=0.05, facet_row_spacing=0.05,
    )

    fig.update_layout(**template)
    fig.update_traces(marker={'size': 1, 'opacity': 0.5})

    return fig
    
if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        name = Path(sys.argv[1])
    else:
        print("Usage: python plotting.py <filename> <axis>")
        print("# axis assumed to be x if not specified")
        sys.exit(1)
        
    if len(sys.argv) > 2:
        axis = sys.argv[2]
        if axis not in ["x", "y"]:
            print("Usage: python plotting.py <filename> <axis>")
            print("# axis equal to 'x' or 'y', assumed to be x if not specified")
            sys.exit(1)
    else:
        axis = "x"
        
    NBSLICES = 10
    NBRANDOM = 100
    NB_RETRIES = 10
    EXPLORE = False
    
    grid = gev.make_grid(
        -0.5, 5, -0.5, 5, 200
    )
    while NB_RETRIES > 0:
        xs, ys = gev.find_domain_points(NBRANDOM, grid, fns.G, EXPLORE)
        xs = gev.np.array(xs)
        ys = gev.np.array(ys)
        mask = (xs > 0) & (ys > 0)
        xs = xs[mask]
        ys = ys[mask]
        if len(xs) > NBSLICES:
            xs = xs[::len(xs)//NBSLICES]
            ys = ys[::len(ys)//NBSLICES]
        
        
        xs = xs if 'x' in axis else None
        ys = ys if xs is None else None
        try:
            fig = plot_2DFunction_along_coord(
                xs=xs, ys=ys, grid=grid, func=fns.G, title="$G(x_0, \cdot)$"
            )
            break
        except Exception as e:
            NB_RETRIES -= 1
            print(f"Error: {e}")
            print(f"Retrying {NB_RETRIES} more times, doubling the sampling space")
            EXPLORE = True
            continue
    
    fig.write_html(name.with_suffix(".html"))
    fig.write_json(name.with_suffix(".json"))
    

    fig.show()    