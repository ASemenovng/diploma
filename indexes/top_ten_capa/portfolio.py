import pandas as pd
import numpy as np
from datetime import datetime


file_name = "filtered_blue_chips-4.xlsx"



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


top_tickers_returns = {date: [] for date in top_tickers_by_date.keys()}

def calculate_total_returnf(df, year_month):
   
    row = df[df['year_month'] == year_month]

   
   
    if row.empty:
        return 0 

    cur_cup = 0
    for t in tickers:
        cap = row['capitalization'].iloc[0] if 'capitalization' in row.columns else 0
        cur_cup += cap

    cap = row['capitalization'].iloc[0] if 'capitalization' in row.columns else 0

    weight = cap / cur_cup if cur_cup else 0 
   

   
    exchange_rate_frac = row['exchange_rate_frac'].iloc[0] if not row.empty and not pd.isna(
        row['exchange_rate_frac'].iloc[0]) else 0
    div_rate = row['div_rate'].iloc[0] if not row.empty and not pd.isna(row['div_rate'].iloc[0]) else 0

   
    return (exchange_rate_frac + div_rate) * weight



for date, tickers in top_tickers_by_date.items():
   
    year_month = date
    for ticker in tickers:
        df = sheets_dict[ticker]
        total_return = calculate_total_returnf(df, year_month)
        top_tickers_returns[date].append(total_return)

print("top_tickers_returns: ", top_tickers_returns)

average_returns = {}


for date, returns in top_tickers_returns.items():
    if returns: 
        average_return = sum(returns)
    else:
        average_return = 0 
    average_returns[date] = average_return

print("average_returns: ", average_returns)


data = {
    'Date': list(average_returns.keys()),
    'Returns': list(average_returns.values()),
}

df = pd.DataFrame(data)


output_file = 'weight_top_ten_capa.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Returns Summary')