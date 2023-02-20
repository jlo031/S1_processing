# ---- This is <S1_swath_mask.py> ----

"""
Creating swath-masks for Sentinel-1 EW images

Adapted from Thomas Kramer.
"""

from loguru import logger

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

# ---- End of <S1_swath_mask.py> ----
