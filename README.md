# Benzlim

>Head over to the [QUICK START](/QUICK_START.md) page if you are familiar with python configuration and the command line. If not, just read the following instructions. Do not forget to take a look at the [FAQ](/FAQ.md) page. Your questions could have been answered before.

## Installation

### Requirements
  - Python 2.7.z (z >= 9) (https://www.python.org/downloads/)
  - Git (https://git-scm.com/downloads)
  - Python packages  
    The required python packages can be installed using `pipX.Y` where X and Y are you majors python versions (`pip2.7` for `python2.7.*`):
    - `pipX.Y install -r requirements.txt` (with admin rights, for a system wide installation) or  
    - `pipX.Y install --user -r requirements.txt` (for a user only installation)
    This will install the following packages (and their dependencies) on your system:
      - coverage
      - numpy >= 1.13.3
      - pandas >= 0.18
      - python-dateutil

### Configuration
- open a console/terminal
- create a directory `InformatiCup` with `mkdir InformatiCup`
- change to the `InformatiCup` directory with `cd InformatiCup`
- change to the `InformatiCup2018` directory with `cd InformatiCup2018`
- clone the official InformatiCup2018 project from the link [InformatiCup2018](https://github.com/InformatiCup/InformatiCup2018 ) inside the `InformtatiCup` directory with `git clone https://github.com/InformatiCup/InformatiCup2018`
- copy the `benzlim` inside the `InformatiCup` directory
- Both `benzlim` and `InformatiCup2018` folders shoud be in the same directory


## Run

   From the `InformatiCup` directory, run the command: `python benzlim -h` to get detailed help.  
   If your `InformatiCup2018` folder is not located in the same directory as `benzlim`, you need to provide the optional argument `--informaticup2018-dir` which refers to it.  
   On the first run, the data will be trained, which can take some time.
   
   Please note that the prediction_file needs to have the following format with the three parts between `;` being "Use Gasoline prices until this date", "The time for the prediction" and "Gas station ID" respectively:
   ```
   YYYY-MM-DD HH:MM:SS+HH;YYYY-MM-DD HH:MM:SS+HH;GAS_STATION_ID
   ```
   Example prediction file:
   ```
   2015-02-10 12:18:01+01;2015-02-15 21:18:01+01;24
   2016-03-22 10:42:01+01;2016-03-22 10:43:01+01;46
   2016-01-27 03:06:01+01;2016-02-26 18:06:01+01;14038
   2015-06-11 14:30:02+02;2015-06-12 07:50:02+02;4160
   ```

   Please note that the route_file needs to have the following format:
   ```
   TANK_CAPACITY
   YYYY-MM-DD HH:MM:SS+HH;GAS_STATION_I
   ```
   Example route file:
   ```
   3
   2015-08-01 08:00:00+02;10957
   2015-08-01 09:55:31+02;11108
   2015-08-01 10:27:25+02;11172
   2015-08-01 11:02:43+02;11150
   2015-08-01 11:48:16+02;11152
   2015-08-01 12:20:23+02;11238
   2015-08-01 12:52:37+02;11320
   ```

### Predict

- `python benzlim predict $prediction_file`

### Routing with price prediction

- `python benzlim route $route_file`

### Routing with predicted prices

- `python benzlim route -g $predicted_prices $route_file`

### Train the model

- `python benzlim train --force`

### Run the tests

- `python benzlim test`

### Run the benchmark

- `python benzlim benchmark`

### Run the coverage benchmark

- `python benzlim coverage`

## Technical Documentation (German)

If you are interested in the technical aspects of `benzlim` and want to know more about how the fuel price predictions are done, the [technical documentation](/docs/DOCS.md) would be what you are looking for. The text is in German.
