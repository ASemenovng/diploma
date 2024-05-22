import pandas as pd
from collections import OrderedDict
import numpy as np


def process_quantiles_div_rate(file_name):
    with pd.ExcelFile(file_name) as xls:
        sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    quantiles_div_rate = {0.2: {}, 0.4: {}, 0.6: {}, 0.8: {}}

    all_div_rate = {}

    for sheet_name, data in sheets_dict.items():
        december_data = data[data['year_month'].str.endswith('-12')]

        for index, row in december_data.iterrows():
            year_month = row['year_month']
            div_rate = row.get('div_rate')

            if year_month not in all_div_rate:
                all_div_rate[year_month] = []

            if pd.isna(div_rate):
                continue
            all_div_rate[year_month].append(div_rate)


    
    for date, div_rates in all_div_rate.items():
        if div_rates:
            sorted_bms = sorted(div_rates)
            for quantile in quantiles_div_rate.keys():
                quantile_value = np.percentile(sorted_bms, int(quantile * 100))
                quantiles_div_rate[quantile][date] = quantile_value

    sorted_quantiles_div_rate = {q: OrderedDict(sorted(data.items())) for q, data in quantiles_div_rate.items()}

    return sorted_quantiles_div_rate


file_name = '../data/filtered_blue_chips (2).xlsx'
quantiles_bm = process_quantiles_div_rate(file_name)




print("\nQuantiles for div_rate:")
for quantile, data in quantiles_bm.items():
    print(f"{int(quantile * 100)}%:", data)