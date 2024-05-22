import pandas as pd
import numpy as np
from collections import OrderedDict



def process_quantiles(file_name):
    
    with pd.ExcelFile(file_name) as xls:
        sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    
    quantiles = {0.2: {}, 0.4: {}, 0.6: {}, 0.8: {}}

    
    all_capitalizations = {}

    for sheet_name, data in sheets_dict.items():
        
        december_data = data[data['year_month'].str.endswith('-12')]

        for index, row in december_data.iterrows():
            year_month = row['year_month']
            capitalization = row['capitalization']

            if year_month not in all_capitalizations:
                all_capitalizations[year_month] = []
            all_capitalizations[year_month].append(capitalization)

    
    for date, caps in all_capitalizations.items():
        if caps:
            sorted_caps = sorted(caps)
            for quantile in quantiles.keys():
                
                quantile_value = np.percentile(sorted_caps, int(quantile * 100))
                quantiles[quantile][date] = quantile_value

    return quantiles



file_name = '../data/filtered_blue_chips (2).xlsx'
quantiles = process_quantiles(file_name)


quantiles = {q: OrderedDict(sorted(data.items())) for q, data in quantiles.items()}



print("Quantiles for 20%:", quantiles[0.2])
print("Quantiles for 40%:", quantiles[0.4])
print("Quantiles for 60%:", quantiles[0.6])
print("Quantiles for 80%:", quantiles[0.8])

