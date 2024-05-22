import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


file_path = 'data_for_reg_upt_upt_1.xlsx'
file_path = 'upt_blue_for_reg_with_dogs (11).xlsx'
df = pd.read_excel(file_path)
df['PC1'] = 0.5 * df['WDY'] + 0.5 * df['WPR']
df['interaction'] = df['WDY'] * df['WPR']



columns = ['depoRmRf', 'WSMB', 'WHML', 'WSOE', 'WDY', 'WPR']
columns = ['RmRf', 'WSMB', 'WHML', 'WSOE', 'WDY', 'WPR', 'PC1', 'interaction']


df[columns] = df[columns] * 100


results = pd.DataFrame(index=columns, columns=['Среднее', 'Стандартное отклонение', 'Минимум', 'Максимум'])


for column in columns:
    results.at[column, 'Среднее'] = df[column].mean()
    results.at[column, 'Стандартное отклонение'] = df[column].std()
    results.at[column, 'Минимум'] = df[column].min()
    results.at[column, 'Максимум'] = df[column].max()


print(results)


X = df[['depoRmRf', 'WSMB', 'WHML', 'WSOE', 'WDY', 'WPR']] 


correlation_matrix = X.corr()


plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Матрица корреляций')
plt.show()


