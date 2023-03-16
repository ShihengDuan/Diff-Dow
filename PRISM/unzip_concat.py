import zipfile
import xarray as xa
import numpy as np
import glob
import os

prefix = '/p/gpfs1/shiduan/PRISM/'
for year in range(1982, 2020):
    for month in range(1, 13):
        year_month = str(year)+str(month).zfill(2)
        files = glob.glob(prefix+'prism.oregonstate.edu/daily/tmax/'+str(year)+'/PRISM_tmax_stable_4kmD2_'+year_month+'*_bil.zip')
        ppts = []
        print(len(files), 'files lens')
        for file in sorted(files):
            for tmp_file in glob.glob(prefix+'tmp/tmax/*'):
                os.remove(tmp_file)
                pass
            ydate = file[-16:-16+8]
            print(ydate, file)
            while True:
                try:
                    # with zipfile.ZipFile(file, 'r') as zip_ref:
                    #     zip_ref.extractall('tmp/tmean/.')
                    zip_ref = zipfile.ZipFile(file, 'r')
                    zip_ref.extractall('tmp/tmax/.')
                    print('unzip done')
                    break
               
                except:
                    for tmp_file in glob.glob('tmp/tmax/*'):
                        os.remove(tmp_file)
                        pass
                    print('retry?')
                    pass
                
            # unzip(file, "tmp/tmin/")
            data = xa.open_rasterio('tmp/tmean/PRISM_tmax_stable_4kmD2_'+ydate+'_bil.bil')
            data_slice = data.isel(band=0)
            ppts.append(data_slice)
            for tmp_file in glob.glob('tmp/tmax/*'):
                os.remove(tmp_file)
                pass
        print(len(ppts))

        ppts = xa.concat(ppts, dim='time')
        print(ppts)
        ppts.to_netcdf(prefix+'tmax_'+str(year_month)+'.nc')