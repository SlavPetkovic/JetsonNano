import pandas as pd
from datetime import datetime, timedelta
import time
from lib.etl import *

def etl(name):
    data = sensorsreading()
    dataload(data)

    dt = datetime.now() + timedelta(minutes=1)
    dt = dt.replace(second=1)

    while datetime.now() < dt:
        time.sleep(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    etl('PyCharm')
    # Re-run the script at the beginning of every new minute.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
