source /home/miguel/anaconda3/etc/profile.d/conda.sh;
conda env remove -y -n test_env || true;
conda create -y --name test_env python==3.10 ;
conda activate test_env;
pip install dist/psf_analyser-0.1.0-py3-none-any.whl;