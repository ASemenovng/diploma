import pandas as pd

file_name = "../data/b-m_tmp.xlsx"  


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
    
    if 'B/M' not in df.columns:
        df['B/M'] = pd.NaT

    
    df['Year'] = df['year_month'].str[:4]
    grouped = df.groupby('Year')

    
    for year, year_data in grouped:
        
        book_value = year_data.loc[year_data['year_month'] == year + '-12', 'book_value']
        if book_value.empty:
            print(f"Для тикера {ticker}, в году {year} отсутствует book_value за декабрь")
            continue

        
        for idx, row in year_data.iterrows():
            capitalization = row['capitalization']
            if pd.notna(capitalization):
                
                df.at[idx, 'B/M'] = (book_value.iloc[0] / capitalization) if capitalization != 0 else None

    
    del df['Year']


with pd.ExcelWriter("../data/upt_data_result_with_factors_with_book_with_b-m.xlsx", engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Обновление файла завершено, данные успешно сохранены.")