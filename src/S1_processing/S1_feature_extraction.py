# ---- This is <S1_feature_extraction.py> ----

"""
Module for extraction of Sentinel-1 features
""" 

import argparse
import os
import sys
import pathlib
import shutil

from loguru import logger

import numpy as np

from osgeo import gdal
from scipy import ndimage as ndim

import S1_processing.S1_processing_config as S1_conf
import S1_processing.S1_product_info as S1_info
import S1_processing.S1_swath_mask as S1_sm

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_S1_intensity(
    safe_folder,
    feat_folder,
    intensity,
    ML='1x1',
    dB=False,
    overwrite=False,
    dry_run=False,
    loglevel='INFO',
):

    """Extract intensity channel from S1 input image

    Parameters
    ----------
    safe_folder : path to S1 input image SAFE folder
    feat_folder : path to feature folder where output files are placed
    intensity : intensity band to extract (HH, HV, VH, VV)
    ML : multilook window size (default='1x1')
    dB : convert intensity to dB (default=False)
    overwrite : overwrite existing files (default=False)
    dry_run : do not execute actual processing (default=False)
    loglevel : loglevel setting (default='INFO')
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    logger.info('Extracting S1 intensity')

    logger.debug(f'{locals()}')
    logger.debug(f'file location: {__file__}')

    # get directory where current module is installed
    module_path = pathlib.Path(__file__).parent.parent
    logger.debug(f'module_path: {module_path}')

    # get directory where config module is installe
    # which contains snap graphs
    config_path = pathlib.Path(S1_conf.__file__).parent
    logger.debug(f'config_path: {config_path}')

# -------------------------------------------------------------------------- #

    # convert folder strings to paths
    safe_folder = pathlib.Path(safe_folder).expanduser().absolute()
    feat_folder = pathlib.Path(feat_folder).expanduser().absolute()

    logger.debug(f'intensity:   {intensity}')
    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')
    logger.debug(f'S1_conf.GPT: {S1_conf.GPT}')

    if intensity not in ['HH', 'HV', 'VH', 'VV']:
        logger.error(f'{intensity} is not a valid choice for intensity')
        raise ValueError(f'{intensity} is not a valid choice for intensity')

    if not os.path.exists(S1_conf.GPT):
        logger.error(f'Cannot find snap GPT executable: {S1_conf.GPT}')
        raise FileNotFoundError(f'Cannot find snap GPT executable: {S1_conf.GPT}')

    if not safe_folder.is_dir():
        logger.error(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')
        raise NotADirectoryError(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')

    # get S1 basename from safe_folder
    f_base = safe_folder.stem

    # build datestring
    date, datetime, datestring = S1_info.get_S1_datestring(f_base)

    # get product mode and type
    p_mode, p_type, p_pol = S1_info.get_S1_product_info(f_base)

    logger.debug(f'f_base:     {f_base}')
    logger.debug(f'date:       {date}')
    logger.debug(f'datetime:   {datetime}')
    logger.debug(f'datestring: {datestring}')
    logger.debug(f'p_mode:     {p_mode}')
    logger.debug(f'p_type:     {p_type}')
    logger.debug(f'p_pol:      {p_pol}')

    # check that product mode contains correct polarisation
    if not intensity in p_pol:
        logger.error(f'Product mode does not contain {intensity} polarisation')
        raise NameError(f'Product mode does not contain {intensity} polarisation')

# -------------------------------------------------------------------------- #

    # build db_str for output file name and define outfile_basename
    db_str = '_db' if dB else ''
    outfile_basename = f'Sigma0_{intensity}{db_str}'

    # define output file name and path
    img_path = feat_folder / f'{outfile_basename}.img'
    hdr_path = feat_folder / f'{outfile_basename}.hdr'

    logger.debug(f'img_path: {img_path}')
    logger.debug(f'hdr_path: {hdr_path}')

    # check if outfile already exists
    if img_path.is_file() and not overwrite:
        logger.info('Output file already exists, use `-overwrite` to force')
        return 

    # create feat_folder if needed
    feat_folder.mkdir(parents=True, exist_ok=True)

    # create tmp dir for snap output
    tmp_folder = feat_folder / 'tmp'
    if tmp_folder.is_dir():
        logger.debug('Removing existing tmp_folder')
        shutil.rmtree(tmp_folder)
    tmp_folder.mkdir(exist_ok=False)


    # check that given ML parameter can be interpreted
    # set looks_rg and looks_az
    try:
        looks_rg = int(ML.split('x')[0])
        looks_az = int(ML.split('x')[1])
    except:
        logger.error(f'Cannot extract looks_rg and looks_az from ML parameter: {ML}')
        logger.error(f'Expected format for ML argument: looks_rgxlooks_az')
        raise ValueError(f'Cannot extract looks_rg and looks_az from ML parameter: {ML}')

    logger.debug(f'looks_rg: {looks_rg}')
    logger.debug(f'looks_az: {looks_az}')

    if looks_rg%2==0 or looks_az%2==0:
        logger.error(
          'looks_rg and looks_az must be odd numbers'
        )
        raise ValueError(
            f'looks_rg and looks_az must be odd numbers'
        )

# -------------------------------------------------------------------------- #

    # build look_str for snap_graph_file name
    # build snap_graph_string
    look_str = '_Spk' if looks_rg>1 else ''
    snap_graph_string = \
        f'S1_conf.snap_S1_{p_mode}_{p_type}_NR_Cal{look_str}{db_str}_XX'

    logger.debug(f'snap_graph_string: {snap_graph_string}')

    # set snap_graph_file
    try:
        snap_graph_file = eval(snap_graph_string)
    except:
        logger.error('Given product mode and settings not implemented yet')
        logger.error(f'S1_processing_config has no attribute: {snap_graph_string}')
        raise NotImplementedError(f'Given product mode and settings not implemented yet')

    # build snap_graph_path
    snap_graph_path = config_path / 'snap_graphs' / snap_graph_file

    # set snap input and output files
    snap_infile  = safe_folder
    snap_outfile = tmp_folder / 'tmp.dim'

    logger.debug(f'snap_graph_path: {snap_graph_path}')
    logger.debug(f'snap_infile:     {snap_infile}')
    logger.debug(f'snap_outfile:    {snap_outfile}')

    # check that snap_graph_path exists
    if not snap_graph_path.is_file():
        logger.error(f'Cannot find snap_graph_path: {snap_graph_path}')
        raise FileNotFoundError(f'Cannot find snap_graph_path: {snap_graph_path}')

# -------------------------------------------------------------------------- #

    # build the snap graph command
    # needs double quotes around {S1_conf.GPT} to avoid issues with spaces in
    # file names on windows
    if looks_rg>1:
        snap_cmd = f'"{S1_conf.GPT}" ' + \
            f'{snap_graph_path} ' + \
            f'-PinFile={snap_infile} ' + \
            f'-PoutFile={snap_outfile} ' + \
            f'-Ppolarization={intensity} ' + \
            f'-Plooks_rg={looks_rg} ' + \
            f'-Plooks_az={looks_az}'
    else:
        snap_cmd = f'"{S1_conf.GPT}" ' + \
            f'{snap_graph_path} ' + \
            f'-PinFile={snap_infile} ' + \
            f'-PoutFile={snap_outfile} ' + \
            f'-Ppolarization={intensity}'

    logger.debug('Running snap to create snap_outfile')
    logger.debug(f"Executing: {snap_cmd}")

    # dry_run? do not execute
    if dry_run:
        logger.info('Dry-run (not performing actual processing)')
        shutil.rmtree(tmp_folder)
        return 


    # system call snap_command
    os.system(snap_cmd)

    # copy image files to feat_folder
    shutil.copyfile(tmp_folder / 'tmp.data' / f'{outfile_basename}.img', img_path)
    shutil.copyfile(tmp_folder / 'tmp.data' / f'{outfile_basename}.hdr', hdr_path)

    # remove snap tmp_dir
    shutil.rmtree(tmp_folder)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_S1_IA(
    safe_folder,
    feat_folder,
    overwrite=False,
    dry_run=False,
    loglevel='INFO',
):

    """Extract incident angle (IA) from S1 input image

    Parameters
    ----------
    safe_folder : path to S1 input image SAFE folder
    feat_folder : path to feature folder where output files are placed
    overwrite : overwrite existing files (default=False)
    dry_run : do not execute actual processing (default=False)
    loglevel : loglevel setting (default='INFO')
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    logger.info('Extracting IA')

    logger.debug(f'{locals()}')
    logger.debug(f'file location: {__file__}')

    # get directory where module is installed
    module_path = pathlib.Path(__file__).parent.parent
    logger.debug(f'module_path: {module_path}')

    # get directory where config module is installed, which contains snap graphs
    config_path = pathlib.Path(S1_conf.__file__).parent
    logger.debug(f'config_path: {config_path}')

