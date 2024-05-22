import pandas as pd

file_name = '../data/sh_upt_upt_data_result (1).xlsx'  


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
    try:
        
        last_date = df['year_month'].max()
        num_of_shares = df.loc[df['year_month'] == last_date, 'num_of_shares'].iloc[0]
        if pd.isna(num_of_shares):
            raise ValueError("Количество акций отсутствует")

        
        df['capitalization'] = df['average_price'] * num_of_shares

    except IndexError:
        print(f"Предупреждение: Данный лист {ticker} не содержит информацию за 2022-12.")
    except ValueError as e:
        print(f"Предупреждение: Для компании {ticker} {str(e)}.")


with pd.ExcelWriter('../data/new_upt_upt_data_result (1).xlsx', engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)
