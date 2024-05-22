import pandas as pd
from collections import OrderedDict
import numpy as np


def process_quantiles_payout_ratio(file_name):
    with pd.ExcelFile(file_name) as xls:
        sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    quantiles_payout_ratio = {0.2: {}, 0.4: {}, 0.6: {}, 0.8: {}}

    all_payout_ratio = {}

    for sheet_name, data in sheets_dict.items():
        december_data = data[data['year_month'].str.endswith('-12')]

        for index, row in december_data.iterrows():
            year_month = row['year_month']
            payout_ratio = row.get('payout_ratio')

            if year_month not in all_payout_ratio:
                all_payout_ratio[year_month] = []

            if pd.isna(payout_ratio):
                continue
            all_payout_ratio[year_month].append(payout_ratio)


    
    for date, payout_ratios in all_payout_ratio.items():
        if payout_ratios:
            sorted_bms = sorted(payout_ratios)
            for quantile in quantiles_payout_ratio.keys():
                quantile_value = np.percentile(sorted_bms, int(quantile * 100))
                quantiles_payout_ratio[quantile][date] = quantile_value

    sorted_quantiles_payout_ratio = {q: OrderedDict(sorted(data.items())) for q, data in quantiles_payout_ratio.items()}

    return sorted_quantiles_payout_ratio


file_name = '../data/filtered_blue_chips (2).xlsx'
quantiles_bm = process_quantiles_payout_ratio(file_name)




print("\nQuantiles for payout_ratio:")
for quantile, data in quantiles_bm.items():
    print(f"{int(quantile * 100)}%:", data)