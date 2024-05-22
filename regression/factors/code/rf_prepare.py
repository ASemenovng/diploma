import pandas as pd


file_name = '../data/Прошлые данные - RGBI Индекс государственных облигаций РФ.csv'  
data = pd.read_csv(file_name, sep=',', decimal=',', parse_dates=['Дата'], dayfirst=True)


data['Дата'] = pd.to_datetime(data['Дата'], format='%d.%m.%Y')
data = data.sort_values(by='Дата')  


result_data = data[['Дата', 'Цена']]


output_file_name = '../data/rgbi.xlsx'
result_data.to_excel(output_file_name, index=False)

print("Данные успешно сохранены в файл:", output_file_name)
