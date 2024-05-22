import pandas as pd


data = pd.read_excel('../data/result_data-3.xlsx')


data['Принадлежность к госсектору'].fillna('нет', inplace=True)


data['цена акций'] = pd.to_numeric(data['цена акций'], errors='coerce')


filtered_data = data[(data['Принадлежность к госсектору'] == 'да') | (data['Принадлежность к госсектору'] == 'нет')].groupby('Тикер биржевой').first()


ownership_dict = filtered_data['Принадлежность к госсектору'].apply(lambda x: 1 if x == 'да' else 0).to_dict()

print(ownership_dict)

with pd.ExcelFile('../data/upt_data_result.xlsx') as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}



for sheet_name, data in sheets_dict.items():
    if sheet_name in ownership_dict:
        state_value = ownership_dict[sheet_name]
        data['state_property'] = state_value  
    else:
        
        print(f"Warning: No state property data for {sheet_name}. Filling with default value 0.")
        

updated_file_name = "../data/upt_upt_data_result.xlsx"  
with pd.ExcelWriter(updated_file_name, engine='xlsxwriter') as writer:
    for sheet_name, data in sheets_dict.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)
