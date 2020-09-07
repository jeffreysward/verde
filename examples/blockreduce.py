"""
Blocked reduction operations
============================

When gridding data that has been highly oversampled in a direction (shipborne
and airborne data, for example), it is important to decimate the data before
interpolation to avoid aliasing. Class :func:`verde.BlockReduce` decimates
data by applying a reduction operation (mean, median, mode, max, etc) to the
data in blocks. For non-smooth data, like bathymetry, a blocked median filter
is a good choice.
"""
import matplotlib.pyplot as plt
import pygmt
import numpy as np
import verde as vd

# We'll test this on the Baja California shipborne bathymetry data
data = vd.datasets.fetch_baja_bathymetry()

# Decimate the data using a blocked median with 10 arc-minute blocks
reducer = vd.BlockReduce(reduction=np.median, spacing=10 / 60)
coordinates, bathymetry = reducer.filter(
    (data.longitude, data.latitude), data.bathymetry_m
)
lon, lat = coordinates

print("Original data size:", data.bathymetry_m.size)
print("Decimated data size:", bathymetry.size)

# Make a plot of the decimated data using PyGMT
fig = pygmt.Figure()
fig.basemap(region=vd.get_region(coordinates), projection="M8i", frame=True)
fig.coast(land="black", water="skyblue")
pygmt.makecpt(cmap="viridis", series=[bathymetry.min(), bathymetry.max()])
fig.plot(x=lon, y=lat, style="c0.2c", color=bathymetry, pen="black", cmap=True)
fig.colorbar(frame='af+l"Depth (km)"')
fig.show()
