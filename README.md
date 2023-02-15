# S1_processing
Feature extraction and processing of Sentinel-1 data.


## Conda environment
The Geospatial Data Abstraction Layer (GDAL) library is required to run the code.
The simplest way to use GDAL with Python is to get the Anaconda Python distribution.
It is recommended to run the code in a virtual environment.

On February15th 2023, the following steps worked to succesfully build the required environment on Ubuntu22.04:

    # create new environment
    conda create -y -n S1_processing gdal
    
    # activate environment
    conda activate S1_processing
    
    # install required packages
    conda install ipython scipy loguru lxml python-dotenv


## Installation

Part of the code in this library uses the graph processing tool (gpt) from ESA's [SNAP] application. Before installation, you have to create a local ".env" file with a variable called GPT that points to the gpt executable of your local SNAP installation. 

    # Clone the repository
    git clone git clone https://github.com/jlo031/S1_processing

Create a file called ".env" with the following line in the folder "S1_processing/src/S1_processing_config/" of the cloned repository: 
>GPT="path/to/your/esa_snap/gpt"

Install the library:

    # installation
    pip install .










[SNAP]: https://step.esa.int
