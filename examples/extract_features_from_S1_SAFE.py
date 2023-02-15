# ---- This is <extract_features_from_S1_SAFE.py> ----

"""
Example for easy use of 'S1_processing' library for feature extraction.
"""

import pathlib

import S1_feature_extraction as S1_feat

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# define the basic data directory for your project
BASE_DIR = pathlib.Path('/home/jo/data/Sentinel-1/')

# build the path to S1 SAFE folder
safe_folder = BASE_DIR / 'L1/S1A_EW_GRDM_1SDH_20230208T065619_20230208T065723_047141_05A7E5_F291.SAFE'

# build the path to output feature folder
feat_folder = BASE_DIR / 'features/S1A_EW_GRDM_1SDH_20230208T065619_20230208T065723_047141_05A7E5_F291'

# build the path to folder for 8bit rgb images
rgb_folder = BASE_DIR / 'rgb'

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# extract both intensities (linear and dB):

for intensity in ['HH', 'HV']:

    # intensity in linear domain
    S1_feat.get_S1_intensity(
        safe_folder,
        feat_folder,
        intensity,
        loglevel='INFO'
    )

    # intensity in log domain (dB)
    S1_feat.get_S1_intensity(
        safe_folder,
        feat_folder,
        intensity,
        dB=True,
        loglevel='INFO'
    )


# extract S1 meta data (swath mask, IA, lat/lon):

# swath mask
S1_feat.get_S1_swath_mask(
    safe_folder,
    feat_folder,
    loglevel='INFO'
)

# incident angle
S1_feat.get_S1_IA(
    safe_folder,
    feat_folder,
    loglevel='INFO'
)

# lat/lon bands
S1_feat.get_S1_lat_lon(
    safe_folder,
    feat_folder,
    loglevel='INFO'
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# make false-color RGB image
# reads the files 'Sigma0_HH.img' and 'Sigma0_HV.img' from feat_folder
# performs the dB conversions and scaling
# assigns red (HV), green (HH), and blue (HH) channels and stacks 3 bands
# writes to 8bit RGB tif
# parameters for scaling (min/max) and colors (rgb) can be adjusted

S1_feat.make_S1_rgb(
    feat_folder,
    rgb_folder
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <extract_features_from_S1_SAFE.py> ----

