import pandas as pd

file_name = "../data/data_result_with_factors.xlsx"  


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
    
    if 'book_value' not in df.columns:
        df['book_value'] = pd.NaT

    
    december_data = df[df['year_month'].str.endswith('-12')]

    for index, row in december_data.iterrows():
        assets = row['assets_total']
        liabilities = row['liabilities_total']
        year_month = row['year_month']

        
        if pd.isna(assets):
            print(f"Отсутствуют данные для {ticker}, дата: {year_month}, отсутствует assets_total")
        elif pd.isna(liabilities):
            print(f"Отсутствуют данные для {ticker}, дата: {year_month}, отсутствует liabilities_total")
        else:
            
            df.at[index, 'book_value'] = assets - liabilities


with pd.ExcelWriter("../data/upt_data_result_with_factors.xlsx", engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Обновленный файл успешно сохранен.")