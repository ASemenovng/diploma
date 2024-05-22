import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


file_name = "../data/filtered_blue_chips_upt.xlsx"


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


median_payout_ratios = {}


for ticker, data in sheets_dict.items():
    if ticker == 'RGBI':
        continue

   
    december_data = data[data['year_month'].str.endswith('-12')]

   
    for year in range(2012, 2023):
        year_str = f"{year}-12" 
        year_data = december_data[december_data['year_month'] == year_str]

       
        valid_data = year_data.dropna(subset=['payout_ratio'])

       
        if not valid_data.empty:
            median_value = valid_data['payout_ratio'].median()
            if median_value < 0:
                print("for company: ", ticker, " in ", year, " median_value: ", median_value)
            if year in median_payout_ratios:
                median_payout_ratios[year].append(median_value)
            else:
                median_payout_ratios[year] = [median_value]


final_medians = {year: pd.Series(values).median() for year, values in median_payout_ratios.items()}

print(final_medians)








file_name_for_all = "../data/data_with_pr.xlsx"


with pd.ExcelFile(file_name_for_all) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


median_payout_ratios_for_all = {}


for ticker, data in sheets_dict.items():
    if ticker == 'RGBI':
        continue
   
    december_data = data[data['year_month'].str.endswith('-12')]

   
    for year in range(2012, 2023):
        year_str = f"{year}-12" 
        year_data = december_data[december_data['year_month'] == year_str]

       
        valid_data = year_data.dropna(subset=['payout_ratio'])

       
        if not valid_data.empty:
            median_value = valid_data['payout_ratio'].median()
            if year in median_payout_ratios_for_all:
                median_payout_ratios_for_all[year].append(median_value)
            else:
                median_payout_ratios_for_all[year] = [median_value]


final_medians_for_all = {year: pd.Series(values).median() for year, values in median_payout_ratios_for_all.items()}

print("final_medians_for_all: ", final_medians_for_all)










plt.figure(figsize=(10, 6))
plt.bar(final_medians_for_all.keys(), final_medians_for_all.values(), color='skyblue')
plt.xlabel('Год')
plt.ylabel('Медианный payout_ratio (%)')
plt.title('Медианный payout_ratio по годам')
plt.xticks(list(final_medians_for_all.keys()), [str(year) for year in final_medians_for_all.keys()])
plt.grid(True)
plt.show()

final_medians = {year: value for year, value in sorted(final_medians.items())}
print("final_medians: ", final_medians)



final_medians = {year: value * 100 for year, value in sorted(final_medians.items())}



final_medians_for_all = {year: value * 100 for year, value in sorted(final_medians_for_all.items())}



years = list(final_medians_for_all.keys())
values_for_all = list(final_medians_for_all.values())
values_final_medians = list(final_medians.values())


bar_width = 0.35 
index = np.arange(len(years)) 


plt.figure(figsize=(12, 7))
bar1 = plt.bar(index, values_for_all, bar_width, label='Все акции', color='skyblue')
bar2 = plt.bar(index + bar_width, values_final_medians, bar_width, label='голубые фишки', color='red')


plt.xlabel('Год')
plt.ylabel('Медианный Payout Ratio (%)')
plt.title('Сравнение медианных Payout Ratios по годам')
plt.xticks(index + bar_width / 2, years) 
plt.legend()


plt.grid(True)
plt.tight_layout()
plt.show()
