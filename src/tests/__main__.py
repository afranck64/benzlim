import sys
import os


APP_DIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..'))

INPUT_TEST_FILE = os.path.abspath("../InformatiCup2018/Eingabedaten/Fahrzeugrouten/Bertha Benz Memorial Route.csv")
INPUT_TEST_FILE = os.path.abspath("../InformatiCup2018/Eingabedaten/Fahrzeugrouten/test_route.csv")

if __name__ == "__main__":
    os.system("python '%s' '%s'" % (APP_DIR, INPUT_TEST_FILE))