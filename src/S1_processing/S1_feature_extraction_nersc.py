"""
Extract features from S1 SAFE folder using 'sentinel1denoised' package from the Nansen Center (NERSC)
"""

from s1denoise import Sentinel1Image

from pathlib import Path
import numpy as np
from loguru import logger

from S1_processing.S1_swath_mask import get_full_S1_swath_mask
from S1_processing.write_raster_to_tif import write_to_tif
import S1_processing.S1_feature_extraction as S1_feat

def get_IA_nersc(path_to_safe,
                 path_to_features,
                 overwrite=False,
                 loglevel='INFO'):
    
    ''' Extract incident angle band from a S1 SAFE product using Nansat package.

    Parameters
    ----------
    path_to_safe : string
        path/to/SAFE
    path_to_features : string
        path/to/feature/folder  
    overwrite: boolean, optional
        Overwrite existing files.
    loglevel : string
        Loglevel setting (default='INFO')
        
    Returns
    -------
    - : IA band saved as tif file
        

    '''
    # convert folder/file strings to paths  
    safe_folder = Path(path_to_safe).expanduser().absolute()
    feat_folder = Path(path_to_features).expanduser().absolute()
    
    # perform checks
    if not safe_folder.is_dir():     
        logger.error(f'Cannot find SAFE folder: {safe_folder}')     
        raise FileNotFoundError(f'Cannot find SAFE folder: {safe_folder}') 
    
    if not feat_folder.is_dir():
        feat_folder.mkdir(exist_ok=True, parents=True)
        logger.info(f'Created feat_folder: {feat_folder}')
    
    # define output file name
    outfile_basename = 'IA'
    
    # define output path
    tif_path = feat_folder / f'{outfile_basename}.tif'    
    
    # check if outfile already exists
    if tif_path.is_file() and not overwrite:
        logger.info('Output file already exists, use `-overwrite` to force')
        return
    
    # create s1 object using Nansat package
    s1 = Sentinel1Image(safe_folder.as_posix())
    
    # extract IA from s1 object
    s1_IA = s1['incidence_angle']
    
    # convert to float32
    s1_IA = s1_IA.astype(np.float32)

    # write IA band to tif file
    write_to_tif(s1_IA, (feat_folder / 'IA.tif'))
    
    return

def get_sigma0_nersc(path_to_safe, 
                     path_to_features,
                     polarization, 
                     denoising_algorithm='NERSC',
                     dB=True,
                     overwrite=False,
                     loglevel='INFO'):
    
    ''' Extract Sigma0 band from S1 SAFE folder for a specific polarization.

    Parameters
    ----------
    path_to_safe : string
        path/to/SAFE
    path_to_features : string
        path/to/feature/folder    
    polarization : string
        for which polarization to extract (HH, HV, VH, VV)
    denoising_algorithm : string, optional
        Which denoising algorithm to use (ESA or NERSC). The default is 'NERSC'.
    dB : boolean, optional
        Return sigma0 values in decibels. The default is True.
    overwrite: boolean, optional
        Overwrite existing files.
    loglevel : string
        Loglevel setting (default='INFO')
        
    Returns
    -------
    - : Nothing returned, sigma0 band saved as tif file

    '''
    # convert folder/file strings to paths  
    safe_folder = Path(path_to_safe).expanduser().absolute()
    feat_folder = Path(path_to_features).expanduser().absolute()
    
    # perform checks
    if not safe_folder.is_dir():     
        logger.error(f'Cannot find SAFE folder: {safe_folder}')     
        raise FileNotFoundError(f'Cannot find SAFE folder: {safe_folder}') 
    
    if not feat_folder.is_dir():
        feat_folder.mkdir(exist_ok=True, parents=True)
        logger.info(f'Created feat_folder: {feat_folder}')
            
    if polarization not in ['HH', 'HV', 'VH', 'VV']:
        logger.error(f'{polarization} is not a valid choice for polarization')
        raise ValueError(f'{polarization} is not a valid choice for polarization')
    
    if denoising_algorithm not in ['ESA', 'NERSC']:
        logger.error(f'{denoising_algorithm} is not a valid choice for denoising_algorithm')
        raise ValueError(f'{denoising_algorithm} is not a valid choice for denoising_algorithm')
     
    # build db_str for output file name and define outfile_basename
    db_str = '_db' if dB else ''
    outfile_basename = f'Sigma0_{polarization}_{denoising_algorithm}{db_str}'
    
    # define output path
    tif_path = feat_folder / f'{outfile_basename}.tif'
    
    # check if outfile already exists
    if tif_path.is_file() and not overwrite:
        logger.info('Output file already exists, use `-overwrite` to force')
        return
    
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
    
    # save to tif
    write_to_tif(sigma0_denoised, tif_path.as_posix())
    
    return
    
    
def extract_features(path_to_safe, 
                     path_to_features, 
                     denoising_algorithm = 'NERSC', 
                     dB = True, 
                     overwrite = False,
                     loglevel='INFO'):
    
    """Extract the following features from S1 EW GRDM SAFE product: 
        1) IA
        2) denoised sigma_0 intensity values for HH and HV channels (with either ESA or NERSC denoising algorithm) 
        3) swath mask
        4) lat/lon bands

    Args:
        path_to_safe (string): /path/to/safe.SAFE
        path_to_features (string): /path/to/features
        denoising_algorithm (string): 'NERSC' or 'ESA' algorithm to extract the NESZ (default = 'NERSC')
        dB (boolean): convert intensity (sigma0) to dB (default = True)
        overwrite (boolean): overwrite existing files (default = False)
        loglevel : string
            Loglevel setting (default='INFO')
    """
    # convert folder/file strings to paths  
    safe_folder = Path(path_to_safe).expanduser().absolute()
    feat_folder = Path(path_to_features).expanduser().absolute()
    
    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')

# ----------------------------------------------------------------- 
    # EXTRACT INCIDENT ANGLE
    
    logger.info("Extracting incidence_angle")
    get_IA_nersc(safe_folder, 
                 feat_folder)
            
# -----------------------------------------------------------------   
    # EXTRACT INTENSITY BANDS
    
    for polarization in ['HH', 'HV']:

        logger.info(f'Denoising {polarization} channel with {denoising_algorithm} algorithm')
        
        get_sigma0_nersc(safe_folder, 
                         feat_folder,
                         polarization, 
                         denoising_algorithm=denoising_algorithm, 
                         dB=dB,
                         overwrite=overwrite,
                         loglevel=loglevel)

        
# -----------------------------------------------------------------      
    # EXTRACT S1 SWATH MASK
    logger.info("Extracting swath mask")
    
    get_full_S1_swath_mask(safe_folder, 
                           feat_folder, 
                           overwrite=overwrite,
                           loglevel=loglevel) 
               
    # -----------------------------------------------------------------      
    # EXTRACT S1 LAT/LON BANDS
    
    logger.info("Extracting lat/lon bands")
    
    # extract lat/lon bands
    S1_feat.get_S1_lat_lon(safe_folder,
                           feat_folder,
                           loglevel=loglevel)

    return