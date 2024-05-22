import pandas as pd


file_name = "../data/b-m_tmp.xlsx"
yearly_data_filename = "../data/reformatted_data_08-12.xlsx"


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


yearly_data = pd.read_excel(yearly_data_filename)


for index, row in yearly_data.iterrows():
    year = str(row['Год']).split(".")[0]
    ticker = row['Тикер биржевой']
    net_assets = row['Чистые активы, RUB']

    
    year_month_key = f"{year}-12"

    
    if ticker in sheets_dict:
        df = sheets_dict[ticker]
        
        if year_month_key in df['year_month'].values:
            
            df.loc[df['year_month'] == year_month_key, 'book_value'] = net_assets
        else:
            print(f"Для тикера {ticker} отсутствует запись за месяц {year_month_key}")
    else:
        print(f"Лист для тикера {ticker} отсутствует")


with pd.ExcelWriter("../data/b-m_tmp.xlsx", engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Данные успешно обновлены и записаны в новый файл.")