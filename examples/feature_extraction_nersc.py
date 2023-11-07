''' 
Script showing how to extract S1 features needed to train or run inference on CNN network.

Features extracted: 
    - Sigma0 in dB for HH and HV, denoised with either ESA or NERSC algorithm
    - incident angle (IA)
    - swath mask
All extracted features are saved in tif format in the 'features' folder.
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

