import torch
from torch.utils.data import Dataset
import os
import glob
import pandas as pd
import xarray as xa

class PrismDataset(Dataset):
    def __init__(self, start_date:str, end_date:str, 
                 path, scaler_mean, scaler_std):
        """
        start_date: starting date of PRISM data. 
        end_date: ending date of PRISM data.
        path: path to the PRISM folder.
                PRISM data should be stored by month (i.e., 200405, 200406) 
        scaler_mean: mean for normalization. 
        scaler_std: std for normalization. 
        """
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.path = path
        # get all files used in the dataset:
        highres_files = []
        lowres_files = []
        interp_files = []
        year_months = pd.date_range(start_date, end_date, freq='MS').strftime("%Y%m").tolist()
        for f in year_months:
            files = path+'*'+f+'.nc'
            highres_files.append(glob.glob(files)[0])
            files = path+'*'+f+'_low.nc'
            lowres_files.append(glob.glob(files)[0])
            files = path+'*'+f+'_interp.nc'
            interp_files.append(glob.glob(files)[0])
        high_data = xa.open_mfdataset(highres_files)
        self.high_data = high_data.compute()
        low_data = xa.open_mfdataset(lowres_files)
        self.low_data = low_data.compute()
        interp_data = xa.open_mfdataset(interp_files)
        self.interp_data = interp_data.compute()
        # transform to Tensor. 
        self.interp_data = self.low_data.interp_like(self.high_data)
        self.high_data = torch.from_numpy(self.high_data['__xarray_dataarray_variable__'].data).float()
        self.low_data = torch.from_numpy(self.low_data['__xarray_dataarray_variable__'].data).float()
        self.interp_data = torch.from_numpy(self.interp_data['__xarray_dataarray_variable__'].data).float()

    def __getitem__(self, index):
        high_sample = self.high_data[index]
        low_sample = self.low_data[index]
        interp_sample = self.interp_data[index]
        high_sample = high_sample.reshape(1, high_sample.shape[0], high_sample.shape[1])
        low_sample = low_sample.reshape(1, low_sample.shape[0], low_sample.shape[1])
        """
        Needed in Diffusion.feed_data:
        Args:
            data: A tuple containing dictionary with the following keys:
                HR: a batch of high-resolution images [B, C, H, W],
                LR: a batch of low-resolution images [B, C, H, W],
                INTERPOLATED: a batch of upsampled (via interpolation) images [B, C, H, W]
            and list of corresponding months of samples in a batch.
        """
        return ({'HR': high_sample, 'LR': low_sample, 'INTERPOLATED': interp_sample}, [0])
    
    def __len__(self):
        return self.interp_data.shape[0]
