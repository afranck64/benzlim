# Benzlim

## Installation

- create a directory: `InformatiCup`
- create a `InformatiCup2018` directory inside the previous one
- clone the official InformatiCup project from the link [InformatiCup2018](https://github.com/InformatiCup/InformatiCup2018 ) inside the `InformtatiCup2018` directory
- copy the `benzlim` project inside the `InformatiCup` directory

## Configuration

- requirements:
  - Python 2.7.x (x >= 9) (https://www.python.org/downloads/)

- installation of required python packages:
    `pip install --user -r requirements.txt`

- train the model:
  see [Model training](#train-model)

## Run

   From the `InformatiCup` directory, run the command: `python benzlim -h` to get detailled help

### Predict

- `python benzlim predict $prediction_file $informaticup2018_dir`

### Routing with price prediction

- `python benzlim route $route_file $informaticup2018_dir`

### Routing with predicted prices

- `python benzlim route -g $predicted_prices $route_file $informaticup2018_dir`

### Train model

- `python benzlim train $informaticup2018_dir`

### Run the tests

- `python benzlim test $informaticup2018_dir`

### Run the benchmark

- `python benzlim benchmark $informaticup2018_dir`

### Run the coverage benchmark

- `python benzlim coverage $informaticup2018_dir`
