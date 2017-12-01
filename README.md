# Benzlim

## Installation

- create a directory: `InformatiCup`
- clone the official InformatiCup project from the link: https://github.com/InformatiCup/InformatiCup2018 inside the `InformtatiCup` directory
- clone/move the `benzlim` project inside the `InformatiCup` directory

## Configuration

- requirements:
  - Python 2.7.x
  - pip

- installation of required python packages:
    `pip install --user -r requirements.txt`   #May need root access

## Run

   From the `InformatiCup` directory, run the command: `python benzlim -h` to get detailled help

### Predict

- `python benzlim predict $prediction_file $informaticup2018_dir`

### Routing with price prediction

- `python benzlim route $route_file $informaticup2018_dir`

### Routing with predicted prices

- `python benzlim route -g $predicted_prices $route_file $informaticup2018_dir`

### Training using available data

- `python benzlim train $informaticup2018_dir`