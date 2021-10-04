import pandas as pd
from datetime import datetime, timedelta
import time
from lib.etl import *

def etl(name):
    data = sensorsreading()
    dataload(data)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    starttime = time.time()
    while True:
        etl('PyCharm')
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    # Re-run the script at the beginning of every new minute.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
