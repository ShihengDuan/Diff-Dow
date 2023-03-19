import xarray as xa

data_slice = xa.open_dataarray('tmean_slice_200405.nc')
data_slice_up = xa.open_dataarray('tmean_slice_200405_low.nc')

interp = data_slice_up.interp_like(data_slice)
print(interp.shape)
interp.to_netcdf('tmean_slice_200405_interp.nc')
