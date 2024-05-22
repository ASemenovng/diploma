import pandas as pd

file_name = "../data/data_without_pr.xlsx"  


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
    if 'payout_ratio' not in df.columns:
        df['payout_ratio'] = pd.NA  

    for index, row in df.iterrows():
        year_month = row['year_month']

        
        if year_month.endswith('12'):
            net_profit = row['net_profit']
            dividend_payout = row['dividend_payout_RUB']

            if pd.isna(net_profit) or pd.isna(dividend_payout):
                
                print(f"Warning: Missing data for {ticker} in {year_month}. Skipping ratio calculation.")
            else:
                
                df.at[index, 'payout_ratio'] = dividend_payout / net_profit if net_profit != 0 else 0


with pd.ExcelWriter("../data/data_with_pr.xlsx", engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Данные успешно обновлены и записаны в новый файл.")