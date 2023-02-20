# S1_processing
This library provides python code for standard feature extraction and processing of Copernicus Sentinel-1 data.


### Conda environment
The Geospatial Data Abstraction Layer ([GDAL]) library is required to run the code.
The simplest way to use GDAL with Python is to get the Anaconda Python distribution.
It is recommended to run the code in a virtual environment.

Creating python environments with a working __gdal__ distribution can be tricky and depends on anaconda, python, and gdal versions as well as your operating system. On February 15th 2023, the following steps worked to succesfully build the required environment on Ubuntu22.04:

    # create new environment
    conda create -y -n S1_processing gdal
    
    # activate environment
    conda activate S1_processing
    
    # install required packages
    conda install ipython scipy loguru lxml python-dotenv


### Installation

Start by cloning the repository:

    # clone the repository
    git clone https://github.com/jlo031/S1_processing.git

Part of the code in this library uses the graph processing tool (__gpt__) from ESA's [SNAP] application. Before installation, you have to create a local _".env"_ file with a variable called GPT that points to the __gpt__ executable of your local SNAP installation. The _".env"_ file must be located at _"S1_processing/src/S1_processing/.env"_ of the cloned repository and must contain the following line:

>GPT="/path/to/your/esa_snap/gpt"

Now, change into the main directory of the cloned repository (it should contain the '_setup.py_' file) and install the library:

    # installation
    pip install .


### Usage

Easy usage examples are provided in the "examples" folder.


[GDAL]: https://gdal.org/
[SNAP]: https://step.esa.int
