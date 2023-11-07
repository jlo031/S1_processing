# ---- This is <S1_swath_mask.py> ----

"""
Creating swath-masks for Sentinel-1 EW images

Adapted from Thomas Kramer.
"""

from loguru import logger
import sys
from pathlib import Path
import tifffile as tf
import numpy as np

from S1_processing.S1_product_info import get_S1_product_info

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- # 

def annotation_path_from_manifest_path(manifest_path, polarization):
  """Get annotation path for S1 input manifest.safe file.

  Parameters
  ----------
  manifest_path : path to manifest.safe input file
  polarization : wanted polarization

  Returns
  -------
  annotation_path : path to annotation folder of input image
  """

  import os
  import glob

  product_folder = os.path.dirname(manifest_path)
  annotation_path = glob.glob(
    os.path.join(
      product_folder,
      'annotation',
      f's1*{polarization.lower()}*.xml'
    )
  )[0]

  return annotation_path

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- # 

def get_swath_mask(manifest_path, swath, polarization):
  """ Get swath mask for S1 EW image

  Parameters
  ----------
  manifest_path : path to manifest.safe input file
  swath : wanted swath
  polarization : wanted polarization

  Returns
  -------
  mask : swath mask

  Examples
  --------
  mask = get_swath_mask(manifest_path, 'EW1', 'HH')
  """

  from numpy import uint8, zeros, ma
  from lxml import etree

  assert polarization.upper() in ['HH', 'HV', 'VH', 'VV'], \
    'Not a valid input polarisation.'

  annotation_path = annotation_path_from_manifest_path(
    manifest_path, polarization.lower()
  )

  with open(annotation_path, 'r') as f:
    xml = etree.parse(f)

  rows = int(xml.xpath('//*/numberOfLines')[0].text)
  cols = int(xml.xpath('//*/numberOfSamples')[0].text)

  mask = zeros((rows, cols), dtype=uint8)

  swathBoundsXml = xml.xpath(
    '//*/swathBounds[../../swath/text() = "{swath}"]'.format(swath=swath)
  )

  for sb_xml in swathBoundsXml:
    y1 = int(sb_xml.xpath('firstAzimuthLine')[0].text)
    y2 = int(sb_xml.xpath('lastAzimuthLine')[0].text)
    x1 = int(sb_xml.xpath('firstRangeSample')[0].text)
    x2 = min(int(sb_xml.xpath('lastRangeSample')[0].text) + 1, cols)
    mask[y1:y2+1, x1:x2] = True

  return mask

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_full_S1_swath_mask(safe_folder, feat_folder, overwrite=False, loglevel='INFO'):

    """Extract full swath mask for a S1 EW input image and save to tiff

    Parameters
    ----------
    safe_folder : path to S1 input image SAFE folder
    feat_folder : path to feature folder where output tif file is placed
    overwrite : overwrite existing files (default=False)
    """
    
    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)
    
    logger.info('Extracting S1 swath mask')
    
    # -------------------------------------------------------------------------- #
    
    # convert folder strings to paths
    safe_folder = Path(safe_folder).expanduser().absolute()
    feat_folder = Path(feat_folder).expanduser().absolute()
    
    logger.debug(f'safe_folder: {safe_folder}')
    logger.debug(f'feat_folder: {feat_folder}')
    
    if not safe_folder.is_dir():
        logger.error(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')
        raise NotADirectoryError(f'Cannot find Sentinel-1 SAFE folder: {safe_folder}')
    
    # get S1 basename from safe_folder
    f_base = safe_folder.stem
    
    # get product mode and type
    p_mode, p_type, p_pol = get_S1_product_info(f_base)
    
    # define manifest_path
    manifest_path = safe_folder / 'manifest.safe'
    
    # define outfile_basename
    outfile_basename = 'swath_mask'
    
    # define output file name and path
    outfile_tif_path = feat_folder / f'{outfile_basename}.tif'
    
    # check if outfile already exists
    if outfile_tif_path.is_file() and not overwrite:
        logger.info('Output file: {outfile_tif_path} already exists, use `-overwrite` to force')
        return 

    # create feat_folder if needed
    feat_folder.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------------------- #
    
    # define swath names
    swaths = ["EW1", "EW2", "EW3", "EW4", "EW5"]
    
    # get number of swaths
    number_of_swaths = len(swaths)
    
    # loop over all swaths
    for swath_number, swath_name in enumerate(swaths, 1):
        logger.debug(f'Extracting swath {swath_number}/{number_of_swaths}: {swath_name}')
    
        if swath_number == 1:
            swath_mask = get_swath_mask(manifest_path, swath_name, p_pol[0])
        else:
            swath_mask = swath_mask + (swath_number) * get_swath_mask(
                manifest_path, swath_name, p_pol[0]
            )
            
  # -------------------------------------------------------------------------- #

    # write swath_mask to disk
    tf.imsave(outfile_tif_path.as_posix(), swath_mask, dtype=np.uint8)
       
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #    

# ---- End of <S1_swath_mask.py> ----
