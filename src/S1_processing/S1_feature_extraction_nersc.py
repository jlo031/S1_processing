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

def get_IA(path_to_safe):
    ''' Extract incident angle band from a S1 SAFE product using Nansat package.

    Parameters
    ----------
    path_to_safe : string
        path/to/SAFE

    Returns
    -------
    s1_IA : float32 numpy array
        Raster with incident angle corresponding to SAFE product.

    '''
    # convert folder/file strings to paths  
    safe_folder = Path(path_to_safe).expanduser().absolute()

    # perform checks
    if not safe_folder.is_dir():     
        logger.error(f'Cannot find SAFE folder: {safe_folder}')     
        raise FileNotFoundError(f'Cannot find SAFE folder: {safe_folder}') 
    
    # create s1 object using Nansat package
    s1 = Sentinel1Image(safe_folder.as_posix())
    
    # extract IA from s1 object
    s1_IA = s1['incidence_angle']
    # convert to float32
    s1_IA = s1_IA.astype(np.float32)

    return s1_IA

def get_sigma0(path_to_safe, 
               polarization, 
               denoising_algorithm='NERSC',
               dB=True):
    ''' Extract Sigma0 band from S1 SAFE folder for a specific polarization.

    Parameters
    ----------
    path_to_safe : string
        path/to/SAFE
    polarization : string
        for which polarization to extract (HH, HV, VH, VV)
    denoising_algorithm : string, optional
        Which denoising algorithm to use (ESA or NERSC). The default is 'NERSC'.
    dB : boolean, optional
        Return sigma0 values in decibels. The default is True.

    Returns
    -------
    sigma0_denoised : float32 numpy array
        Denoised Sigma0 values for specified polarization.

    '''
    # convert folder/file strings to paths  
    safe_folder = Path(path_to_safe).expanduser().absolute()
    
    # perform checks
    if not safe_folder.is_dir():     
        logger.error(f'Cannot find SAFE folder: {safe_folder}')     
        raise FileNotFoundError(f'Cannot find SAFE folder: {safe_folder}') 
        
    if polarization not in ['HH', 'HV', 'VH', 'VV']:
        logger.error(f'{polarization} is not a valid choice for polarization')
        raise ValueError(f'{polarization} is not a valid choice for polarization')
    
    if denoising_algorithm not in ['ESA', 'NERSC']:
        logger.error(f'{denoising_algorithm} is not a valid choice for denoising_algorithm')
        raise ValueError(f'{denoising_algorithm} is not a valid choice for denoising_algorithm')
        
    # create s1 object using Nansat package
    s1 = Sentinel1Image(safe_folder.as_posix)
    
    # run thermal noise correction with the ESA or NERSC algorithm
    sigma0_denoised = s1.remove_thermal_noise(polarization, denoising_algorithm)
    
    if dB:
        logger.info('Converting Sigma0 intensities to decibels.')
        # convert to dB
        sigma0_denoised = 10 * np.log10(sigma0_denoised)
    
    # convert to float32
    sigma0_denoised = sigma0_denoised.astype(np.float32)
    
    return sigma0_denoised
    
    
def extract_features(path_to_safe, path_to_features, denoising_algorithm = 'NERSC', dB = True, overwrite = False):
    """Extract the following features from S1 EW GRDM SAFE product: 
        1) IA
        2) denoised sigma_0 intensity values for HH and HV channels (with either ESA or NERSC denoising algorithm) 
        3) S1 swath mask

    Args:
        path_to_safe (string): /path/to/safe.SAFE
        path_to_features (string): /path/to/features
        denoising_algorithm (string): 'NERSC' or 'ESA' algorithm to extract the NESZ (default = 'NERSC')
        dB (boolean): convert intensity (sigma0) to dB (default = True)
        overwrite (boolean): overwrite existing files (default = False)
    """
    # convert folder/file strings to paths  
    safe_folder = Path(path_to_safe).expanduser().absolute()
    feat_folder = Path(path_to_features).expanduser().absolute()
    
    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')
    
    # folder checks
    if not safe_folder.is_dir():     
        logger.error(f'Cannot find SAFE folder: {safe_folder}')     
        raise FileNotFoundError(f'Cannot find SAFE folder: {safe_folder}')   
    
    if not feat_folder.is_dir():
        feat_folder.mkdir(exist_ok=True, parents=True)
        logger.info(f'Created feat_folder: {feat_folder}')
        
    if denoising_algorithm == 'ESA':
        files_to_check = ["IA.tif", "Sigma0_HH_ESA_db.tif","Sigma0_HV_ESA_db.tif", "swath_mask.tif"]

    if denoising_algorithm == 'NERSC':
        files_to_check = ["IA.tif", "Sigma0_HH_NERSC_db.tif","Sigma0_HV_NERSC_db.tif", "swath_mask.tif"]
    
    files_not_exist = [files for files in files_to_check if not os.path.isfile(path_to_features+'/'+files)]
    
    if (files_not_exist == [] and not overwrite):
        logger.info(f"Features already exist: {files_to_check}. Set overwrite to True to extract features anew.")
    
    if (files_not_exist == [] and overwrite):
        logger.info("Overwriting existing features!")
        files_not_exist = files_to_check

