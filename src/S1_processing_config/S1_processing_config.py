#---- This is <S1_processing_config.py> ----

"""
Configuration for settings for S1_processing library
""" 

from dotenv import load_dotenv
from os.path import join, dirname
from os import environ

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# load local .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# get snap gpt executable
GPT = environ.get('GPT', '/home/jo/esa_snap/snap/bin/gpt')

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# SNAP GRAPH FILES FOR SENTINEL-1

# --------- #

# EW GRDM graphs
# with and without speckle filter (ML)
# with and without dB

snap_S1_EW_GRDM_NR_Cal_Spk_XX    = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_XX.xml'
snap_S1_EW_GRDM_NR_Cal_Spk_db_XX = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_dB_XX.xml'
snap_S1_EW_GRDM_NR_Cal_XX        = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_XX.xml'
snap_S1_EW_GRDM_NR_Cal_db_XX     = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_dB_XX.xml'

# --------- #

# EW GRDH graphs
# with and without speckle filter (ML)
# with and without dB

snap_S1_EW_GRDH_NR_Cal_Spk_XX    = 'S1_EW_GRDM/S1_EW_GRDH_NR_Cal_Spk_XX.xml'
snap_S1_EW_GRDH_NR_Cal_Spk_db_XX = 'S1_EW_GRDM/S1_EW_GRDH_NR_Cal_Spk_dB_XX.xml'
snap_S1_EW_GRDH_NR_Cal_XX        = 'S1_EW_GRDM/S1_EW_GRDH_NR_Cal_XX.xml'
snap_S1_EW_GRDH_NR_Cal_db_XX     = 'S1_EW_GRDM/S1_EW_GRDH_NR_Cal_dB_XX.xml'

# --------- #

# IW GRDH graphs
# with and without speckle filter (ML)
# with and without dB

snap_S1_IW_GRDH_NR_Cal_Spk_XX    = 'S1_IW_GRDM/S1_IW_GRDH_NR_Cal_Spk_XX.xml'
snap_S1_IW_GRDH_NR_Cal_Spk_db_XX = 'S1_IW_GRDM/S1_IW_GRDH_NR_Cal_Spk_dB_XX.xml'
snap_S1_IW_GRDH_NR_Cal_XX        = 'S1_IW_GRDM/S1_IW_GRDH_NR_Cal_XX.xml'
snap_S1_IW_GRDH_NR_Cal_db_XX     = 'S1_IW_GRDM/S1_IW_GRDH_NR_Cal_dB_XX.xml'

# --------- #

# lat, lon, IA
snap_S1_lat = 'S1_meta/S1_lat.xml'
snap_S1_lon = 'S1_meta/S1_lon.xml'
snap_S1_IA  = 'S1_meta/S1_IA.xml'







