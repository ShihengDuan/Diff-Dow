import torch
from torch.utils.data import dataloader

from dataset import PrismDataset

ds = PrismDataset(start_date='2004-05-01', end_date='2004-05-30', scaler_mean=200, scaler_std=12, path='./')
print(ds.__len__())

