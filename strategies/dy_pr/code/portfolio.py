from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as stats
import seaborn as sns

from scipy.stats import shapiro, ttest_ind, mannwhitneyu

file_name = "../data/all_data_with_ep.xlsx"


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


sheets_dict = {sheet: df for sheet, df in sheets_dict.items() if not df.empty}


all_data = pd.concat(sheets_dict.values(), ignore_index=True)








grouped_data = all_data.groupby('year_month')



def calculate_median(series):
    if series.dropna().empty:
        return 0 
    else:
        return series.median()



median_values = grouped_data['div_rate'].apply(calculate_median)


median_dict_dy = median_values.to_dict()


def aggregate_by_year(data):
    result = {}
    for date, value in data.items():
        year = date.split('-')[0]
        if year not in result:
            result[year] = 0
        result[year] += value
    return result




print(median_dict_dy)

median_dict_pr = {'2012': 0.2151024354175791, '2013': 0.2797926646568403, '2014': 0.1927675390909912, '2015': 0.1986543201652122, '2016': 0.30939976884023723, '2017': 0.3456754847129341, '2018': 0.46035017967989633, '2019': 0.4347740417548192, '2020': 0.5241676430033908, '2021': 0.4590011402221228, '2022': 0.5845020978230812}


H_DY_H_PR = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
H_DY_L_PR = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
L_DY_H_PR = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
L_DY_L_PR = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}

H_DY = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
L_DY = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}


for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue

   
    df['year_month'] = pd.to_datetime(df['year_month'])
    df = df[(df['year_month'] >= '2011-01') & (df['year_month'] <= '2022-12')]

    for year in range(2013, 2023):
       
        first_month_data = df[df['year_month'] == f"{year-1}-01-01"]
        if not first_month_data.empty:
            ticker = first_month_data['ticker'].values[0]
            div_rate = first_month_data['div_rate'].values[0]
            median_value = median_dict_dy.get(f"{year-1}-01")

           
            if pd.isna(div_rate) or div_rate == 0 or div_rate < median_value:
                portfolio = L_DY
            else:
                portfolio = H_DY

           
            for month in range(1, 13):
                portfolio[f"{year}-{month:02d}"].append(ticker)


print("H_DY: ", H_DY)
print("L_DY: ", L_DY)



for date, tickers in H_DY.items():
    if not date.endswith("-12"):
        continue
    for ticker in tickers:
        df = sheets_dict[ticker]
        if ticker == 'RGBI':
            continue
       
        df['year'] = pd.to_datetime(df['year_month']).dt.year
        df['month'] = pd.to_datetime(df['year_month']).dt.month

        year = date.split("-12")[0]
        year = int(year)
        prev_data = df[(df['year'] == year - 1) & (df['month'] == 12)]
        prev_year_payout = prev_data.iloc[0]['payout_ratio']
        if prev_year_payout is None or pd.isna(prev_year_payout) or prev_year_payout < median_dict_pr[str(year - 1)]:
            H_DY_L_PR[f'{year}-12'].append(ticker)
        else:
            H_DY_H_PR[f'{year}-12'].append(ticker)

       
       
       
       
       
       
       
       
       
       
       
       


for date, tickers in L_DY.items():
    if not date.endswith("-12"):
        continue
    for ticker in tickers:
        df = sheets_dict[ticker]
        if ticker == 'RGBI':
            continue
       
        df['year'] = pd.to_datetime(df['year_month']).dt.year
        df['month'] = pd.to_datetime(df['year_month']).dt.month

        year = date.split("-12")[0]
        year = int(year)
       
        prev_data = df[(df['year'] == year - 1) & (df['month'] == 12)]
        if prev_data.empty:
            prev_data = df[(df['year'] == year - 1) & (df['month'] == 5)]
        if prev_data.empty:
            continue
       
       
        prev_year_payout = prev_data.iloc[0]['payout_ratio']
        if prev_year_payout is None or pd.isna(prev_year_payout) or prev_year_payout < median_dict_pr[str(year - 1)]:
            L_DY_L_PR[f'{year}-12'].append(ticker)
        else:
            L_DY_H_PR[f'{year}-12'].append(ticker)

       
       
       
       
       
       
       
       
       
       
       
       


def remove_duplicates(dictionary):
    for key in dictionary:
        dictionary[key] = list(set(dictionary[key]))
    return dictionary


L_DY_H_PR = remove_duplicates(L_DY_H_PR)
L_DY_L_PR = remove_duplicates(L_DY_L_PR)
H_DY_L_PR = remove_duplicates(H_DY_L_PR)
H_DY_H_PR = remove_duplicates(H_DY_H_PR)



