
# PSF_analyzer

## Dependencies
A custom version of Picasso is currently used; it can be downloaded and installed from the following url or using the following command:

https://github.com/mb1069/picasso.git

```sh
pip install git+https://github.com/mb1069/picasso.git#egg=picassosr
```

## Installation

The package can be installed as a Python package (currently tested for Python 3.10).

```sh
pip install git+https://github.com/mb1069/psf_analyser.git#egg=psf_analyser`
```

To create a conda env for the package:
```sh
conda  create  -y  --name  psf_analyser  python==3.10 ;
conda  activate  psf_analyser;
pip install git+https://github.com/mb1069/psf_analyser.git#egg=psf_analyser`
```

## Using the package
### Preparing bead stacks
Pre-processing is required to gather statistics & images of the beads for the app.
This can be done using:  
`psf-prep-data <mydir>`

This tool will:
1. Find TIF files recursively in directory
2. Localise beads in each TIF file using Picasso
3. Calculate metrics / render images for each bead
4. Compile these into files for the app to visualise.

Bead stacks need to be placed in a common directory structure, eg:
```
mydir
│
└─── folder1
│      file1.ome.tif
└─── folder2
       file2.ome.tif
       file3.ome.tif  
```

Other options for `psf-prep-data` are available to fine-tune Picasso's localisation algorithm, or overwrite the metadat in TIF files if it is incorrect (eg `--pixel_size`, `--z_step`). The `--regen` flag is available to re-generate localisation results for each TIF file.

The output location of the program will be `<mydir>/combined/` (you'll need this to point the app at the correct results location).

### Visualising results
The web-based visualisation tool can be started using `psf-gui`. A URL will be shown in the command line.

Navigate to the URL, enter the directory containing your results `<mydir>/combined` and click `submit`.


## Developer help
To run the tool to prepare data (from repo directory):
`python psf_analyser/prepare_data/main.py -h`

To run the Dash app
`python psf_analyser/app.py`

A useful debugging flag is available in app.py - this enables Dash's debugging tools, with front-end error reporting.