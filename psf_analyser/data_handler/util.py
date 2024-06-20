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


def grid_psfs(psfs, cols=10):
    rows = (len(psfs) // cols) + (1 if len(psfs) % cols != 0 else 0)
    n_spaces = int(cols * rows)
    if n_spaces > len(psfs):
        placeholder = np.zeros((n_spaces-len(psfs), *psfs[0].shape))
        placeholder[:] = np.mean(psfs)
        psfs = np.concatenate((psfs, placeholder))
        cols = len(psfs) // rows
    psfs = list(chunks(psfs, cols))
    psfs = [np.concatenate(p, axis=-1) for p in psfs]
    psfs = np.concatenate(psfs, axis=-2)
    return psfs