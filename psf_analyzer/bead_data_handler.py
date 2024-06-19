from tifffile import imread
import pandas as pd
import json
import numpy as np
# n_psfs = 10
import os

from PIL import Image
class BeadDataHandler:
    def __init__(self, stacks, locs, config_file, xyz_profiles):
        self.dirname = os.path.dirname(stacks).replace('combined', '')
        # print('Loading stacks...', end='')
        # self.stacks = imread(stacks)
        # print('Done.')

        self._locs = pd.read_hdf(locs, key='locs')
        self._locs['point_id'] = np.arange(self._locs.shape[0])

        self.locs = self._locs.copy()
        
        with open(config_file) as f:
            self.config = json.load(f)
        self.px_size_xy = self.config['gen_args']['pixel_size']
        self.xyz_profile_dir = xyz_profiles
        # self.key_frames = {}
        # for fname in set(self.locs['fname']):
        #     tif_name = fname.split('___')[-1]
        #     tif_path = os.path.join(self.dirname, tif_name)
        #     self.key_frames[fname] = Image.open(tif_path)


    def get_bead_profile_img(self, i):
        return Image.open(os.path.join(self.xyz_profile_dir, f'{i}.jpg'))
