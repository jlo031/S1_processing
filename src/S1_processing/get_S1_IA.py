# ---- This is <get_S1_IA.py> ----

import S1_processing.S1_feature_extraction as S1_features
import argparse
from loguru import logger

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def make_parser():

    p = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = S1_features.get_S1_IA.__doc__.split("\n")[0],
    )

    p.add_argument(
        'safe_folder',
        help = 'path to S1 input image SAFE folder'
    )
    p.add_argument(
        'feat_folder',
        help = 'path to feature folder where output files are placed'
    )
    p.add_argument(
        '-overwrite',
        action = 'store_true',
        help = 'overwrite existing files'
    )
    p.add_argument(
        '-dry_run',
        action = 'store_true',
        help = 'do not execute actual processing'
    )
    p.add_argument(
        '-loglevel',
        choices = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        default = 'INFO',
        help = 'loglevel setting (default=INFO)',
    )

    return p

# -------------------------------------------------------------------------- #

if __name__ == '__main__':

    p = make_parser()
    args = p.parse_args()

    try:
        S1_features.get_S1_IA(**vars(args))
    except Exception as E:
        logger.critical(E)

# -------------------------------------------------------------------------- #

# ---- End of <get_S1_IA.py> ----