# -------------------------------------------------------------------------- #

    # convert folder strings to paths
    safe_folder = pathlib.Path(safe_folder).expanduser().absolute()
    feat_folder = pathlib.Path(feat_folder).expanduser().absolute()

    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')
    logger.debug(f'S1_conf.GPT: {S1_conf.GPT}')

    if not os.path.exists(S1_conf.GPT):
        logger.error(f'Cannot find snap GPT executable: {S1_conf.GPT}')
        raise FileNotFoundError(f'Cannot find snap GPT executable: {S1_conf.GPT}')

    if not safe_folder.is_dir():
        logger.error(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')
        raise NotADirectoryError(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')

    # get S1 basename from safe_folder
    f_base = safe_folder.stem

    # build datestring
    date, datetime, datestring = S1_info.get_S1_datestring(f_base)

    # get product mode and type
    p_mode, p_type, p_pol = S1_info.get_S1_product_info(f_base)

    logger.debug(f'f_base:     {f_base}')
    logger.debug(f'date:       {date}')
    logger.debug(f'datetime:   {datetime}')
    logger.debug(f'datestring: {datestring}')
    logger.debug(f'p_mode:     {p_mode}')
    logger.debug(f'p_type:     {p_type}')
    logger.debug(f'p_pol:      {p_pol}')

# -------------------------------------------------------------------------- #

    # define outfile_basename
    outfile_basename = 'IA'

    # define output file name and path
    img_path = feat_folder / f'{outfile_basename}.img'
    hdr_path = feat_folder / f'{outfile_basename}.hdr'

    logger.debug(f'img_path: {img_path}')
    logger.debug(f'hdr_path: {hdr_path}')

    # check if outfile already exists
    if img_path.is_file() and not overwrite:
        logger.info('Output file already exists, use `-overwrite` to force')
        return 

    # create feat_folder if needed
    feat_folder.mkdir(parents=True, exist_ok=True)

    # create tmp dir for snap output
    tmp_folder = feat_folder / 'tmp'
    if tmp_folder.is_dir():
        logger.debug('Removing existing tmp_folder')
        shutil.rmtree(tmp_folder)
    tmp_folder.mkdir(exist_ok=False)

# -------------------------------------------------------------------------- #

    # set snap graph file
    snap_graph_file = S1_conf.snap_S1_IA

    # build snap_graph_path
    snap_graph_path = config_path / 'snap_graphs' / snap_graph_file

    # set snap input and output files
    snap_infile  = safe_folder
    snap_outfile = tmp_folder / 'tmp.dim'

    logger.debug(f'snap_graph_path: {snap_graph_path}')
    logger.debug(f'snap_infile:     {snap_infile}')
    logger.debug(f'snap_outfile:    {snap_outfile}')

    # check that snap_graph_path exists
    if not snap_graph_path.is_file():
        logger.error(f'Cannot find snap_graph_path: {snap_graph_path}')
        raise FileNotFoundError(f'Cannot find snap_graph_path: {snap_graph_path}')

# -------------------------------------------------------------------------- #

    # build the snap graph command
    # needs double quotes around {S1_conf.GPT} to avoid issues with spaces in
    # file names on windows
    snap_cmd = f'"{S1_conf.GPT}" ' + \
        f'{snap_graph_path} ' + \
        f'-PinFile={snap_infile} ' + \
        f'-PoutFile={snap_outfile}'

    logger.debug('Running snap to create snap_outfile')
    logger.debug(f'Executing: {snap_cmd}')

    # dry_run? do not execute
    if dry_run:
        logger.info('Dry-run - not performing actual processing')
        shutil.rmtree(tmp_folder)
        return 


    # system call snap_command
    os.system(snap_cmd)

    # copy image files to feat_folder
    shutil.copyfile(tmp_folder / 'tmp.data' / 'incAngle.img', img_path)
    shutil.copyfile(tmp_folder / 'tmp.data' / 'incAngle.hdr', hdr_path)

    # remove snap tmp_dir
    shutil.rmtree(tmp_folder)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_S1_lat_lon(
    safe_folder,
    feat_folder,
    overwrite=False,
    dry_run=False,
    loglevel='INFO',
):

    """Extract lat/lon from S1 input image

    Parameters
    ----------
    safe_folder : path to S1 input image SAFE folder
    feat_folder : path to feature folder where output files are placed
    overwrite : overwrite existing files (default=False)
    dry_run : do not execute actual processing (default=False)
    loglevel : loglevel setting (default='INFO')
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    logger.info('Extracting lat/lon')

    logger.debug(f'{locals()}')
    logger.debug(f'file location: {__file__}')

    # get directory where module is installed
    module_path = pathlib.Path(__file__).parent.parent
    logger.debug(f'module_path: {module_path}')

    # get directory where config module is installed, which contains snap graphs
    config_path = pathlib.Path(S1_conf.__file__).parent
    logger.debug(f'config_path: {config_path}')

# -------------------------------------------------------------------------- #

    # convert folder strings to paths
    safe_folder = pathlib.Path(safe_folder).expanduser().absolute()
    feat_folder = pathlib.Path(feat_folder).expanduser().absolute()

    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')
    logger.debug(f'S1_conf.GPT: {S1_conf.GPT}')

    if not os.path.exists(S1_conf.GPT):
        logger.error(f'Cannot find snap GPT executable: {S1_conf.GPT}')
        raise FileNotFoundError(f'Cannot find snap GPT executable: {S1_conf.GPT}')

    if not safe_folder.is_dir():
        logger.error(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')
        raise NotADirectoryError(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')

    # get S1 basename from safe_folder
    f_base = safe_folder.stem

    # build datestring
    date, datetime, datestring = S1_info.get_S1_datestring(f_base)

    # get product mode and type
    p_mode, p_type, p_pol = S1_info.get_S1_product_info(f_base)

    logger.debug(f'f_base:     {f_base}')
    logger.debug(f'date:       {date}')
    logger.debug(f'datetime:   {datetime}')
    logger.debug(f'datestring: {datestring}')
    logger.debug(f'p_mode:     {p_mode}')
    logger.debug(f'p_type:     {p_type}')
    logger.debug(f'p_pol:      {p_pol}')

# -------------------------------------------------------------------------- #

    # define outfile_basenames
    outfile_basename_1 = 'lat'
    outfile_basename_2 = 'lon'

    # define output file name and path
    img_path_1 = feat_folder / f'{outfile_basename_1}.img'
    hdr_path_1 = feat_folder / f'{outfile_basename_1}.hdr'
    img_path_2 = feat_folder / f'{outfile_basename_2}.img'
    hdr_path_2 = feat_folder / f'{outfile_basename_2}.hdr'

    logger.debug(f'img_path_1: {img_path_1}')
    logger.debug(f'hdr_path_1: {hdr_path_1}')
    logger.debug(f'img_path_2: {img_path_2}')
    logger.debug(f'hdr_path_2: {hdr_path_2}')

    # check if outfiles already exist
    if img_path_1.is_file() and img_path_2.is_file() and not overwrite:
        logger.info('Output files already exist, use `-overwrite` to force')
        return 

    # create feat_folder if needed
    feat_folder.mkdir(parents=True, exist_ok=True)

    # create tmp dir for snap output
    tmp_folder = feat_folder / 'tmp'
    if tmp_folder.is_dir():
        logger.debug('Removing existing tmp_folder')
        shutil.rmtree(tmp_folder)
    tmp_folder.mkdir(exist_ok=False)

# -------------------------------------------------------------------------- #

    # set snap graph files
    snap_graph_file_1 = S1_conf.snap_S1_lat
    snap_graph_file_2 = S1_conf.snap_S1_lon

    # build snap_graph_paths
    snap_graph_path_1 = config_path / 'snap_graphs' / snap_graph_file_1
    snap_graph_path_2 = config_path / 'snap_graphs' / snap_graph_file_2

    # set snap input and output files
    snap_infile  = safe_folder
    snap_outfile = tmp_folder / 'tmp.dim'

    logger.debug(f'snap_graph_path_1: {snap_graph_path_1}')
    logger.debug(f'snap_graph_path_2: {snap_graph_path_2}')
    logger.debug(f'snap_infile:       {snap_infile}')
    logger.debug(f'snap_outfile:      {snap_outfile}')

    # check that snap_graph_paths exists
    if not snap_graph_path_1.is_file():
        logger.error(f'Cannot find snap_graph_path_1: {snap_graph_path_1}')
        raise FileNotFoundError(f'Cannot find snap_graph_path_1: {snap_graph_path_1}')
    if not snap_graph_path_2.is_file():
        logger.error(f'Cannot find snap_graph_path_2: {snap_graph_path_2}')
        raise FileNotFoundError(f'Cannot find snap_graph_path_2: {snap_graph_path_2}')

# -------------------------------------------------------------------------- #

    # build the snap graph commands
    # needs double quotes around {S1_conf.GPT} to avoid issues with spaces in
    # file names on windows
    snap_cmd_1 = f'"{S1_conf.GPT}" ' + \
        f'{snap_graph_path_1} ' + \
        f'-PinFile={snap_infile} ' + \
        f'-PoutFile={snap_outfile}'
    snap_cmd_2 = f'"{S1_conf.GPT}" ' + \
        f'{snap_graph_path_2} ' + \
        f'-PinFile={snap_infile} ' + \
        f'-PoutFile={snap_outfile}'

    logger.debug('Running snap to create snap_outfile')
    logger.debug(f'Executing: {snap_cmd_1}')
    logger.debug(f'Executing: {snap_cmd_2}')

    # dry_run? do not execute
    if dry_run:
        logger.info('Dry-run - not performing actual processing')
        shutil.rmtree(tmp_folder)
        return 


    # system call snap_command
    os.system(snap_cmd_1)

    # copy image files to feat_folder
    shutil.copyfile(tmp_folder / 'tmp.data' / f'{outfile_basename_1}.img', img_path_1)
    shutil.copyfile(tmp_folder / 'tmp.data' / f'{outfile_basename_1}.hdr', hdr_path_1)

    # remove snap tmp_dir and create again empty
    shutil.rmtree(tmp_folder)
    tmp_folder.mkdir(exist_ok=False)


    # system call snap_command
    os.system(snap_cmd_2)

    # copy image files to feat_folder
    shutil.copyfile(tmp_folder / 'tmp.data' / f'{outfile_basename_2}.img', img_path_2)
    shutil.copyfile(tmp_folder / 'tmp.data' / f'{outfile_basename_2}.hdr', hdr_path_2)

    # remove snap tmp_dir and create again empty
    shutil.rmtree(tmp_folder)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_S1_swath_mask(
    safe_folder,
    feat_folder,
    overwrite=False,
    loglevel='INFO',
):

    """Extract swath mask from S1 input image

    Parameters
    ----------
    safe_folder : path to S1 input image SAFE folder
    feat_folder : path to feature folder where output files are placed
    overwrite : overwrite existing files (default=False)
    loglevel : loglevel setting (default='INFO')
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    logger.info('Extracting S1 swath mask')

    logger.debug(f'{locals()}')
    logger.debug(f'file location: {__file__}')

    # get directory where module is installed
    module_path = pathlib.Path(__file__).parent.parent
    logger.debug(f'module_path: {module_path}')

    # get directory where config module is installed, which contains snap graphs
    config_path = pathlib.Path(S1_conf.__file__).parent
    logger.debug(f'config_path: {config_path}')

# -------------------------------------------------------------------------- #

    # convert folder strings to paths
    safe_folder = pathlib.Path(safe_folder).expanduser().absolute()
    feat_folder = pathlib.Path(feat_folder).expanduser().absolute()

    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')

    if not safe_folder.is_dir():
        logger.error(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')
        raise NotADirectoryError(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')

    # get S1 basename from safe_folder
    f_base = safe_folder.stem

    # build datestring
    date, datetime, datestring = S1_info.get_S1_datestring(f_base)

    # get product mode and type
    p_mode, p_type, p_pol = S1_info.get_S1_product_info(f_base)

    logger.debug(f'f_base:     {f_base}')
    logger.debug(f'date:       {date}')
    logger.debug(f'datetime:   {datetime}')
    logger.debug(f'datestring: {datestring}')
    logger.debug(f'p_mode:     {p_mode}')
    logger.debug(f'p_type:     {p_type}')
    logger.debug(f'p_pol:      {p_pol}')

# -------------------------------------------------------------------------- #

    # define outfile_basename
    outfile_basename = 'swath_mask'

    # define output file name and path
    img_path = feat_folder / f'{outfile_basename}.img'
    hdr_path = feat_folder / f'{outfile_basename}.hdr'

    logger.debug(f'img_path: {img_path}')
    logger.debug(f'hdr_path: {hdr_path}')

    # check if outfile already exists
    if img_path.is_file() and not overwrite:
        logger.info('Output file already exists, use `-overwrite` to force')
        return 

    # create feat_folder if needed
    feat_folder.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------- #

    # define manifest_path
    manifest_path = safe_folder / 'manifest.safe'

    # define swath names
    if p_mode == 'EW':
        swaths = ["EW1", "EW2", "EW3", "EW4", "EW5"]
    elif p_mode == 'IW':
        swaths = ["IW1", "IW2", "IW3"]
    else:
        logger.error(f'Acquisition mode {p_mode} not implemented yet')
        raise NotImplementedError(f'Given product mode and settings not implemented yet')

    # get number of swaths
    number_of_swaths = len(swaths)

    # loop over all swaths
    for swath_number, swath_name in enumerate(swaths, 1):
        logger.debug(f'Extracting swath {swath_number}/{number_of_swaths}: {swath_name}')

        if swath_number == 1:
            swath_mask = S1_sm.get_swath_mask(manifest_path, swath_name, p_pol[0])
        else:
            swath_mask = swath_mask + (swath_number) * S1_sm.get_swath_mask(
                manifest_path, swath_name, p_pol[0]
            )

# -------------------------------------------------------------------------- #

    # write swath_mask to file

    # delete output file if it exists
    if img_path.is_file() and overwrite:
        logger.info('Remving existing output file')
        os.remove(img_path.as_posix())
        os.remove(os.path.splitext(img_path.as_posix())[0]+'.hdr')

    # get dimensions
    Ny, Nx    = swath_mask.shape

    # set number of bands and data type
    bands     = 1
    data_type =gdal.GDT_Byte
    
    # get driver
    output = gdal.GetDriverByName('Envi').Create(
        img_path.as_posix(),
        Nx,
        Ny,
        bands,
        data_type
    )

    # write to file
    output.GetRasterBand(1).WriteArray(swath_mask)

    output.FlushCache()

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def make_S1_rgb(
    feat_folder,
    result_folder,
    hhMin=-30,
    hhMax=0,
    hvMin=-35,
    hvMax=-5,
    newMin=0,
    newMax=255,
    red='HV',
    green='HH',
    blue='HH',
    overwrite=False,
    loglevel='INFO',
):

    """Scale intensity channels of S1 input image and stack to 8bit RGB

    Parameters
    ----------
    feat_folder : path to folder with input image features (linear scale)
    result_folder : path to result folder where scaled RGB file is placed
    hhMin : minimum value for scaling HH channel (default=-30),
    hhMax : maximum value for scaling HH channel (default=0),
    hvMin : minimum value for scaling HV channel (default=-35),
    hvMax : maximum value for scaling HV channel (default=-5),
    newMin : new minimum for scaled image (default=0),
    newMax : new maximum for scaled image (default=255),
    red : channel for red band (default='HV'),
    green : channel for green band (default='HH'),
    blue : channel for blue band (default='HH'),
    overwrite : overwrite existing files (default=False)
    loglevel : loglevel setting (default='INFO')
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    logger.info('Stacking to false-color RGB 8bit')

    logger.debug(f'{locals()}')
    logger.debug(f'file location: {__file__}')

    # get directory where module is installed
    module_path = pathlib.Path(__file__).parent.parent
    logger.debug(f'module_path: {module_path}')

    # get directory where config module is installed, which contains snap graphs
    config_path = pathlib.Path(S1_conf.__file__).parent
    logger.debug(f'config_path: {config_path}')

# -------------------------------------------------------------------------- #

    # convert folder strings to paths
    feat_folder   = pathlib.Path(feat_folder).expanduser().absolute()
    result_folder = pathlib.Path(result_folder).expanduser().absolute()

    # convert min and max strings to integers
    hhMin  = int(hhMin)
    hhMax  = int(hhMax)
    hvMin  = int(hvMin)
    hvMax  = int(hvMax)
    newMin = int(newMin)
    newMax = int(newMax)

    logger.debug(f'feat_folder:   {feat_folder}')
    logger.debug(f'result_folder: {result_folder}')
    logger.debug(f'hhMin:         {hhMin}')
    logger.debug(f'hhMax:         {hhMax}')
    logger.debug(f'hvMin:         {hvMin}')
    logger.debug(f'hvMax:         {hvMax}')
    logger.debug(f'newMin:        {newMin}')
    logger.debug(f'newMax:        {newMax}')
    logger.debug(f'red:           {red}')
    logger.debug(f'green:         {green}')
    logger.debug(f'blue:          {blue}')

    if not feat_folder.is_dir():
        logger.error(f'Cannot find feat_folder: {feat_folder}')
        raise NotADirectoryError(f'Cannot find feat_folder: {feat_folder}')

    # get S1 basename from safe_folder
    f_base = feat_folder.stem

    # build datestring
    date, datetime, datestring = S1_info.get_S1_datestring(f_base)

    # get product mode and type
    p_mode, p_type, p_pol = S1_info.get_S1_product_info(f_base)

    logger.debug(f'f_base:     {f_base}')
    logger.debug(f'date:       {date}')
    logger.debug(f'datetime:   {datetime}')
    logger.debug(f'datestring: {datestring}')
    logger.debug(f'p_mode:     {p_mode}')
    logger.debug(f'p_type:     {p_type}')
    logger.debug(f'p_pol:      {p_pol}')

# -------------------------------------------------------------------------- #

    # define output file name and path
    img_path = result_folder / f'{f_base}_rgb.tif'

    logger.debug(f'img_path: {img_path}')

    # check if outfile already exists
    if img_path.is_file() and not overwrite:
        logger.info('Output file already exists, use `-overwrite` to force')
        return 

    # create result_folder if needed
    result_folder.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------- #

    # define input file paths (Sigma0_HH and Sigma0_HV)
    HH_path = feat_folder / 'Sigma0_HH.img'
    HV_path = feat_folder / 'Sigma0_HV.img'

    logger.debug(f'HH_path: {HH_path}')
    logger.debug(f'HV_path: {HV_path}')

    # check that HH_path exists
    if not HH_path.exists():
        logger.error(f'Cannot find HH_path: {HH_path}')
        raise FileNotFoundError(f'Cannot find HH_path: {HH_path}')

    # check that HV_path exists
    if not HV_path.exists():
        logger.error(f'Cannot find HV_path: {HV_path}')
        raise FileNotFoundError(f'Cannot find HV_path: {HV_path}')

# -------------------------------------------------------------------------- #

    logger.info('Loading HH and HV images')

    # load HH and HV
    HH = gdal.Open(HH_path.as_posix()).ReadAsArray()
    HV = gdal.Open(HV_path.as_posix()).ReadAsArray()

    # check that HH and HV dimensions match
    if HH.shape != HV.shape:
        logger.error('Intensity channels must have the same array shape')
        raise ValueError(f'Intensity channels must have the same array shape')

    # convert to dB
    logger.info('Converting HH and HV to dB')
    HH_db = 10*np.log10(HH)
    HV_db = 10*np.log10(HV)

    # clip to min and max
    HH_db[HH_db<hhMin] = hhMin
    HH_db[HH_db>hhMax] = hhMax
    HV_db[HV_db<hvMin] = hvMin
    HV_db[HV_db>hvMax] = hvMax

    # scale both channels
    logger.info('Scaling HH and HV channel individually')
    HH_scaled = (HH_db - (hhMin)) * ((newMax - newMin) / ((hhMax) - (hhMin))) + newMin
    HV_scaled = (HV_db - (hvMin)) * ((newMax - newMin) / ((hvMax) - (hvMin))) + newMin

    # assign to RGB channels
    if red == 'HV':
        r = HV_scaled
    elif red == 'HH':
        r = HH_scaled
    elif red == 'zero':
        r = np.zeros(HH_db.shape)

    if green == 'HV':
        g = HV_scaled
    elif green == 'HH':
        g = HH_scaled
    elif green == 'zero':
        g = np.zeros(HH_db.shape)

    if blue == 'HV':
        b = HV_scaled
    elif blue == 'HH':
        b = HH_scaled
    elif blue == 'zero':
        b = np.zeros(HH_db.shape)

    logger.info(f'Stacking to RGB: red:{red}, green:{green}, blue:{blue}')

    # stack all channels to one array
    RGB = np.stack((r,g,b),0)

# -------------------------------------------------------------------------- #

    # write rgb to file

    # delete output file if it exists
    if img_path.is_file() and overwrite:
        logger.info('Removing existing output file')
        os.remove(img_path.as_posix())

    # get bands and dimensions (bands should be 3)
    bands, Ny, Nx = RGB.shape

    # set data type
    data_type =gdal.GDT_Byte
    
    # get driver
    output = gdal.GetDriverByName('GTiff').Create(
        img_path.as_posix(),
        Nx,
        Ny,
        bands,
        data_type
    )

    # write to file
    for b in np.arange(bands):
        output.GetRasterBand(int(b+1)).WriteArray(RGB[b,:,:])

    output.FlushCache()

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <S1_feature_extraction.py> ----
