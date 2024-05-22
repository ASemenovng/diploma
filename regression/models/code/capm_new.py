import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

def prepare_data(company_file, market_file):
    
    with pd.ExcelFile(company_file) as xls:
        company_data_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    
    market_data = pd.read_excel(market_file)

    
    all_data = []

    
    for ticker, data in company_data_dict.items():
        if ticker == 'RGBI':
            continue
        data['Total_Return'] = data['exchange_rate'] / 100 + data['div_rate'].fillna(0)

        
        merged_data = pd.merge(data, market_data, left_on='year_month', right_on='date', how='left')

        
        
        merged_data['Y'] = (merged_data['Total_Return'] - merged_data['Rf']) * 100  
        merged_data['RmRf'] = merged_data['RmRf'] * 100  

        
        merged_data = merged_data[['year_month', 'Y', 'RmRf']]
        merged_data['year_month'] = pd.to_datetime(merged_data['year_month'], format='%Y-%m')
        merged_data['year'] = merged_data['year_month'].dt.year
        merged_data = merged_data[(merged_data['year'] >= 2010)]
        merged_data['Company'] = ticker  

        all_data.append(merged_data)

    
    final_data = pd.concat(all_data)

    return final_data


prepared_data = prepare_data('../data/upt_data_result.xlsx', '../data/Факторы-2.xlsx')
print(prepared_data)


fixed_effects_data = prepared_data.set_index(['year_month', 'Company'])
print("fixed_effects_data")
print(fixed_effects_data.iloc[67])
print(fixed_effects_data.iloc[182])
print("\n\n\n\n\n\n")
print("fixed_effects_data new")
print(fixed_effects_data)
print("\n\n\n\n\n\n")

X = sm.add_constant(fixed_effects_data[['RmRf']])  


fe_model = sm.OLS(fixed_effects_data['Y'], X).fit()

print("Результаты модели с фиксированными эффектами:")
print(fe_model.summary())
