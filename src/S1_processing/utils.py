# ---- This is <utils.py> ----

"""
Utils for S1 processing library
"""

import sys
import pathlib
import os

from dotenv import load_dotenv

from loguru import logger

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_GPT_path(dotenv_location='installation'):
    """
    Get path to SNAP 'GPT' executable.
    On default, this searches in installation directory of the 'S1_processing' library.
    Can be forced to use local '.env' file by setting 'dotenv_location' to 'local'.

    Parameters
    ----------
    dotenv_location : location of .env file with GPT path (default: 'installation')

    Returns
    -------
    GPT : path to local GPT executable
    """    

    # set default path for GPT
    GPT_default = '/home/jo/esa_snap/snap/bin/gpt_test'
    ##  GPT_default = "C:\Users\jplohse\AppData\Local\Programs\esa-snap\bin\gpt.exe" # on UTAS windows

    # check that doten_location is valid, if not return default GPT with warning
    if dotenv_location not in ['installation', 'local']:
        logger.warning(f"Invalid input. 'dotenv_location' must be 'installation' or 'local'")
        logger.warning("Using default path for GPT which may not be correct for your system")
        return GPT_default

    # look for installed .env
    if dotenv_location == 'installation':
        logger.debug("Trying to read GPT path from installation directory '.env'")
        
        # get path to installation directory
        ##install_dir = pathlib.Path('path_to_install_dir')
        install_dir = pathlib.Path(__file__).parent
        logger.debug(f"install_dir: {install_dir}")

        dotenv_path = install_dir / 'gpt_config' / '.env'
        logger.debug(f"dotenv_path: {dotenv_path}")
        
        # if not found, try local .env
        if not dotenv_path.is_file():
            logger.warning("Could not find '.env' in installation directory")
            logger.warning("Checking for local '.env' in your current directory")

            dotenv_path = pathlib.Path('.env')
            logger.debug(f"dotenv_path: {dotenv_path}")

            if not dotenv_path.is_file():
                logger.warning("Could not find local '.env' either")
                logger.warning("Using default path for GPT which may not be correct for your system")
                return GPT_default

    # look for local .env immediately and ignore possibly installed .env
    elif dotenv_location == 'local':
        logger.debug("Trying to read GPT path from local directory '.env'")    

        dotenv_path = pathlib.Path('.env')
        logger.debug(f"dotenv_path: {dotenv_path}")

        if not dotenv_path.is_file():
            logger.warning("Could not find local 'env' file")
            logger.warning("Using default path for GPT which may not be correct for your system")
            return GPT_default

    if not dotenv_path.is_file():
        logger.warning("THIS SHOULD NOT HAPPEN, SHOULD HAVE BEEN CAUGHT BEFORE")
        logger.warning("Using default path for GPT which may not be correct for your system")
        return GPT_default

    elif dotenv_path.is_file():
        load_dotenv(dotenv_path , override=True)

        try:
            GPT = os.environ["GPT"]
        except:
            logger.warning("The environment variable 'GPT' is not set from your '.env' file")
            logger.warning("Using default path for GPT which may not be correct for your system")
            return GPT_default

        logger.debug(f"GPT set to: {GPT}")

    return GPT

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <utils.py> ----