# ----------------------------------------------------------------- 
    # EXTRACT INCIDENT ANGLE
    
    if not (feat_folder / "IA.tif").is_file():
        logger.info("Extracting incidence_angle")
        
        s1_IA = get_IA(safe_folder.as_posix())
        write_to_tif(s1_IA, (feat_folder / 'IA.tif').as_posix())
        
    elif (feat_folder / "IA.tif").is_file() and overwrite:
        logger.info('Overwriting existing IA.tif')
        
        s1_IA = get_IA(safe_folder.as_posix())
        write_to_tif(s1_IA, (feat_folder / 'IA.tif').as_posix())
        
    else:
        logger.info('IA already extracted, set overwrite=True to extract again')
            
# -----------------------------------------------------------------   
    # EXTRACT INTENSITY BANDS
    
    for polarization in ['HH', 'HV']:
        if not (feat_folder / f"Sigma0_{polarization}_{denoising_algorithm}_db.tif").is_file():
            logger.info(f'Denoising {polarization} channel with {denoising_algorithm} algorithm')
            
            sigma0_denoised = get_sigma0(safe_folder.as_posix(), 
                                         polarization, 
                                         denoising_algorithm, 
                                         dB)
            
            # save to tif
            if dB:
                write_to_tif(sigma0_denoised, (feat_folder / f'Sigma0_{polarization}_{denoising_algorithm}_db.tif').as_posix())
            else:
                write_to_tif(sigma0_denoised, (feat_folder / f'Sigma0_{polarization}_{denoising_algorithm}.tif').as_posix())
                
        elif (feat_folder / f"Sigma0_{polarization}_{denoising_algorithm}_db.tif").is_file() and overwrite:
            logger.info(f'Overwriting existing Sigma0 {polarization} channel. Denoising {polarization} channel with {denoising_algorithm} algorithm')
            
            sigma0_denoised = get_sigma0(safe_folder.as_posix(), 
                                         polarization, 
                                         denoising_algorithm, 
                                         dB)
            
            # save to tif
            if dB:
                write_to_tif(sigma0_denoised, (feat_folder / f'Sigma0_{polarization}_{denoising_algorithm}_db.tif').as_posix())
            else:
                write_to_tif(sigma0_denoised, (feat_folder / f'Sigma0_{polarization}_{denoising_algorithm}.tif').as_posix())
        
        else:
            logger.info(f'Denoised {polarization} channel already extracted, set overwrite=True to extract again')

        
    # -----------------------------------------------------------------      
    # EXTRACT S1 SWATH MASK
    
    if not (feat_folder / "swath_mask.tif").is_file():
        logger.info("Extracting swath mask")
        
        get_full_S1_swath_mask(safe_folder.as_posix(), 
                               feat_folder.as_posix(), 
                               overwrite=overwrite) 

    elif (feat_folder / "swath_mask.tif").is_file() and overwrite:
        logger.info('Overwriting existing swath mask')
        
        get_full_S1_swath_mask(safe_folder.as_posix(), 
                               feat_folder.as_posix(), 
                               overwrite=overwrite)
        
    else:
        logger.info('Swath mask already extracted, set overwrite=True to extract again')
               
            
