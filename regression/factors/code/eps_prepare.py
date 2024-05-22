import pandas as pd

file_name = "../data/data_with_pr.xlsx"  


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
    if 'eps' not in df.columns:
        df['eps'] = pd.NA  

    last_date = df['year_month'].max()

    for index, row in df.iterrows():
        year_month = row['year_month']

        
        if year_month.endswith('12'):
            net_profit = row['net_profit']
            num_of_shares = df.loc[df['year_month'] == last_date, 'num_of_shares'].iloc[0]

            if pd.isna(net_profit) or pd.isna(num_of_shares):
                
                print(f"Warning: Missing data for {ticker} in {year_month}. Skipping ratio calculation.")
            else:
                
                df.at[index, 'eps'] = net_profit / num_of_shares if num_of_shares != 0 else 0


with pd.ExcelWriter("../data/data_with_eps.xlsx", engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Данные успешно обновлены и записаны в новый файл.")