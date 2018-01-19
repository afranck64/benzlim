# Benzlim

## Installation

### Requirements
  - Python 2.7.z (z >= 9) (https://www.python.org/downloads/)
  - Git (https://git-scm.com/downloads)
  - Python packages  
    The required python packages can be installed using `pipX.Y` where X and Y are you majors python versions (`pip2.7` for `python2.7.*`):
    - `pipX.Y install -r requirements.txt` (with admin rights, for a system wide installation) or  
    - `pipX.Y install --user -r requirements.txt` (for a user only installation)
    This will install the following packages (and their dependancies) on your system:
      - coverage
      - numpy >= 1.13.3
      - pandas >= 0.18
      - python-dateutil

### Configuration
- create a directory `InformatiCup` with `mkdir InformatiCup`
- change to the `InformatiCup` directory with `cd InformatiCup`
- create a `InformatiCup2018` directory inside `InformatiCup` with `mkdir InformatiCup2018`
- change to the `InformatiCup2018` directory with `cd InformatiCup2018`
- clone the official InformatiCup2018 project from the link [InformatiCup2018](https://github.com/InformatiCup/InformatiCup2018 ) inside the `InformtatiCup2018` directory with `git clone https://github.com/InformatiCup/InformatiCup2018`
- get back to the `InformatiCup` directory with `cd ..`
- copy the `benzlim` project inside the `InformatiCup` directory


## Run

   From the `InformatiCup` directory, run the command: `python benzlim -h` to get detailled help.  
   if your `InformatiCup2018` is not located in the same directory as `benzlim`, you need to provide the optional argument `--informaticup2018-dir` refering to it.  
   On the first run, the data will be trained, which can take some time.

### Predict

- `python benzlim predict $prediction_file`

### Routing with price prediction

- `python benzlim route $route_file`

### Routing with predicted prices

- `python benzlim route -g $predicted_prices $route_file`

### Train model

- `python benzlim train --force`

### Run the tests

- `python benzlim test`

### Run the benchmark

- `python benzlim benchmark`

### Run the coverage benchmark

- `python benzlim coverage`
