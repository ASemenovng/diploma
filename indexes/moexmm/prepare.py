import pandas as pd

file_path = 'Прошлые данные - Индекс ММВБ - Металлургия и горнодобыча.csv'
df = pd.read_csv(file_path, delimiter=',', quotechar='"', parse_dates=['Дата'], dayfirst=True, decimal=',')

df['Цена'] = df['Цена'].str.replace('.', '').str.replace(',', '.').astype(float)

df.sort_values('Дата', inplace=True)

df['prc'] = df['Цена'].pct_change()

result_df = df[['Дата', 'Цена', 'prc']]


result_file_path = 'moexmm.xlsx'
result_df.to_excel(result_file_path, index=False)

print("Результаты сохранены в файл:", result_file_path)