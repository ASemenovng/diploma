import pandas as pd
from collections import defaultdict
import statistics
import numpy as np
from scipy.stats import shapiro, ttest_1samp,  ttest_rel, wilcoxon
from statsmodels.stats.descriptivestats import sign_test
import matplotlib.pyplot as plt


file_name = "stat_test_for_portfolios_new-2.xlsx"





df = pd.read_excel(file_name)

df = df[pd.to_datetime(df['Date']) < pd.to_datetime('2022-01')]











portfolio1 = np.array(df['H_DY_L_PR'])

portfolio2 = np.array(df['L_DY_H_PR'])











return_differences = portfolio1 - portfolio2

return_differences = np.array(df['RmRf'])
return_differences = np.array(df['WSMB'])
return_differences = np.array(df['WHML'])
return_differences = np.array(df['WDY'])
return_differences = np.array(df['WPR'])
return_differences = np.array(df['WDY'] * df['WPR'])































normality_test = shapiro(return_differences)
print(f"Normality test p-value: {normality_test.pvalue}")


if normality_test.pvalue < 0.1:
    print("Данные не распределены нормально.")
   
    wilcoxon_test_result = wilcoxon(return_differences - 0)
    print(f"Wilcoxon test statistic: {wilcoxon_test_result.statistic}, p-value: {wilcoxon_test_result.pvalue}")

   
    if wilcoxon_test_result.pvalue < 0.1:
        print(
            "Среднее значимо отличается от нуля, есть статистические основания полагать, что средний доход отличается.")
    else:
        print("Нет статистических оснований предполагать, что средний доход значимо отличается от нуля.")
else:
    print("Данные распределены нормально.")
   

    t_statistic, p_value = ttest_1samp(return_differences, 0)
    print(f"T-test t-statistic: {t_statistic}, p-value: {p_value}")
    print(f"{p_value:.8f}")


   
    if p_value < 0.1:
        print(
            "Среднее значимо отличается от нуля, есть статистические основания полагать, что средний доход отличается.")
    else:
        print("Нет статистических оснований предполагать, что средний доход значимо отличается от нуля.")





test_statistic, p_value = sign_test(return_differences, 0)
print("\n")
print(f"Robust median test statistic: {test_statistic}, p-value: {p_value}")


if p_value < 0.1:
    print("Средняя доходность портфеля статистически значимо отличается от нуля.")
else:
    print("Нет статистических оснований предполагать, что средняя доходность портфеля значимо отличается от нуля.")












def bootstrap(data, num_samples):
    indices = np.random.randint(0, len(data), size=(num_samples, len(data)))
    samples = data[indices]
    sample_means = np.mean(samples, axis=1)
    return sample_means


num_samples = 10000
bootstrap_means = bootstrap(return_differences, num_samples)


ci_lower = np.percentile(bootstrap_means, 5)
ci_upper = np.percentile(bootstrap_means, 95)

print(f"95% интервал доверия для разницы доходностей: ({ci_lower}, {ci_upper})")


plt.hist(bootstrap_means, bins=50, alpha=0.6, color='b')
plt.axvline(ci_lower, color='r', linestyle='dashed', linewidth=2)
plt.axvline(ci_upper, color='r', linestyle='dashed', linewidth=2)
plt.title('Bootstrapped Distribution of Differences in Returns')
plt.show()

