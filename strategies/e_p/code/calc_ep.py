import pandas as pd

file_name = "../data/data_with_eps.xlsx" 


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue
    print(sheet_name)
   
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')
    december_data = df[df['year_month'].dt.month == 12]

   
    if 'e/p' not in df.columns:
        df['e/p'] = pd.NA

   
    december_data['e/p'] = december_data.apply(lambda row: row['eps'] / row['average_price'] if pd.notna(row['eps']) and row['eps'] > 0 and row['average_price'] > 0 else pd.NA, axis=1)

   
    df.update(december_data[['e/p']])

    df['year_month'] = df['year_month'].dt.strftime('%Y-%m')



with pd.ExcelWriter("../data/all_data_with_ep.xlsx", engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)