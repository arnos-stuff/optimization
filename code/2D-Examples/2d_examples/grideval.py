import numpy as np
import pandas as pd

np.random.seed(0)

def make_grid(
    xlow, xhigh,
    ylow, yhigh,
    npts = 500
    ):
    return np.meshgrid(
        np.linspace(xlow, xhigh, npts),
        np.linspace(ylow, yhigh, npts)
    )
    
    
def eval_on_grid(func, grid):
    vfunc = np.vectorize(func)
    return vfunc(*grid)

def stretch(x):
    num = x**2 - x**2*np.exp(-x)
    denom = 1 + np.exp(-x)
    return num/(denom+1e-8)

def find_domain_points(npts, grid, func, explore=False):
    # Define the limits of the domain
    xmin, xmax = grid[0].min(), grid[0].max()
    ymin, ymax = grid[1].min(), grid[1].max()
    
    # Stretch the limits of the domain, if explore is True
    if explore:
        xmin = stretch(xmin)
        xmax = stretch(xmax)
        ymin = stretch(ymin)
        ymax = stretch(ymax)
        npts = int(npts*2)

    
    # Evaluate the function on the grid
    zvals = eval_on_grid(func, grid)
    
    # Create a mask of the domain
    zdom = np.zeros_like(zvals, dtype=bool)
    mask = ~np.isnan(zvals)
    zdom[mask] = np.isfinite(zvals[mask])
    
    # Get the x and y points in the domain
    xdom, ydom = grid[0][zdom], grid[1][zdom]
    
    # Choose npts random points from the domain
    randinds = np.random.choice(
        np.arange(len(xdom)),
        size=npts,
        replace=False
    )
    
    return (
        xdom[randinds].ravel().tolist(),
        ydom[randinds].ravel().tolist()
    )
    



def slice_grid(
    x=None,
    y=None,
    grid=None,
    tol = 0.01
    ):
    
    # sanity check the tolerance
    xg, yg = grid
    xgap = np.median(np.abs(xg[0,:-1] - xg[0,1:]))
    ygap = np.median(np.abs(yg[:-1,0] - yg[1:,0]))
    tol = max(tol, xgap, ygap)
    
    if grid is None:
        raise ValueError("grid must be specified")
    if x is not None:
        mask = np.abs(grid[0][0,:] - x) < tol
        return grid[0][:,mask], grid[1][:, mask]
    elif y is not None:
        mask = np.abs(grid[1][0,:] - y) < tol
        return grid[0][mask,mask], grid[1][mask,mask]
    else:
        raise ValueError("x or y must be specified")
    
def slice_along_ray(
    xs=None,
    ys=None,
    grid=None,
    tol=0.01,
    ):
    
    if grid is None:
        raise ValueError("grid must be specified")
    if xs is not None:
        return [
            slice_grid(x=x, grid=grid, tol=tol) for x in xs
        ]
    elif ys is not None:
        return [
            slice_grid(y=y, grid=grid, tol=tol) for y in ys
        ]
    else:
        raise ValueError("xs or ys must be specified")

def is_more_truthy(a, b):
    a = np.isnan(np.array(a)).astype(int).sum()
    b = np.isnan(np.array(b)).astype(int).sum()
    return a < b

def eval_along_slice(
    xs=None,
    ys=None,
    grid=None,
    tol=0.01,
    func=None,
    ):
    
    grids = slice_along_ray(
        xs=xs,
        ys=ys,
        grid=grid,
        tol=tol,
    )
    xs = xs if xs is not None else np.array([np.nan] * len(grids))
    ys = ys if ys is not None else np.array([np.nan] * len(grids))

    for x,y, g in zip(xs, ys, grids):
        try:
            xfg = eval_on_grid(func, g).ravel()
        except Exception:
            continue
        fg = eval_on_grid(func, g).ravel()
        x = (x if is_more_truthy(x,y) else np.nan) * np.ones_like(g[0].ravel())
        y = (y if is_more_truthy(y,x) else np.nan) * np.ones_like(g[1].ravel())
        yield x, y , eval_on_grid(func, g).ravel(), g[0].ravel(), g[1].ravel()
        
        
def eval_ray_as_df(
    xs=None,
    ys=None,
    grid=None,
    tol=0.01,
    func=None,
    ):
    genxyz = eval_along_slice(
        xs=xs, ys=ys, grid=grid, tol=tol, func=func
        )
    for xfilt, yfilt, z, xg, yg in genxyz:
        
        df = pd.concat(
            [
                pd.DataFrame({"x-filter": xfilt}),
                pd.DataFrame({"y-filter": yfilt}),
                pd.DataFrame({"z-values": z}),
                pd.DataFrame({"x-values": xg}),
                pd.DataFrame({"y-values": yg}),
            ],
            axis=1
        )
        
        df["slice-axis"] = "x" if np.isnan(xfilt).any() else "y"
        df["slice-value"] = df["x-filter"] if np.isnan(xfilt).any() else df["y-filter"]
        yield df
        
def make_ray_slice(
    xs=None,
    ys=None,
    grid=None,
    tol=0.01,
    func=None,
    ):
    
    return pd.concat(
        list(eval_ray_as_df(xs=xs, ys=ys, grid=grid, tol=tol, func=func)),
        axis=0,
    )
    