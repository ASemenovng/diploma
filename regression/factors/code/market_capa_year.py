import pandas as pd

file_name = '../data/filtered_blue_chips-2.xlsx'  
file_name = '../data/final_data_for_regression-3.xlsx'
with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for sheet, df in sheets_dict.items():
    sheets_dict[sheet] = df[df['year_month'].str.endswith('-01')]

from collections import defaultdict

market_capitalization = defaultdict(float)  

for sheet, df in sheets_dict.items():
    if sheet == 'RGBI':
        continue
    for index, row in df.iterrows():
        year = row['year_month'][:4]  
        market_capitalization[year] += row['capitalization']


market_capitalization = dict(market_capitalization)

sorted_market_capitalization = dict(sorted(market_capitalization.items()))

print(sorted_market_capitalization)
