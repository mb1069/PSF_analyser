from pathlib import Path
import numpy as np


def find_ftype_in_dir(dirname, key):
    return [str(fpath) for fpath in Path(dirname).rglob(key)][0]

def find_files_in_result_dir(dirname):
    tiff_files = {
        'locs': find_ftype_in_dir(dirname, 'locs.hdf'),
        'stacks': find_ftype_in_dir(dirname, 'stacks.ome.tif'),
        'config_file': find_ftype_in_dir(dirname, 'stacks_config.json'),
        'xyz_profiles': find_ftype_in_dir(dirname, 'xyz_profiles')
    }

    return tiff_files