"""
# graphs with ML (Spk)

# EW_GRDM
snap_S1_EW_GRDM_NR_Cal_Spk_HH    = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_HH.xml'
snap_S1_EW_GRDM_NR_Cal_Spk_VV    = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_VV.xml'
snap_S1_EW_GRDM_NR_Cal_Spk_HV    = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_HV.xml'
snap_S1_EW_GRDM_NR_Cal_Spk_VH    = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_VH.xml'

# EW_GRDM in dB
snap_S1_EW_GRDM_NR_Cal_Spk_db_HH = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_dB_HH.xml'
snap_S1_EW_GRDM_NR_Cal_Spk_db_VV = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_dB_VV.xml'
snap_S1_EW_GRDM_NR_Cal_Spk_db_HV = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_dB_HV.xml'
snap_S1_EW_GRDM_NR_Cal_Spk_db_VH = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_Spk_dB_VH.xml'

# EW_GRDH
snap_S1_EW_GRDH_NR_Cal_Spk_HH    = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_HH.xml'
snap_S1_EW_GRDH_NR_Cal_Spk_VV    = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_VV.xml'
snap_S1_EW_GRDH_NR_Cal_Spk_HV    = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_HV.xml'
snap_S1_EW_GRDH_NR_Cal_Spk_VH    = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_VH.xml'

# EW_GRDH in db
snap_S1_EW_GRDH_NR_Cal_Spk_db_HH = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_dB_HH.xml'
snap_S1_EW_GRDH_NR_Cal_Spk_db_VV = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_dB_VV.xml'
snap_S1_EW_GRDH_NR_Cal_Spk_db_HV = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_dB_HV.xml'
snap_S1_EW_GRDH_NR_Cal_Spk_db_VH = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_Spk_dB_VH.xml'

# IW_GRDH
snap_S1_IW_GRDH_NR_Cal_Spk_HH    = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_HH.xml'
snap_S1_IW_GRDH_NR_Cal_Spk_VV    = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_VV.xml'
snap_S1_IW_GRDH_NR_Cal_Spk_HV    = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_HV.xml'
snap_S1_IW_GRDH_NR_Cal_Spk_VH    = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_VH.xml'

# IW_GRDH in dB
snap_S1_IW_GRDH_NR_Cal_Spk_db_HH = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_dB_HH.xml'
snap_S1_IW_GRDH_NR_Cal_Spk_db_VV = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_dB_VV.xml'
snap_S1_IW_GRDH_NR_Cal_Spk_db_HV = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_dB_HV.xml'
snap_S1_IW_GRDH_NR_Cal_Spk_db_VH = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_Spk_dB_VH.xml'


# graphs with no ML (Spk)

# EW_GRDM
snap_S1_EW_GRDM_NR_Cal_HH      = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_HH.xml'
snap_S1_EW_GRDM_NR_Cal_VV      = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_VV.xml'
snap_S1_EW_GRDM_NR_Cal_HV      = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_HV.xml'
snap_S1_EW_GRDM_NR_Cal_VH      = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_VH.xml'

# EW_GRDM in dB
snap_S1_EW_GRDM_NR_Cal_db_HH   = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_dB_HH.xml'
snap_S1_EW_GRDM_NR_Cal_db_VV   = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_dB_VV.xml'
snap_S1_EW_GRDM_NR_Cal_db_HV   = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_dB_HV.xml'
snap_S1_EW_GRDM_NR_Cal_db_VH   = 'S1_EW_GRDM/S1_EW_GRDM_NR_Cal_dB_VH.xml'

# EW_GRDH
snap_S1_EW_GRDH_NR_Cal_HH      = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_HH.xml'
snap_S1_EW_GRDH_NR_Cal_VV      = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_VV.xml'
snap_S1_EW_GRDH_NR_Cal_HV      = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_HV.xml'
snap_S1_EW_GRDH_NR_Cal_VH      = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_VH.xml'

# EW_GRDH in dB
snap_S1_EW_GRDH_NR_Cal_db_HH   = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_dB_HH.xml'
snap_S1_EW_GRDH_NR_Cal_db_VV   = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_dB_VV.xml'
snap_S1_EW_GRDH_NR_Cal_db_HV   = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_dB_HV.xml'
snap_S1_EW_GRDH_NR_Cal_db_VH   = 'S1_EW_GRDH/S1_EW_GRDH_NR_Cal_dB_VH.xml'

# IW_GRDH
snap_S1_IW_GRDH_NR_Cal_HH      = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_HH.xml'
snap_S1_IW_GRDH_NR_Cal_VV      = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_VV.xml'
snap_S1_IW_GRDH_NR_Cal_HV      = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_HV.xml'
snap_S1_IW_GRDH_NR_Cal_VH      = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_VH.xml'

# EW_GRDH in dB
snap_S1_IW_GRDH_NR_Cal_db_HH   = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_dB_HH.xml'
snap_S1_IW_GRDH_NR_Cal_db_VV   = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_dB_VV.xml'
snap_S1_IW_GRDH_NR_Cal_db_HV   = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_dB_HV.xml'
snap_S1_IW_GRDH_NR_Cal_db_VH   = 'S1_IW_GRDH/S1_IW_GRDH_NR_Cal_dB_VH.xml'
"""

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <S1_processing_config.py> ----
