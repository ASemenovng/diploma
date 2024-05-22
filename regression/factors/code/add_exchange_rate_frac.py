import pandas as pd

file_name = "../data/data_with_eps.xlsx"  


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for sheet_name, df in sheets_dict.items():
    
    if 'exchange_rate' in df.columns:
        
        df['exchange_rate_frac'] = df['exchange_rate'] / 100
    else:
        print(f"'exchange_rate' column missing in {sheet_name}")


with pd.ExcelWriter("../data/final_data_for_regression.xlsx", engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Данные успешно обновлены и записаны в новый файл.")

