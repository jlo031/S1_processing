#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
write numpy array to tiff using gdal library

NOTE: to get GDAL dtype of numpy array, run the following:
            data_type = gdal_array.NumericTypeCodeToGDALTypeCode(array.dtype)
            
            Needs this import: from osgeo import gdal_array
"""

from osgeo import gdal, gdalconst
from loguru import logger


def write_to_tif(input_array, output_tif_path, data_type_out = gdalconst.GDT_Float32):
    # get dims and data type of input_array
    if len(input_array.shape) == 2:
        lines, samples = input_array.shape
        bands = 1
    elif len(input_array.shape) == 3:
        bands, lines, samples = input_array.shape
    else:
        logger.error('input_array.shape must be (lines,samples) or (bands,lines,samples)')
    
    # initialize new GTiff file for output
    GTdriver = gdal.GetDriverByName('GTiff')
    out = GTdriver.Create(
      output_tif_path,
      samples,
      lines,
      bands,
      data_type_out
    )
    
    # write input_array to tiff file
    if bands == 1:
        band_out = out.GetRasterBand(1)
        band_out.WriteArray(input_array)
        band_out.FlushCache()
    elif bands > 1:
        for b in range(1,bands+1):
            band_out = out.GetRasterBand(b)
            band_out.WriteArray(input_array[b-1,:,:])
            band_out.FlushCache()
    out.FlushCache()
    del out