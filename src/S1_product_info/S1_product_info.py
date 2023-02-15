# ---- This is <S1_product_info.py> ----

"""
Collection of simple function snippets to work with S1 data.
"""

import os
from loguru import logger

from osgeo import gdal

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_S1_datestring(f_base):
    """Build datestring from S1 basename.

    Parameters
    ----------
    f_base : S1 input basename

    Returns
    -------
    date : datestring
    datetime : datetime string
    datestring : datestring for figure labeling

    Examples
    --------
    date, datetime, datestring = get_S1_datestring(f_base)
    """

    try:
        datetime = f_base.split('_')[4]
        date     = datetime[0:8]

        yyyy = datetime[0:4];
        mm   = datetime[4:6]
        dd   = datetime[6:8]
        HH   = datetime[9:11]
        MM   = datetime[11:13]
        SS   = datetime[13:15]
        datestring = yyyy + '/' + mm + '/' + dd + ', ' + HH + ':' + MM

    except:
        logger.warning('Unable to extract date and time from f_base. Use S1 naming conventions.')
        date, datetime, datestring = [], [], []

    return date, datetime, datestring

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_S1_product_info(f_base):
    """Get product info from S1 basename.

    Parameters
    ----------
    f_base : S1 input basename

    Returns
    -------
    product_mode : product mode
    product_type : product type
    product_pols : product polarisation

    Examples
    --------
    product_mode, product_type, product_pols = get_S1_product_info(f_base)
    """

    try:
        product_mode = f_base.split('_')[1]
        product_type = f_base.split('_')[2]
        product_pol  = f_base.split('_')[3]

    except:
        logger.error('Unable to extract product info from f_base. Use S1 naming conventions.')
        product_mode, product_type, product_pols = [], [], []
        return product_mode, product_type, product_pols

    logger.debug(f'product_mode: {product_mode}')
    logger.debug(f'product_type: {product_type}')
    logger.debug(f'product_pol:  {product_pol}')

    # build polarisations from string
    if product_pol == '1SDH':
        product_pols = ['HH', 'HV']
    elif product_pol == '1SSH':
        product_pols = ['HH']
    elif product_pol == '1SDV':
        product_pols = ['VV', 'VH']
    elif product_pol == '1SSV':
        product_pols = ['VV']
    else:
        logger.error(f'Unknown polarization string: {product_pol}')
        product_mode, product_type, product_pols = [], [], []
        return product_mode, product_type, product_pols


    if product_mode not in ['SM', 'IW', 'EW', 'WV']:
        logger.error('Unable to extract product info from f_base. Use S1 naming conventions.')
        product_mode, product_type, product_pols = [], [], []
        return product_mode, product_type, product_pols

    return product_mode, product_type, product_pols

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_S1_zip_name(f_base):
    """Build zip-file name and manifest.safe file name from S1 basename.

    Parameters
    ----------
    f_base : S1 input file basename

    Returns
    -------
    zip_file : zip-file name
    safe_file : manifest.safe file name

    Examples
    --------
    zip_file, safe_file = get_S1_zip_name(f_base)
    """

    zip_file  = f_base + '.zip'
    safe_file = f_base + '.SAFE/' + 'manifest.safe'

    return zip_file, safe_file

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_img_dimensions(img_path):
    """Get dimensions of image in img_path

    Parameters
    ----------
    img_path : path to img file

    Returns
    -------
    Nx : pixels in x
    Ny : pixels in y

    Examples
    --------
    Nx, Ny = get_img_dimensions(img_path)
    """

    img = gdal.Open(img_path)
    Nx  = img.RasterXSize
    Ny  = img.RasterYSize
    img = None

    return Nx, Ny

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <S1_product_info.py> ----
