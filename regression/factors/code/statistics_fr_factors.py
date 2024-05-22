import pandas as pd
from collections import defaultdict
import statistics
import numpy as np
from scipy.stats import shapiro, ttest_1samp, wilcoxon


file_name = "../data/upt_blue_for_reg_with_dogs (12).xlsx"


df = pd.read_excel(file_name)

df = df[df['date'] < pd.to_datetime('2022-01')]


return_differences = np.array(df['RmRf'])
return_differences = np.array(df['WSMB'])
return_differences = np.array(df['WHML'])
return_differences = np.array(df['WDY'])
return_differences = np.array(df['WPR'])
return_differences = np.array(0.5 * df['WDY'] + 0.5 * df['WPR'])
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
