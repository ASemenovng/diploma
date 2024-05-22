import pandas as pd
import numpy as np


def process_excel_data(file_name):
    
    with pd.ExcelFile(file_name) as xls:
        sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    
    monthly_returns = {}

    
    for sheet_name, data in sheets_dict.items():
        if sheet_name == 'RGBI':
            continue
        
        for index, row in data.iterrows():
            year_month = row['year_month']
            exchange_rate = row['exchange_rate'] / 100  
            
            div_rate = row.get('div_rate', 0)  
            if np.isnan(div_rate):
                div_rate = 0
            

            
            total_return = exchange_rate + div_rate

            
            if year_month in monthly_returns:
                monthly_returns[year_month].append(total_return)
            else:
                monthly_returns[year_month] = [total_return]

    
    average_monthly_returns = {month: np.mean(returns) for month, returns in monthly_returns.items()}
    
    
    return average_monthly_returns


def update_excel_with_returns(results_file, results):
    
    df_results = pd.read_excel(results_file)

    
    df_results['Rm'] = df_results['date'].map(results).fillna(df_results['Rm'])

    
    with pd.ExcelWriter(results_file, engine='xlsxwriter') as writer:
        df_results.to_excel(writer, index=False)
        writer.save()















def save_results_to_excel(data, output_file):
    
    df = pd.DataFrame(list(data.items()), columns=['Дата', 'Доходность'])

    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)


file_name = '/Users/a.i.semenov/Desktop/Final-Work/result_code/regression/factors/data/upt_data_result.xlsx'
results_file = '/Users/a.i.semenov/Desktop/Final-Work/result_code/regression/factors/data/factors.xlsx'

result_data = process_excel_data(file_name)
print(result_data)


output_file = '../data/результаты_доходности.xlsx'
save_results_to_excel(result_data, output_file)

print("Данные успешно сохранены в файл.")



print("Данные успешно обновлены.")
