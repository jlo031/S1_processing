# ---- This is <make_S1_rgb.py> ----

import S1_feature_extraction as S1_features
import argparse
from loguru import logger

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def make_parser():

    p = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = S1_features.make_S1_rgb.__doc__.split("\n")[0],
    )

    p.add_argument(
        'feat_folder',
        help = 'path to folder with input image features (HH, HV)'
    )
    p.add_argument(
        'result_folder',
        help = 'path to result folder where scaled RGB file is placed'
    )
    p.add_argument(
        '-hhMin',
        default = -30,
        help='minimum value for scaling HH channel (default=-30)'
    )
    p.add_argument(
        '-hhMax',
        default = 0,
        help = 'maximum value for scaling HH channel (default=0)'
    )
    p.add_argument(
        '-hvMin',
        default = -35,
        help = 'minimum value for scaling HV channel (default=-35)'
    )
    p.add_argument(
        '-hvMax',
        default=-5,
        help = 'maximum value for scaling HV channel (default=-5)'
    )
    p.add_argument(
        '-newMin',
        default = 0,
        help = 'new minimum for scaled image (default=0)'
    )
    p.add_argument(
        '-newMax',
        default = 255,
        help = 'new maximum for scaled image (default=255)'
    )
    p.add_argument(
        '-red',
        choices = ['HH','HV','zero'],
        default = 'HV',
        help = 'channel for red band (default=HV)'
    )
    p.add_argument(
        '-green',
        choices = ['HH','HV','zero'],
        default = 'HH',
        help = 'channel for green band (default=HH)'
    )
    p.add_argument(
        '-blue',
        choices = ['HH','HV','zero'],
        default = 'HH',
        help = 'channel for blue band (default=HH)'
    )
    p.add_argument(
        '-overwrite',
        action = 'store_true',
        help = 'overwrite existing files'
    )
    p.add_argument(
        '-loglevel',
        choices = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        default = 'INFO',
        help = 'set logger level (default=INFO)',
    )

    return p

# -------------------------------------------------------------------------- #

if __name__ == '__main__':

  p = make_parser()
  args = p.parse_args()

  try:
    S1_features.make_S1_rgb(**vars(args))
  except Exception as E:
    logger.critical(E)

# -------------------------------------------------------------------------- #

# ---- End of <make_S1_rgb.py> ----
