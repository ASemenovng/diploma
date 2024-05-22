from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

from scipy.stats import shapiro, ttest_ind, mannwhitneyu


file_name = "../data/filtered_blue_chips.xlsx"
file_name = "../data/final_data_for_regression-3.xlsx"



with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

final_medians = {2012: 0.3761421125126635, 2013: 0.2797926646568403, 2014: 0.2006120173335431, 2015: 0.41526354815763744, 2016: 0.4749281288510294, 2017: 0.6015515582188047, 2018: 0.7254633602107892, 2019: 0.5649907269371841, 2020: 0.7047477863057807, 2021: 0.48023611083062445, 2022: 0.657433157726831}
final_medians = {2012: 0.2151024354175791, 2013: 0.2797926646568403, 2014: 0.1927675390909912, 2015: 0.1986543201652122, 2016: 0.30939976884023723, 2017: 0.3456754847129341, 2018: 0.46035017967989633, 2019: 0.4347740417548192, 2020: 0.5241676430033908, 2021: 0.4590011402221228, 2022: 0.5845020978230812}






portfolio_1 = {}
portfolio_2 = {}


for year in range(2013, 2023):
    date_key = f'{year}-12'
    portfolio_1[date_key] = []
    portfolio_2[date_key] = []


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
   
    df['year'] = pd.to_datetime(df['year_month']).dt.year
    df['month'] = pd.to_datetime(df['year_month']).dt.month

    prev_year_payout = None 
   
    for year in range(2012, 2023):
        current_data = df[(df['year'] == year) & (df['month'] == 12)]
        if not current_data.empty:
            current_payout = current_data.iloc[0]['payout_ratio']
            if year >= 2013: 
                if prev_year_payout is None or pd.isna(prev_year_payout) or prev_year_payout < final_medians[year - 1]:
                    portfolio_1[f'{year}-12'].append(ticker)
                else:
                    portfolio_2[f'{year}-12'].append(ticker)
            prev_year_payout = current_payout 




for year in range(2013, 2023):
    date_key = f'{year}-12'
   
    for m in range(1, 12):
        if m <= 9:
            new_key = f'{year}-0{m}'
        else:
            new_key = f'{year}-{m}'
       
       
       
        portfolio_1[new_key] = portfolio_1[date_key]
        portfolio_2[new_key] = portfolio_2[date_key]





def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m')


sorted_portfolio_1_keys = sorted(portfolio_1, key=parse_date)
sorted_portfolio_2_keys = sorted(portfolio_2, key=parse_date)


portfolio_1 = {date: portfolio_1[date] for date in sorted_portfolio_1_keys}
portfolio_2 = {date: portfolio_2[date] for date in sorted_portfolio_2_keys}




print("\nПортфель 1:")
for date, value in portfolio_1.items():
   
    print(f"{date}: {value}")

print("Портфель 2:")
for date, value in portfolio_2.items():
    print(f"{date}: {value}")













portfolio_1_tuples = {date: [] for date in portfolio_1.keys()}
portfolio_2_tuples = {date: [] for date in portfolio_2.keys()}


























































def create_weighted_returns_dict_portolios(capitalization_dict, sheets_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        returns = 0
        for ticker in tickers:
            df = sheets_dict[ticker]
            specific_row = df[df['year_month'] == date]
            if not specific_row.empty:
                cap = specific_row['capitalization'].iloc[
                    0] if 'capitalization' in specific_row.columns else 0
                returns += cap
        returns_dict[date] = returns
    return returns_dict


def create_weighted_returns_dict(capitalization_dict, sorted_market_capitalization, sheets_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        for ticker in tickers:
            if ticker in sheets_dict:
                df = sheets_dict[ticker]
                specific_row = df[df['year_month'] == date]

                if not specific_row.empty:
                    cur_cup = sorted_market_capitalization[date]
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   

                    cap = specific_row['capitalization'].iloc[0] if 'capitalization' in specific_row.columns else 0
                    exchange_rate_frac = specific_row['exchange_rate_frac'].iloc[
                        0] if 'exchange_rate_frac' in specific_row.columns else 0
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(
                        specific_row['div_rate'].iloc[0]) else 0

                    weight = cap / cur_cup if cur_cup else 0 
                   
                   
                   
                    weighted_exchange = exchange_rate_frac * weight
                    weighted_div = div_rate * weight
                    returns_dict[date].append((weighted_exchange, weighted_div))

    print("returns_dict: ", returns_dict)
    return dict(returns_dict)

portfolio_1_market_returns = create_weighted_returns_dict_portolios(portfolio_1, sheets_dict)
portfolio_2_market_returns = create_weighted_returns_dict_portolios(portfolio_2, sheets_dict)
print("portfolio_1_market_returns: ", portfolio_1_market_returns)
print("portfolio_2_market_returns: ", portfolio_2_market_returns)


portfolio_1_tuples = create_weighted_returns_dict(portfolio_2, portfolio_1_market_returns, sheets_dict)
portfolio_2_tuples = create_weighted_returns_dict(portfolio_2, portfolio_2_market_returns, sheets_dict)



print("portfolio_1_tuple:")
for date, value in portfolio_1_tuples.items():
    print(f"{date}: {value}")

print("\nportfolio_2_tuple:")
for date, value in portfolio_2_tuples.items():
    print(f"{date}: {value}")







def average_tuples(tuples_list):
    if not tuples_list:
        return 0, 0 

   
    exchange_rates = [tup[0] for tup in tuples_list if tup[0] is not None]
    div_yields = [tup[1] if tup[1] is not None and not pd.isna(tup[1]) else 0 for tup in tuples_list] 

   
    avg_exchange_rate = np.mean(exchange_rates) * 100 if exchange_rates else 0
    avg_div_yield = np.mean(div_yields) * 100 if div_yields else 0

    avg_exchange_rate = sum(exchange_rates) * 100 if exchange_rates else 0
    avg_div_yield = sum(div_yields) * 100 if div_yields else 0
    avg_div_yield = sum(
        0 if pd.isna(yield_value) else yield_value for yield_value in div_yields) * 100 if div_yields else 0

    return avg_exchange_rate, avg_div_yield



portfolio_1_avg = {date: average_tuples(tuples) for date, tuples in portfolio_1_tuples.items()}
portfolio_2_avg = {date: average_tuples(tuples) for date, tuples in portfolio_2_tuples.items()}



print("portfolio_1_avg:")
for date, value in portfolio_1_avg.items():
    print(f"{date}: {value}")

print("\nportfolio_2_avg:")
for date, value in portfolio_2_avg.items():
    print(f"{date}: {value}")








def sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

   

    return exchange_rates, div_yields




def honest_sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

    print("exchange_rates: ", exchange_rates, " div_yields: ", div_yields, " pd.isna: ", pd.isna(div_yields), " is None: ", div_yields is None)

   
    return exchange_rates + div_yields


portfolio_1_avg_avg = {date: honest_sum_tuple(tuple) / 100 for date, tuple in portfolio_1_avg.items()}
portfolio_2_avg_avg = {date: honest_sum_tuple(tuple) / 100 for date, tuple in portfolio_2_avg.items()}




df = pd.read_excel("stat_test_for_portfolios_new.xlsx")
df['below pr'] = list(portfolio_1_avg_avg.values())
df['below pr'] = df['below pr'] * 100
df['above pr'] = list(portfolio_2_avg_avg.values())
df['above pr'] = df['above pr'] * 100

print("df")
print(df)


output_filename = "stat_test_for_portfolios_new.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns')







portfolio_1_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_1_avg.items()}
portfolio_2_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_2_avg.items()}






