import os
import torch
import torch.nn.parallel
import torch.utils.data
from torch.utils.data import Dataset
import torchvision.utils as vutils
import numpy as np
import cv2
import matplotlib.pyplot as plt
import utils as utils
import glob
import nibabel as nab
import torchvision

def show_example_images(dataloader):
    # Get image batch
    real_batch = next(iter(dataloader))

    # Create a grid of subplots
    fig, axes = plt.subplots(3, 5, figsize=(12, 6))
    axes = axes.flatten()

    # Plot each subplot
    for i in range(15):
        img = real_batch[i, :, :].cpu().numpy()  
        axes[i].imshow(img, cmap='gray')         
        axes[i].axis("off")                      

    plt.suptitle("Training Images")
    plt.savefig(f'./outputs/test_images.png')

def load_data():
    device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")
    
    train_folder_path = "/home/groups/comp3710/HipMRI_Study_open/keras_slices_data/keras_slices_train"
    test_folder_path = "/home/groups/comp3710/HipMRI_Study_open/keras_slices_data/keras_slices_test"

    train_file_list = sorted(glob.glob(f"{train_folder_path}/**.nii.gz", recursive=True))
    test_file_list = sorted(glob.glob(f"{test_folder_path}/**.nii.gz", recursive=True))
    
    train_dataset = utils.load_data_2D(train_file_list[1:]) # trim list as root file is included
    test_dataset = utils.load_data_2D(test_file_list[1:])
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=64,
                                            shuffle=True)
    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=64,
                                            shuffle=True)
   
    return train_dataloader, test_dataloader
    