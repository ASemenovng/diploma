import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

file_name = "upt_upt_filtered_bc.xlsx"



with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

top_tickers_by_date = {"2013-01": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-02": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-03": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-04": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-05": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-06": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-07": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-08": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-09": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-10": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-11": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2013-12": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'LKOH', 'NVTK', 'GMKN', 'MTSS', 'TATN', 'FEES'],
                 "2014-01": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-02": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-03": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-04": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-05": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-06": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-07": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-08": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-09": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-10": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-11": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2014-12": ['GAZP', 'GAZP', 'ROSN', 'SBER', 'LKOH', 'VTBR', 'NVTK', 'GMKN', 'MTSS', 'TATN'],
                 "2015-01": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-02": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-03": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-04": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-05": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-06": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-07": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-08": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-09": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-10": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-11": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2015-12": ['GAZP', 'ROSN', 'LKOH', 'VTBR', 'GMKN', 'NVTK', 'SBER', 'TATN', 'ALRS', 'CHMF'],
                 "2016-01": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-02": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-03": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-04": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-05": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-06": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-07": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-08": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-09": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-10": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-11": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2016-12": ['GAZP', 'ROSN', 'SBER', 'VTBR', 'NVTK', 'LKOH', 'GMKN', 'TATN', 'CHMF', 'PLZL'],
                 "2017-01": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-02": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-03": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-04": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-05": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-06": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-07": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-08": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-09": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-10": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-11": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2017-12": ['ROSN', 'SBER', 'GAZP', 'NVTK', 'LKOH', 'VTBR', 'GMKN', 'TATN', 'CHMF', 'ALRS'],
                 "2018-01": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-02": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-03": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-04": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-05": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-06": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-07": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-08": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-09": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-10": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-11": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2018-12": ['SBER', 'GAZP', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'VTBR', 'TATN', 'NLMK', 'CHMF'],
                 "2019-01": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-02": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-03": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-04": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-05": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-06": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-07": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-08": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-09": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-10": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-11": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2019-12": ['ROSN', 'SBER', 'GAZP', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'NLMK', 'CHMF'],
                 "2020-01": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-02": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-03": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-04": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-05": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-06": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-07": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-08": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-09": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-10": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-11": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2020-12": ['GAZP', 'SBER', 'ROSN', 'LKOH', 'NVTK', 'GMKN', 'TATN', 'VTBR', 'PLZL', 'YNDX'],
                 "2021-01": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-02": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-03": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-04": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-05": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-06": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-07": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-08": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-09": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-10": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-11": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2021-12": ['SBER', 'GAZP', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'NLMK', 'TATN'],
                 "2022-01": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-02": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-03": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-04": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-05": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-06": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-07": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-08": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-09": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-10": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-11": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 "2022-12": ['GAZP', 'SBER', 'ROSN', 'NVTK', 'LKOH', 'GMKN', 'PLZL', 'YNDX', 'CHMF', 'NLMK'],
                 }


def create_weighted_returns_dict_portolios(capitalization_dict, sheets_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        returns = 0
        for ticker in tickers:
            df = sheets_dict[ticker]
            specific_row = df[df['year_month'] == date]
            if not specific_row.empty:
                cap = specific_row['capitalization'].iloc[
                    0] if 'capitalization' in specific_row.columns else 0
                returns += cap
        returns_dict[date] = returns
    return returns_dict


def create_weighted_returns_dict(capitalization_dict, sorted_market_capitalization, sheets_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        for ticker in tickers:
            if ticker in sheets_dict:
                df = sheets_dict[ticker]
                specific_row = df[df['year_month'] == date]

                if not specific_row.empty:
                    cur_cup = sorted_market_capitalization[date]
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   

                    cap = specific_row['capitalization'].iloc[0] if 'capitalization' in specific_row.columns else 0
                    exchange_rate_frac = specific_row['exchange_rate_frac'].iloc[
                        0] if 'exchange_rate_frac' in specific_row.columns else 0
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(
                        specific_row['div_rate'].iloc[0]) else 0

                    weight = cap / cur_cup if cur_cup else 0 
                    print("weight: ", weight)
                    if weight <= 0.01:
                        print("alert")
                    weighted_exchange = exchange_rate_frac * weight
                    weighted_div = div_rate * weight
                    returns_dict[date].append((weighted_exchange, weighted_div))

    return dict(returns_dict)


high_market_returns = create_weighted_returns_dict_portolios(top_tickers_by_date, sheets_dict)
print("high_market_returns: ", high_market_returns)

high_returns = create_weighted_returns_dict(top_tickers_by_date, high_market_returns, sheets_dict)

def average_tuples(tuples_list):
    if not tuples_list:
        return 0, 0 

   
    exchange_rates = [tup[0] for tup in tuples_list if tup[0] is not None]
    div_yields = [tup[1] if tup[1] is not None and not pd.isna(tup[1]) else 0 for tup in tuples_list] 

    print("exchange_rates: ", exchange_rates)
   
    avg_exchange_rate = sum(exchange_rates) * 100 if exchange_rates else 0
   
   
   
    avg_div_yield = sum(div_yields) * 100 if div_yields else 0
    avg_div_yield = sum(
        0 if pd.isna(yield_value) else yield_value for yield_value in div_yields) * 100 if div_yields else 0

   

    print("avg_exchange_rate, avg_div_yield: ", avg_exchange_rate, avg_div_yield)

    return avg_exchange_rate, avg_div_yield



high_returns_avg = {date: average_tuples(tuples) for date, tuples in high_returns.items()}

def sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0
    return exchange_rates, div_yields


high_returns_avg = {date: sum_tuple(tuple) for date, tuple in high_returns_avg.items()}

def calculate_cumulative_returns_separatly(monthly_returns):
    cumulative_returns = {}
    cumulative_product = 1
    for date, tuple_return in monthly_returns.items():
        cumulative_product *= (tuple_return[0] / 100 + 1)
        cumulative_product += (tuple_return[1] / 100)
        cumulative_returns[date] = ( cumulative_product - 1) * 100
    return cumulative_returns


def plot_portfolio_returns(with_rolling_average, portfolio_name):
   
    dates = pd.to_datetime(list(with_rolling_average.keys()))
    values = list(with_rolling_average.values())

    df = pd.DataFrame({'Date': dates, 'Value': values})
    df.set_index('Date', inplace=True)

   
    df['MA'] = df['Value'].rolling(window=6, min_periods=1).mean()

   
    plt.figure(figsize=(12, 6))
    plt.bar(df.index, df['Value'], width=25, color='blue', label=f'Доходность {portfolio_name}')
    plt.plot(df.index, df['MA'], color='red', linestyle='-', linewidth=1, label='Скользящее среднее 6 месяцев')

   
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)

    plt.title(f'Накопленная доходность портфеля {portfolio_name}')
    plt.xlabel('Дата')
    plt.ylabel('Накопленная доходность (%)')
    plt.legend()
    plt.grid(True)
    plt.show()







cum_high_returns_avg = calculate_cumulative_returns_separatly(high_returns_avg)

print("cum_high_returns_avg: ", cum_high_returns_avg)


plot_portfolio_returns(cum_high_returns_avg, "акций, капитализация которых выше медианы")