for year in range(2013, 2023):
    date_key = f'{year}-12'
   
    for m in range(1, 12):
        if m <= 9:
            new_key = f'{year}-0{m}'
        else:
            new_key = f'{year}-{m}'
        L_DY_H_PR[new_key] = L_DY_H_PR[date_key]
        L_DY_L_PR[new_key] = L_DY_L_PR[date_key]
        H_DY_L_PR[new_key] = H_DY_L_PR[date_key]
        H_DY_H_PR[new_key] = H_DY_H_PR[date_key]




print("L_DY_H_PR: ", L_DY_H_PR)
print("L_DY_L_PR: ", L_DY_L_PR)
print("H_DY_L_PR: ", H_DY_L_PR)
print("H_DY_H_PR: ", H_DY_H_PR)

portfolio_L_DY_H_PR_tuples = {date: [] for date in L_DY_H_PR.keys()}
portfolio_L_DY_L_PR_tuples = {date: [] for date in L_DY_L_PR.keys()}
portfolio_H_DY_L_PR_tuples = {date: [] for date in H_DY_L_PR.keys()}
portfolio_H_DY_H_PR_tuples = {date: [] for date in H_DY_H_PR.keys()}

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
                    exchange_rate = specific_row['exchange_rate'].iloc[
                        0] if 'exchange_rate' in specific_row.columns else 0
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(
                        specific_row['div_rate'].iloc[0]) else 0

                    weight = cap / cur_cup if cur_cup else 0 
                    weighted_exchange = exchange_rate / 100 * weight
                    weighted_div = div_rate * weight
                    returns_dict[date].append((weighted_exchange, weighted_div))

    print("returns_dict: ", returns_dict)
    return dict(returns_dict)




portfolio_L_DY_H_PR_market_returns = create_weighted_returns_dict_portolios(L_DY_H_PR, sheets_dict)
portfolio_L_DY_L_PR_market_returns = create_weighted_returns_dict_portolios(L_DY_L_PR, sheets_dict)
portfolio_H_DY_L_PR_market_returns = create_weighted_returns_dict_portolios(H_DY_L_PR, sheets_dict)
portfolio_H_DY_H_PR_market_returns = create_weighted_returns_dict_portolios(H_DY_H_PR, sheets_dict)


portfolio_L_DY_H_PR_tuples = create_weighted_returns_dict(L_DY_H_PR, portfolio_L_DY_H_PR_market_returns, sheets_dict)
portfolio_L_DY_L_PR_tuples = create_weighted_returns_dict(L_DY_L_PR, portfolio_L_DY_L_PR_market_returns, sheets_dict)
portfolio_H_DY_L_PR_tuples = create_weighted_returns_dict(H_DY_L_PR, portfolio_H_DY_L_PR_market_returns, sheets_dict)
portfolio_H_DY_H_PR_tuples = create_weighted_returns_dict(H_DY_H_PR, portfolio_H_DY_H_PR_market_returns, sheets_dict)


print("portfolio_L_DY_H_PR_tuples:")
for date, value in portfolio_L_DY_H_PR_tuples.items():
    print(f"{date}: {value}")

print("\nportfolio_L_DY_L_PR_tuples:")
for date, value in portfolio_L_DY_L_PR_tuples.items():
    print(f"{date}: {value}")

print("portfolio_H_DY_L_PR_tuples:")
for date, value in portfolio_H_DY_L_PR_tuples.items():
    print(f"{date}: {value}")

print("\nportfolio_H_DY_H_PR_tuples:")
for date, value in portfolio_H_DY_H_PR_tuples.items():
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



portfolio_L_DY_H_PR_avg = {date: average_tuples(tuples) for date, tuples in portfolio_L_DY_H_PR_tuples.items()}
portfolio_L_DY_L_PR_avg = {date: average_tuples(tuples) for date, tuples in portfolio_L_DY_L_PR_tuples.items()}
portfolio_H_DY_L_PR_avg = {date: average_tuples(tuples) for date, tuples in portfolio_H_DY_L_PR_tuples.items()}
portfolio_H_DY_H_PR_avg = {date: average_tuples(tuples) for date, tuples in portfolio_H_DY_H_PR_tuples.items()}


print("portfolio_L_DY_H_PR_avg:")
for date, value in portfolio_L_DY_H_PR_avg.items():
    print(f"{date}: {value}")

print("\nportfolio_L_DY_L_PR_avg:")
for date, value in portfolio_L_DY_L_PR_avg.items():
    print(f"{date}: {value}")

print("portfolio_H_DY_L_PR_avg:")
for date, value in portfolio_H_DY_L_PR_avg.items():
    print(f"{date}: {value}")

