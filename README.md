# Timeseries Analysis Tool

A config-based timeseries analysis tool

### Description ###

A python script that runs a number of tests and calculations on a timeseries stored in a database. The script requires a config (json and yaml supported so far). Check ``` /examples/ ``` for config examples.

### Installation ###

This script requires python3.X

1. (Optional) **Create a python virutal environment**:

``` 
$ python3 -m venv . 
```
Activate the virtual environment:

```
$ source ./bin/activate
```


2. **Clone this repo**:

``` 
$ git clone git@github.com:VascoRegal/timeseries-analysis-tool.git 
```

3. **```cd``` into the repo**.

4. **Install the requirments**:
```
$ pip install -r requirments.txt
```

5. **Create a folder to store the plots**:
```
$ mkdir plots
```

### Usage ###
```
$ python3 main.py <path-to-config-file>
```

If you are running the script on a remote machine through ssh, you might want to copy the saved plots. On your local machine:
```
$ scp user@remomte_machine:path/to/installation/plots/*.png path/to/local_machine
```

### TODO ###
* Test the script for multiple contexts.
* Do a proper interpretation of the autocorrelation method to find the series' possible period. (see Note on the fucntion ```autocorrelate```)
* Implement XML parsing.
* Save plots with better names, not just number.png
* Exception handling.


