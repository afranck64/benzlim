##Quick Start

This quick start guide is aimed at users with some basic knowledge of running and compiling python code who already have a development environment set up. Head over to the [Installation Chapter](/installation) for the complete guide.

### Requirements

  - Python 2.7.z (z >= 9) (https://www.python.org/downloads/)
  - Git (https://git-scm.com/downloads)
  - Python packages  
      - coverage
      - numpy >= 1.13.3
      - pandas >= 0.18
      - python-dateutil

### Installing Benzlim

- Create a folder named `InformatiCup`
- Inside the `InformatiCup` folder, clone the official InformatiCup2018 project from the link [InformatiCup2018](https://github.com/InformatiCup/InformatiCup2018 ) inside a new folder named `InformtatiCup2018`
- Extract `benzlim's` zip file into a new folder named `benzlim`

### Run

   From the `InformatiCup` directory, run the command: `python benzlim -h` to get a more detailled help.  
   if your `InformatiCup2018` is not located in the same directory as `benzlim`, you need to provide the optional argument `--informaticup2018-dir` when refering to it.  
   Running `benzlim` for the first time may take some time because the fuel prices need to be trained first.

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
Example prediction file:
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

#### Predict

- `python benzlim predict $prediction_file`

#### Routing with price prediction

- `python benzlim route $route_file`

#### Routing with predicted prices

- `python benzlim route -g $predicted_prices $route_file`

#### Train model

- `python benzlim train --force`

#### Run the tests

- `python benzlim test`

#### Run the benchmark

- `python benzlim benchmark`

#### Run the coverage benchmark

- `python benzlim coverage`

