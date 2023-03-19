"""
Interpolate low-res to high-res. There will be NAN paddings around the pictures. 
"""
import xarray as xa

data_slice = xa.open_dataarray('tmean_slice_200405.nc')
data_slice_up = xa.open_dataarray('tmean_slice_200405_low.nc')

interp = data_slice_up.interp_like(data_slice)
print(interp.shape)
interp = interp.fillna(0) # fill nan with 0. should be smarter than this. 
interp.to_netcdf('tmean_slice_200405_interp.nc')
print(interp[0])
