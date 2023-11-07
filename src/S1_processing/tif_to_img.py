#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 12:43:12 2023

@author: cirfa
"""
import os
import argparse
from loguru import logger

def make_parser():
      p = argparse.ArgumentParser(
              formatter_class=argparse.RawDescriptionHelpFormatter,
              description='convert GeoTiff to ENVI (hdr + img) file using gdal_translate',
            )

      p.add_argument(
              'in_file',
              help='path to input tif file'
              )
      p.add_argument(
              'out_file',
              help='path to output img file'
              )
      return p

# parse arguments
p = make_parser()
args = p.parse_args()

in_file = args.in_file
out_file = args.out_file

# check if input file exists
if not os.path.isfile(in_file):
    logger.error(f'Input file does not exist: {in_file}!')
    exit(1)

# gdal command to compress a tiff file
gdal_call = f"gdal_translate -of ENVI {in_file} {out_file}"

# execute call in subshell
os.system(gdal_call)