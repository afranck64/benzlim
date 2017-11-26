# Benzlim

## Installation

- create a directory: `InformatiCup`
- clone the official InformatiCup project from the link: https://github.com/InformatiCup/InformatiCup2018 inside the `InformtatiCup` directory
- clone/move the `benzlim` project inside the `InformatiCup` directory

## Configuration

- requirements:
  - Python >= 2.6
  - pip

- installation of required python packages:
    `pip install --user -r requirements.txt`   #May need root access

## Run
   From the `InformatiCup` directory, run the command: `python benzlim -h` to get detailled

   ### Predict: `python benzlim -p $prediction_file $DIR_InformatiCup2018`

   ### Routing with price prediction: `python benzlim -r $route_file $dir_informaticup2018`

   ### Routing with predicted prices: `python benzlim -r -g $predicted_prices $route_file $dir_informaticup2018`