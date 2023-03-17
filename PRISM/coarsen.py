import xarray as xa

file = '/p/gpfs1/shiduan/PRISM/tmean_200405.nc'
data = xa.open_dataarray(file)

data_slice = data.isel(x=slice(40, 40+128), y=slice(70, 70+128))
print('high_res mean: ', data_slice.mean())
print('high_res shape: ', data_slice.shape)
data_slice_up = data_slice.coarsen(x=4, y=4).mean()
print('low_res mean: ', data_slice_up.mean())
print('low_res shape: ', data_slice_up.shape)
data_slice_up.to_netcdf('tmean_slice_200405_low.nc')
data_slice.to_netcdf('tmean_slice_200405.nc')
print('Done')
