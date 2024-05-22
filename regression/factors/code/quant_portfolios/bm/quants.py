import pandas as pd
from collections import OrderedDict
import numpy as np


def process_quantiles_bm(file_name):
    with pd.ExcelFile(file_name) as xls:
        sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    quantiles_bm = {0.2: {}, 0.4: {}, 0.6: {}, 0.8: {}}

    all_bm = {}

    for sheet_name, data in sheets_dict.items():
        december_data = data[data['year_month'].str.endswith('-12')]

        for index, row in december_data.iterrows():
            year_month = row['year_month']
            bm = row.get('B/M')

            if year_month not in all_bm:
                all_bm[year_month] = []

            if pd.isna(bm):
                continue
            all_bm[year_month].append(bm)


    
    for date, bms in all_bm.items():
        if bms:
            sorted_bms = sorted(bms)
            for quantile in quantiles_bm.keys():
                quantile_value = np.percentile(sorted_bms, int(quantile * 100))
                quantiles_bm[quantile][date] = quantile_value

    sorted_quantiles_bm = {q: OrderedDict(sorted(data.items())) for q, data in quantiles_bm.items()}

    return sorted_quantiles_bm


file_name = '../data/filtered_blue_chips (2).xlsx'
quantiles_bm = process_quantiles_bm(file_name)




print("\nQuantiles for B/M:")
for quantile, data in quantiles_bm.items():
    print(f"{int(quantile * 100)}%:", data)