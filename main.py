import pandas as pd
from datetime import datetime, timedelta
import time
from lib.etl import *

def print_hi(name):
    data = pd.DataFrame()

    # Re-run the script at the beginning of every new minute.
    dt = datetime.now() + timedelta(minutes=1)
    dt = dt.replace(second=1)
    sensorsreading()
    print(data)
    while datetime.now() < dt:
        time.sleep(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
