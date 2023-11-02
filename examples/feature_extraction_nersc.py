''' 
Script showing how to extract S1 features needed to train or run inference on CNN network.

Features extracted: 
    - Sigma0 in dB for HH and HV, denoised with either ESA or NERSC algorithm
    - incident angle (IA)
    - swath mask
All extracted features are saved in tif format in the 'features' folder.
'''

from ice_water_cnn_qiang.extract_features import extract_features
from pathlib import Path
from loguru import logger
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# define the basic data directory for your project
BASE_DIR = Path('/scratch/cta014/Sentinel1/CNN_ice_water/training')

# define the level 1 (L1) data directory (i.e.where SAFE folders are stored)
BASE_L1 = BASE_DIR / 'originals'

# read in list of S1 basenames to process
S1_list = open((BASE_DIR / 'S1_imagelist_training.txt'), 'r')
ID_to_process = S1_list.read().splitlines()

for S1_name in ID_to_process:

    # build the path to S1 SAFE folder
    safe_folder = BASE_L1 / f'{S1_name}.SAFE'

    # build the path to input/output features folder
    feat_folder = BASE_DIR / f'features/{S1_name}/' # path_to_features + ID_to_process
    
    # algorithm to use for NESZ extraction, choose from ['ESA', 'NERSC']
    algorithm = 'NERSC'
    
    # overwrite existing features?
    overwrite = False
    
    # extract features from S1 
    logger.info(f'Extracting features for {S1_name}')
    extract_features(str(safe_folder), str(feat_folder), algorithm, overwrite)

