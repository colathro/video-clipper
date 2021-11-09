import os
import ntpath
from glob import glob
import pandas as pd
from torchvision.io import read_image
from torch.utils.data import Dataset
import torch


class CSGOImageDataset(Dataset):
    def __init__(self, img_dir, transform=None, target_transform=None):
        self.image_files = [y for x in os.walk(
            img_dir) for y in glob(os.path.join(x[0], '*.jpg'))]
        self.transform = transform
        self.image_dir = img_dir

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        image = read_image(img_path)
        image_name = ntpath.basename(self.image_files[idx]).split('.')[0]
        label_str = image_name.split('_')[3]

        label = []
        for char in label_str:
            label.append(float(char))

        image = image.float()
        return image, torch.tensor(label)