print("\nportfolio_H_DY_H_PR_avg:")
for date, value in portfolio_H_DY_H_PR_avg.items():
    print(f"{date}: {value}")



def sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

    return exchange_rates, div_yields


portfolio_L_DY_H_PR_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_L_DY_H_PR_avg.items()}
portfolio_L_DY_L_PR_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_L_DY_L_PR_avg.items()}
portfolio_H_DY_L_PR_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_H_DY_L_PR_avg.items()}
portfolio_H_DY_H_PR_avg = {date: sum_tuple(tuple) for date, tuple in portfolio_H_DY_H_PR_avg.items()}



def honest_sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

   
    return exchange_rates + div_yields


h_portfolio_L_DY_H_PR_avg = {date: honest_sum_tuple(tuple) for date, tuple in portfolio_L_DY_H_PR_avg.items()}
h_portfolio_L_DY_L_PR_avg = {date: honest_sum_tuple(tuple) for date, tuple in portfolio_L_DY_L_PR_avg.items()}
h_portfolio_H_DY_L_PR_avg = {date: honest_sum_tuple(tuple) for date, tuple in portfolio_H_DY_L_PR_avg.items()}
h_portfolio_H_DY_H_PR_avg = {date: honest_sum_tuple(tuple) for date, tuple in portfolio_H_DY_H_PR_avg.items()}







df = pd.read_excel("stat_test_for_portfolios_new.xlsx")
df['L_DY_H_PR'] = list(h_portfolio_L_DY_H_PR_avg.values())

df['L_DY_L_PR'] = list(h_portfolio_L_DY_L_PR_avg.values())

df['H_DY_L_PR'] = list(h_portfolio_H_DY_L_PR_avg.values())
df['H_DY_H_PR'] = list(h_portfolio_H_DY_H_PR_avg.values())


output_filename = "stat_test_for_portfolios_new.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns')


print("df")
df = df.to_string(max_colwidth=None)
print(df)










def transform_data(portfolio):
    return {date: (value[0])
            for date, value in portfolio.items()}
   
   

portfolio_1_transformed = transform_data(portfolio_H_DY_L_PR_avg)
portfolio_2_transformed = transform_data(portfolio_L_DY_H_PR_avg)


returns_1 = np.array(list(portfolio_1_transformed.values()))
returns_2 = np.array(list(portfolio_2_transformed.values()))


plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.histplot(returns_1, kde=True, color='blue')
plt.title('Гистограмма доходностей портфеля')
plt.xlabel('Доходность')
plt.ylabel('Частота')


plt.subplot(1, 2, 2)
stats.probplot(returns_1, dist="norm", plot=plt)
plt.title('Q-Q plot доходностей портфеля')

plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.histplot(returns_2, kde=True, color='blue')
plt.title('Гистограмма доходностей портфеля')
plt.xlabel('Доходность')
plt.ylabel('Частота')


plt.subplot(1, 2, 2)
stats.probplot(returns_2, dist="norm", plot=plt)
plt.title('Q-Q plot доходностей портфеля')

plt.tight_layout()
plt.show()


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




cum_portfolio_L_DY_H_PR_avg = calculate_cumulative_returns_separatly(portfolio_L_DY_H_PR_avg)
cum_portfolio_L_DY_L_PR_avg = calculate_cumulative_returns_separatly(portfolio_L_DY_L_PR_avg)
cum_portfolio_H_DY_L_PR_avg = calculate_cumulative_returns_separatly(portfolio_H_DY_L_PR_avg)
cum_portfolio_H_DY_H_PR_avg = calculate_cumulative_returns_separatly(portfolio_H_DY_H_PR_avg)

print("cum_portfolio_L_DY_H_PR_avg: ", cum_portfolio_L_DY_H_PR_avg)
print("cum_portfolio_L_DY_L_PR_avg: ", cum_portfolio_L_DY_L_PR_avg)
print("cum_portfolio_H_DY_L_PR_avg: ", cum_portfolio_H_DY_L_PR_avg)
print("cum_portfolio_H_DY_H_PR_avg: ", cum_portfolio_H_DY_H_PR_avg)


plot_portfolio_returns(cum_portfolio_L_DY_H_PR_avg, "L_DY_H_PR")
plot_portfolio_returns(cum_portfolio_L_DY_L_PR_avg, "L_DY_L_PR")
plot_portfolio_returns(cum_portfolio_H_DY_L_PR_avg, "H_DY_L_PR")
plot_portfolio_returns(cum_portfolio_H_DY_H_PR_avg, "H_DY_H_PR")
