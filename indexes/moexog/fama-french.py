import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.stattools import durbin_watson
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA




file_path = "upt_blue_for_reg_with_dogs (14).xlsx"

df = pd.read_excel(file_path)

df['date'] = pd.to_datetime(df['date'])



df.set_index('date', inplace=True)



features = ['WDY', 'WPR']
pca = PCA(n_components=1)
principalComponent = pca.fit_transform(df[features])
df['PC1'] = principalComponent[:, 0]
df['PC1'] = 0.5 * df['WDY'] + 0.5 * df['WPR']
df['PC1_NO_DIV'] = 0.5 * df['WDY_NO_DIV'] + 0.5 * df['WPR_NO_DIV']
df['PC1_ALL'] = 0.5 * df['WDY_ALL'] + 0.5 * df['WPR_ALL']
df['interaction'] = df['WDY'] * df['WPR']
df['interaction_NO_DIV'] = df['WDY_NO_DIV'] * df['WPR_NO_DIV'] * 100
df['interaction_ALL'] = df['WDY_ALL'] * df['WPR_ALL']

print("Веса компонентов:", pca.components_)


df['meogtr_cur_Rf'] = df['meogtr'] - df['rgbitr_prc_frac']
df['mcftr_prc_new_Rf'] = df['mcftr_prc_new'] - df['rgbitr_prc_frac']



y = df['moexogRf']

X = df[['RmRf']]
X = df[['RmRf', 'WSMB', 'WHML']]
X = df[['RmRf', 'WSMB', 'WHML', 'WDY']]



vif = pd.DataFrame()
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['variable'] = X.columns

print("vif")
print(vif)





correlation_matrix = X.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Матрица корреляций')
plt.show()


X = sm.add_constant(X)




result = adfuller(df['WSMB'])

print("\nfor WSMB:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


result = adfuller(df['WHML'])

print("\nfor WHML:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


result = adfuller(df['WDY'])

print("\nfor WDY:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


result = adfuller(df['WPR'])

print("\nfor WPR:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


result = adfuller(df['PC1'])

print("\nfor C1:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


result = adfuller(df['interaction'])

print("\nfor interaction:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))





result = adfuller(df['moexogRf'])

print("\nfor moexogRf:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))

result = adfuller(df['RmRf'])
print("\nfor RmRf:")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))



model = sm.OLS(y, X)






results = model.fit(cov_type='HC1')



print(results.summary())




residuals = results.resid


correlation = residuals.corr(y)
print("Корреляция между остатками и moexogRf:", correlation)



sns.histplot(residuals, kde=True)
plt.title('Распределение остатков регрессии')
plt.xlabel('Остатки')
plt.ylabel('Частота')
plt.show()








sm.qqplot(results.resid, line='s')
plt.title('QQ-plot of Residuals')
plt.show()



jb_stat, jb_p_value, _, _ = jarque_bera(residuals)
print('Jarque-Bera Test: Statistics=%.3f, p-value=%.3f' % (jb_stat, jb_p_value))
if jb_p_value > 0.05:
    print("Остатки можно считать распределенными нормально (по критерию Харке-Берра).")
else:
    print("Остатки не распределены нормально (по критерию Харке-Берра).")




stat, p_value = shapiro(results.resid)
print('Shapiro-Wilk Test: Statistics=%.3f, p-value=%.3f' % (stat, p_value))
if p_value > 0.05:
    print("Остатки можно считать распределенными нормально (по критерию Шапиро-Уилка).")
else:
    print("Остатки не распределены нормально (по критерию Шапиро-Уилка).")


bp_test = het_breuschpagan(results.resid, results.model.exog)
labels = ['Lagrange Multiplier Statistic', 'p-value',
          'f-value', 'f p-value']
print(dict(zip(labels, bp_test)))
if bp_test[1] > 0.05:
    print('Остатки гомоскедастичны (по тесту Бреуша-Пагана).')
else:
    print('В остатках присутствует гетероскедастичность (по тесту Бреуша-Пагана).')




dw_statistic = durbin_watson(results.resid)

print(f'Durbin-Watson statistic: {dw_statistic}')


if dw_statistic < 1.5:
    print("Присутствует положительная автокорреляция.")
elif dw_statistic > 2.5:
    print("Присутствует отрицательная автокорреляция.")
else:
    print("Автокорреляция отсутствует.")

