import pandas as pd
from collections import defaultdict
import statistics
import numpy as np
from scipy.stats import shapiro, ttest_1samp


from result_code.regression.factors.code.smb_factor import create_weighted_returns_dict, market_capa

black_list = {'MERF', 'VRSB', 'ALBK', 'GTLC', 'ZVEZ', 'CHKZ', 'KRKN', 'ROLO', 'TANL', 'PRFN', 'MRSB', 'USBN', 'VJGZ',
              'YAKG', 'KLSB', 'RUSI', 'VGSB', 'NSVZ', 'PRMB', 'MOBB', 'VDSB', 'IRKT', 'NAUK', 'TGKN', 'APTK', 'RGSS',
              'LNZL', 'ODVA', 'MORI', 'LPSB', 'KTSB', 'ISKJ'}


file_name = "../data/upt_upt_filtered_bc.xlsx"



with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names if sheet != 'RGBI'}












































all_data = pd.concat(sheets_dict.values(), ignore_index=True)


grouped_data = all_data.groupby('year_month')



def calculate_median(series):
    if series.dropna().empty:
        return 0  
    else:
        return series.median()


median_values = grouped_data['div_rate'].apply(calculate_median)


median_dict = median_values.to_dict()


print(median_dict)


high_div_portfolio = {f"{year}-{month:02d}": [] for year in range(2012, 2023) for month in range(1, 13)}
low_div_portfolio = {f"{year}-{month:02d}": [] for year in range(2012, 2023) for month in range(1, 13)}


for year in range(2012, 2023):
    
    january_key = f"{year}-01"
    january_median = median_dict.get(january_key)

    
    january_data = all_data[(all_data['year_month'] == january_key) & (all_data['div_rate'].notna())]

    high_div_tickers = january_data[january_data['div_rate'] >= january_median]['ticker'].tolist()
    low_div_tickers = january_data[january_data['div_rate'] < january_median]['ticker'].tolist()

    
    for month in range(1, 13):
        month_key = f"{year}-{month:02d}"
        high_div_portfolio[month_key].extend(high_div_tickers)
        low_div_portfolio[month_key].extend(low_div_tickers)


for year in range(2012, 2012):  
    for month in range(1, 13):  
        key = f"{year}-{month:02d}"  
        high_div_portfolio[key] = []  



print("High dividend yield portfolio:")
for key, value in high_div_portfolio.items():
    print(f"{key}: {value}")

print("\nLow dividend yield portfolio:")
for key, value in low_div_portfolio.items():
    print(f"{key}: {value}")



high_div_returns = {}
low_div_returns = {}


def create_returns_dict(capitalization_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        
        if len(tickers) == 0:
            returns_dict[date].append(0)
        for ticker in tickers:
            if ticker in sheets_dict:
                df = sheets_dict[ticker]
                specific_row = df[df['year_month'] == date]
                if not specific_row.empty:
                    exchange_rate_frac = specific_row['exchange_rate_frac'].iloc[0] if 'exchange_rate_frac' in specific_row.columns else 0
                    print("for ticker: ", ticker, " in date: ", date, " dr: ", specific_row['div_rate'].iloc[0],  " isna: ", pd.isna(specific_row['div_rate'].iloc[0]))
                    print("for ticker: ", ticker, " in date: ", date, " exchange_rate_frac: ", specific_row['exchange_rate_frac'].iloc[0],
                          " isna: ", pd.isna(specific_row['exchange_rate_frac'].iloc[0]))
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(specific_row['div_rate'].iloc[0]) else 0
                    returns_dict[date].append(exchange_rate_frac + div_rate)
    return dict(returns_dict)


high_returns = create_returns_dict(high_div_portfolio)
low_returns = create_returns_dict(low_div_portfolio)



high_returns = create_weighted_returns_dict(high_div_portfolio, market_capa, sheets_dict)
low_returns = create_weighted_returns_dict(low_div_portfolio, market_capa, sheets_dict)







print("Доходности для портфеля с div_rate выше или равной медианной:")
for date, returns in high_returns.items():
    print(f"{date}: {returns}")

print("\nДоходности для портфеля с div_rate ниже медианной:")
for date, returns in low_returns.items():
    print(f"{date}: {returns}")


def calculate_average_returns(returns_dict):
    average_returns = {}
    for date, returns in returns_dict.items():
        if returns:  
            average_returns[date] = statistics.mean(returns)
            average_returns[date] = sum(returns)
        else:
            average_returns[date] = 0  
    return average_returns


average_high_returns = calculate_average_returns(high_returns)
average_low_returns = calculate_average_returns(low_returns)


print("Средняя доходность для портфеля с div_rate выше или равной медианной:")
for date, avg_return in average_high_returns.items():
    print(f"{date}: {avg_return:.2f}")

print("\nСредняя доходность для портфеля с div_rate ниже медианной:")
for date, avg_return in average_low_returns.items():
    print(f"{date}: {avg_return:.2f}")


data = {
    'Date': list(average_high_returns.keys()),
    'High Returns': list(average_high_returns.values()),
    'Low Returns': [average_low_returns[date] for date in average_high_returns.keys()]  
}

df = pd.DataFrame(data)


output_filename = "../data/no_div_weight_dy_factors_bc.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns Summary')

print(f"Данные успешно сохранены в файл {output_filename}")




df['Return Differences'] = df['High Returns'] - df['Low Returns']


return_differences = np.array(df['Return Differences'])


normality_test = shapiro(return_differences)
print(f"Normality test p-value: {normality_test.pvalue}")


if normality_test.pvalue < 0.05:
    print("Данные не распределены нормально.")
else:
    print("Данные распределены нормально.")


t_statistic, p_value = ttest_1samp(return_differences, 0)
print(f"T-test t-statistic: {t_statistic}, p-value: {p_value}")


if p_value < 0.05:
    print("Среднее значимо отличается от нуля, есть статистические основания полагать, что средний доход отличается.")
else:
    print("Нет статистических оснований предполагать, что средний доход значимо отличается от нуля.")