print("portfolio_1_avg:")
for date, value in portfolio_1_avg.items():
    print(f"{date}: {value}")

print("\nportfolio_2_avg:")
for date, value in portfolio_2_avg.items():
    print(f"{date}: {value}")











def transform_data(portfolio):
    return {date: (value[0] + (0 if pd.isna(value[1]) else value[1]))
            for date, value in portfolio.items()}


portfolio_1_transformed = transform_data(portfolio_1_avg)
portfolio_2_transformed = transform_data(portfolio_2_avg)


returns_1 = np.array(list(portfolio_1_transformed.values()))
returns_2 = np.array(list(portfolio_2_transformed.values()))


normal_test_1 = shapiro(returns_1)
normal_test_2 = shapiro(returns_2)


u_statistic, p_value = mannwhitneyu(returns_1, returns_2)


print(f"Portfolio 1 normality test p-value: {normal_test_1.pvalue:.3f}")
print(f"Portfolio 2 normality test p-value: {normal_test_2.pvalue:.3f}")
print(f"U-statistic: {u_statistic:.3f}, P-value: {p_value:.3f}")

if normal_test_1.pvalue < 0.05 or normal_test_2.pvalue < 0.05:
    print("Один или оба портфеля не нормальны, применён U-тест Манна-Уитни.")
else:
    print("Оба портфеля имеют нормальное распределение доходностей.")

if p_value < 0.05:
    print("Существуют статистически значимые различия между медианами доходностей портфелей.")
else:
    print("Статистически значимые различия между медианами доходностей портфелей отсутствуют.")










def calculate_cumulative_returns(monthly_returns):
    cumulative_returns = {}
    cumulative_product = 1
    for date, return_value in monthly_returns.items():
        cumulative_product *= (return_value / 100 + 1)
        cumulative_returns[date] = (cumulative_product - 1) * 100
    return cumulative_returns


def calculate_cumulative_returns_separatly(monthly_returns):
    cumulative_returns = {}
    cumulative_product = 1
    for date, tuple_return in monthly_returns.items():
        cumulative_product *= (tuple_return[0] / 100 + 1)
       
        cumulative_returns[date] = (cumulative_product - 1) * 100
    return cumulative_returns


def plot_portfolio_returns(with_rolling_average, portfolio_name):
   
    dates = pd.to_datetime(list(with_rolling_average.keys()))
    values = list(with_rolling_average.values())

    df = pd.DataFrame({'Date': dates, 'Value': values})
    df.set_index('Date', inplace=True)

   
    df['MA'] = df['Value'].rolling(window=6, min_periods=1).mean()

   
    plt.figure(figsize=(12, 6))
    plt.bar(df.index, df['Value'], width=25, color='blue', label=f'Доходность {portfolio_name}')
    plt.plot(df.index, df['MA'], color='red', linestyle='-', linewidth=1, label='Скользящее среднее 6 месяцев')

   
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)

    plt.title(f'Накопленная доходность портфеля {portfolio_name}')
    plt.xlabel('Дата')
    plt.ylabel('Накопленная доходность (%)')
    plt.legend()
    plt.grid(True)
    plt.show()






portfolio_1_avg['2014-03'] = (1, 0)

cum_portfolio_1_avg = calculate_cumulative_returns_separatly(portfolio_1_avg)
cum_portfolio_2_avg = calculate_cumulative_returns_separatly(portfolio_2_avg)

print("cum_portfolio_1_avg: ", cum_portfolio_1_avg)
print("cum_portfolio_2_avg: ", cum_portfolio_2_avg)


plot_portfolio_returns(cum_portfolio_1_avg, "акций, которые не платят или платят ниже медианы")
plot_portfolio_returns(cum_portfolio_2_avg, "акций, которые платят выше медианы")

