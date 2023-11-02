"""
Extract features from S1 SAFE folder using 'sentinel1denoised' package from the Nansen Center (NERSC)
"""

from s1denoise import Sentinel1Image

from pathlib import Path
import numpy as np
import os
from loguru import logger

from S1_processing.S1_swath_mask import get_full_S1_swath_mask
from S1_processing.write_raster_to_tif import write_to_tif

def extract_features(path_to_safe, path_to_features, algorithm_nesz = 'NERSC', overwrite = False):
    """Extracts the following features from S1 EW GRDM products: 
        1) IA
        2) denoised sigma_0 values for HH and HV channels (with either ESA or NERSC algorithm) in decibels (db)
        3) S1 swath mask

    Args:
        path_to_safe (_type_): /path/to/safe.SAFE
        path_to_features (_type_): /path/to/features
        algorithm_nesz : 'NERSC' or 'ESA' algorithm to extract the NESZ (default = 'NERSC')
    """
    # convert folder/file strings to paths  
    safe_folder = Path(path_to_safe).expanduser().absolute()
    feat_folder = Path(path_to_features).expanduser().absolute()
    
    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')
    
    if not safe_folder.is_dir():     
        logger.error(f'Cannot find SAFE folder: {safe_folder}')     
        raise FileNotFoundError(f'Cannot find SAFE folder: {safe_folder}')   
    
    if not feat_folder.is_dir():
        feat_folder.mkdir(exist_ok=True, parents=True)
        logger.info(f'Created feat_folder: {feat_folder}')
        
    if algorithm_nesz == 'ESA':
        files_to_check = ["IA.tif", "Sigma0_HH_ESA_db.tif","Sigma0_HV_ESA_db.tif", "swath_mask.tif"]

    if algorithm_nesz == 'NERSC':
        files_to_check = ["IA.tif", "Sigma0_HH_NERSC_db.tif","Sigma0_HV_NERSC_db.tif", "swath_mask.tif"]
    
    files_not_exist = [files for files in files_to_check if not os.path.isfile(path_to_features+'/'+files)]
    
    if (files_not_exist == [] and not overwrite):
        logger.info(f"Features already exist: {files_to_check}. Set overwrite to True to extract features anew.")
    
    if (files_not_exist == [] and overwrite):
        logger.info("Overwriting existing features!")
        files_not_exist = files_to_check

# ----------------------------------------------------------------- 
    # FEATURE EXTRACTION
    s1 = Sentinel1Image(safe_folder.as_posix())

    # extract incident angle
    if not (feat_folder / "IA.tif").is_file():
        logger.info("Extracting incidence_angle")
        s1_IA = s1['incidence_angle']
        s1_IA = s1_IA.astype(np.float32)
        write_to_tif(s1_IA, (feat_folder / 'IA.tif').as_posix())
        
    elif (feat_folder / "IA.tif").is_file() and overwrite:
        logger.info('Overwriting existing IA.tif')
        s1_IA = s1['incidence_angle']
        s1_IA = s1_IA.astype(np.float32)        
        write_to_tif(s1_IA, (feat_folder / 'IA.tif').as_posix())
        
    else:
        logger.info('IA already extracted, set overwrite=True to extract again')
            
    # -----------------------------------------------------------------   
    # EXTRACT + DENOISE HH and HV bands
    for polarization in ['HH', 'HV']:
        if not (feat_folder / f"Sigma0_{polarization}_{algorithm_nesz}_db.tif").is_file():
            logger.info(f'Denoising {polarization} channel with {algorithm_nesz} algorithm')
            
            # run thermal noise correction with the ESA or NERSC algorithm
            sigma0_denoised = s1.remove_thermal_noise(polarization, algorithm_nesz)
            
            # convert to dB
            sigma0_denoised_db = 10 * np.log10(sigma0_denoised)
            sigma0_denoised_db = sigma0_denoised_db.astype(np.float32)
            
            # save to tif
            write_to_tif(sigma0_denoised_db, (feat_folder / f'Sigma0_{polarization}_{algorithm_nesz}_db.tif').as_posix())
        
        elif (feat_folder / f"Sigma0_{polarization}_{algorithm_nesz}_db.tif").is_file() and overwrite:
            logger.info(f'Overwriting existing Sigma0 {polarization} channel. Denoising {polarization} channel with {algorithm_nesz} algorithm')
            
            # run thermal noise correction with the ESA or NERSC algorithm
            sigma0_denoised = s1.remove_thermal_noise(polarization, algorithm_nesz)
            
            # convert to dB
            sigma0_denoised_db = 10 * np.log10(sigma0_denoised)
            sigma0_denoised_db = sigma0_denoised_db.astype(np.float32)
            
            # save to tif
            write_to_tif(sigma0_denoised_db, (feat_folder / f'Sigma0_{polarization}_{algorithm_nesz}_db.tif').as_posix())
        
        else:
            logger.info(f'Denoised {polarization} channel already extracted, set overwrite=True to extract again')

        
    # -----------------------------------------------------------------      
    # EXTRACT S1 SWATH MASK
    
    if not (feat_folder / "swath_mask.tif").is_file():
        logger.info("Extracting swath mask")
        get_full_S1_swath_mask(safe_folder.as_posix(), feat_folder.as_posix(), overwrite=overwrite) 

    elif (feat_folder / "swath_mask.tif").is_file() and overwrite:
        logger.info('Overwriting existing swath mask')
        get_full_S1_swath_mask(safe_folder.as_posix(), feat_folder.as_posix(), overwrite=overwrite)
        
    else:
        logger.info('Swath mask already extracted, set overwrite=True to extract again')
               
            
