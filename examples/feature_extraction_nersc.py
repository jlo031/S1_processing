''' 
Extract the following features from S1 EW GRDM SAFE product: 
        1) IA
        2) denoised sigma_0 intensity values for HH and HV channels (with either ESA or NERSC denoising algorithm) 
        3) swath mask
        4) lat/lon bands

Features 1-3 are saved in tif format, feature 4 (lat/lon bands) is saved in ENVI format.
'''

import S1_processing.S1_feature_extraction_nersc as S1_feat
from pathlib import Path
from loguru import logger
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# define the basic data directory for your project
BASE_DIR = Path('/scratch/cta014/Sentinel1/CNN_ice_water/inference')

# define the level 1 (L1) data directory (i.e.where SAFE folders are stored)
BASE_L1 = BASE_DIR / 'originals'

# read in list of S1 basenames to process
S1_list = open((BASE_DIR / 'S1_imagelist_inference.txt'), 'r')
ID_to_process = S1_list.read().splitlines()

#ID_to_process = ID_to_process[0]

for S1_name in ID_to_process:

    # build the path to S1 SAFE folder
    safe_folder = BASE_L1 / f'{S1_name}.SAFE'

    # build the path to input/output features folder
    feat_folder = BASE_DIR / f'features/{S1_name}/' # path_to_features + ID_to_process
    
    # algorithm to use for NESZ extraction, choose from ['ESA', 'NERSC']
    algorithm = 'NERSC'
    
    # convert Sigma0 values to decibels
    dB = True
    
    # overwrite existing features?
    overwrite = False
    
    # extract features from S1 
    logger.info(f'Extracting features for {S1_name}')
    
    S1_feat.extract_features(safe_folder, 
                             feat_folder, 
                             denoising_algorithm = algorithm, 
                             dB = dB,
                             overwrite = overwrite)

