from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

from scipy.stats import shapiro, ttest_ind, mannwhitneyu

file_name = "../data/filtered_blue_chips_with_ep.xlsx"
file_name = "../data/all_data_with_ep.xlsx"


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

final_medians = {2012: 0.0927343941782047, 2013: 0.08746678646783736, 2014: 0.06809013565667602, 2015: 0.07829107371080113, 2016: 0.08470722336794635, 2017: 0.05395670657446295, 2018: 0.05167082554120872, 2019: 0.09202766631031509, 2020: 0.07473287150854784, 2021: 0.0895812096886025, 2022: 0.1110617829017947}

final_medians = {2012: 0.0918695280901907, 2013: 0.08071777954404268, 2014: 0.11408169145305945, 2015: 0.10052922559026031, 2016: 0.08927302364919676, 2017: 0.0944344820115047, 2018: 0.1097372484968202, 2019: 0.1042620164117494, 2020: 0.08232532785882798, 2021: 0.1147796097689749, 2022: 0.11614136521351934}





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
            current_payout = current_data.iloc[0]['e/p']
            if year >= 2013: 
                if prev_year_payout is None or pd.isna(prev_year_payout) or prev_year_payout < final_medians[year - 1]:
                    portfolio_1[f'{year}-12'].append(ticker)
                    print("company ", ticker, " in portfolio_1 with prev_year_payout: ", prev_year_payout, " less than final_medians: ", final_medians[year - 1])
                else:
                    portfolio_2[f'{year}-12'].append(ticker)
                    print("company ", ticker, " in portfolio_2 with prev_year_payout: ", prev_year_payout,
                          " greater than final_medians: ", final_medians[year - 1])
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


portfolio_1_market = create_weighted_returns_dict_portolios(portfolio_1, sheets_dict)
portfolio_2_market = create_weighted_returns_dict_portolios(portfolio_2, sheets_dict)
print("portfolio_1_market: ", portfolio_1_market)
print("portfolio_2_market: ", portfolio_2_market)



for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue

    df['year_month'] = pd.to_datetime(df['year_month']).dt.strftime('%Y-%m')

   
    for date in portfolio_1.keys():

       
        monthly_data = df[df['year_month'] == date]

        if not monthly_data.empty:
           
            exchange_rate = monthly_data['exchange_rate'].values[0] / 100
            if sheet_name == 'IRAO':
                exchange_rate = 0.1

            if exchange_rate > 1 or exchange_rate < -1:
                print("sheet_name: ", sheet_name, " for date: ", date, " with exchange_rate: ", exchange_rate)

            div_rate = monthly_data['div_rate'].values[0]

           
           
           

           
            if sheet_name in portfolio_1[date]:

                cur_cup = portfolio_1_market[date]
               
               
               
               
               
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
               
               
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

               
                portfolio_1_tuples[date].append((weighted_exchange, weighted_div))

           
           
           

           
            if sheet_name in portfolio_2[date]:

                cur_cup = portfolio_2_market[date]
                cur_cup1 = 0
                for t in portfolio_2[date]:
                    if t == 'RGBI':
                        continue
                    cur_ticker_data = sheets_dict.get(t)
                    cur_month_data = cur_ticker_data[cur_ticker_data['year_month'] == date]
                    if cur_month_data.empty:
                        continue
                   
                   
                    cap = cur_month_data['capitalization'].iloc[0] if 'capitalization' in cur_month_data.columns else 0
                    cur_cup1 += cap
               
               
               
               
               
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
               
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

                if sheet_name == 'RTKM':
                    print("div_rate: ", div_rate, " date: ", date)
               
               
                portfolio_2_tuples[date].append((weighted_exchange, weighted_div))



print("test")
print(portfolio_1['2013-01'])
print(portfolio_1_tuples['2013-01'])


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

    print("exchange_rates: ", exchange_rates, " div_yields: ", div_yields, " pd.isna: ", pd.isna(div_yields), " is None: ", div_yields is None)

    return exchange_rates, div_yields


portfolio_1_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_1_avg.items()}
portfolio_2_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_2_avg.items()}



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
df['below ep'] = list(portfolio_1_avg_avg.values())
df['below ep'] = df['below ep'] * 100

df['above ep'] = list(portfolio_2_avg_avg.values())
df['above ep'] = df['above ep'] * 100

print("df")
print(df)


output_filename = "stat_test_for_portfolios_new.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns')





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







cum_portfolio_1_avg = calculate_cumulative_returns_separatly(portfolio_1_avg)
cum_portfolio_2_avg = calculate_cumulative_returns_separatly(portfolio_2_avg)

print("cum_portfolio_1_avg: ", cum_portfolio_1_avg)
print("cum_portfolio_2_avg: ", cum_portfolio_2_avg)


plot_portfolio_returns(cum_portfolio_1_avg, "акций, показатель E/P которых ниже медианы")
plot_portfolio_returns(cum_portfolio_2_avg, "акций, показатель E/P которых выше медианы")

