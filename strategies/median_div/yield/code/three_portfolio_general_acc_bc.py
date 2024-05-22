from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as stats
import seaborn as sns
from scipy.stats import shapiro, ttest_ind



file_name = "../data/filtered_blue_chips.xlsx"
file_name = "../data/final_data_for_regression-3.xlsx"


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


median_dict = median_values.to_dict()


print(median_dict)







no_dividend_portfolio = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
below_median_portfolio = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
above_median_portfolio = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}


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
            median_value = median_dict.get(f"{year-1}-01")

           
            if pd.isna(div_rate) or div_rate == 0:
                portfolio = no_dividend_portfolio
            elif div_rate < median_value:
                portfolio = below_median_portfolio
            else:
                portfolio = above_median_portfolio

           
            for month in range(1, 13):
                portfolio[f"{year}-{month:02d}"].append(ticker)


print("No Dividend Portfolio by Month and Year:")
for date, value in no_dividend_portfolio.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio by Month and Year:")
for date, value in below_median_portfolio.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio by Month and Year:")
for date, value in above_median_portfolio.items():
    print(f"{date}: {value}")






merged_dict = {}


for date in no_dividend_portfolio:
   
    combined_set = set(no_dividend_portfolio[date] + below_median_portfolio[date])
   
    merged_dict[date] = list(combined_set)






no_dividend_portfolio_tuples = {date: [] for date in no_dividend_portfolio.keys()}
below_median_portfolio_tuples = {date: [] for date in below_median_portfolio.keys()}
above_median_portfolio_tuples = {date: [] for date in above_median_portfolio.keys()}
merged_dict_portfolio_tuples = {date: [] for date in merged_dict.keys()}






















































































































































































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

    return dict(returns_dict)

no_dividend_market_returns = create_weighted_returns_dict_portolios(no_dividend_portfolio, sheets_dict)
below_median_market_returns = create_weighted_returns_dict_portolios(below_median_portfolio, sheets_dict)
above_median_capitalization = create_weighted_returns_dict_portolios(above_median_portfolio, sheets_dict)
print("no_dividend_market_returns: ", no_dividend_market_returns)
print("below_median_market_returns: ", below_median_market_returns)
print("above_median_capitalization: ", above_median_capitalization)


no_dividend_portfolio_tuples = create_weighted_returns_dict(no_dividend_portfolio, no_dividend_market_returns, sheets_dict)
below_median_portfolio_tuples = create_weighted_returns_dict(below_median_portfolio, below_median_market_returns, sheets_dict)
above_median_portfolio_tuples = create_weighted_returns_dict(above_median_portfolio, above_median_capitalization, sheets_dict)





print("No Dividend Portfolio by Month and Year:")
for date, value in no_dividend_portfolio_tuples.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio by Month and Year:")
for date, value in below_median_portfolio_tuples.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio by Month and Year:")
for date, value in above_median_portfolio_tuples.items():
    print(f"{date}: {value}")







def average_tuples(tuples_list):
    if not tuples_list:
        return 0, 0 

   
    exchange_rates = [tup[0] for tup in tuples_list if tup[0] is not None]
    div_yields = [tup[1] if tup[1] is not None else 0 for tup in tuples_list] 

   
    avg_exchange_rate = np.mean(exchange_rates) * 100 if exchange_rates else 0
    avg_div_yield = np.mean(div_yields) * 100 if div_yields else 0

    avg_exchange_rate = sum(exchange_rates) * 100 if exchange_rates else 0
    avg_div_yield = sum(div_yields) * 100 if div_yields else 0
    avg_div_yield = sum(
        0 if pd.isna(yield_value) else yield_value for yield_value in div_yields) * 100 if div_yields else 0

    return avg_exchange_rate, avg_div_yield



no_dividend_avg = {date: average_tuples(tuples) for date, tuples in no_dividend_portfolio_tuples.items()}
below_median_avg = {date: average_tuples(tuples) for date, tuples in below_median_portfolio_tuples.items()}
above_median_avg = {date: average_tuples(tuples) for date, tuples in above_median_portfolio_tuples.items()}


print("No 1 Dividend Portfolio Average by Month and Year:")
for date, value in no_dividend_avg.items():
    print(f"{date}: {value}")

print("\nBelow 1 Median Dividend Portfolio Average by Month and Year:")
for date, value in below_median_avg.items():
    print(f"{date}: {value}")

print("\nAbove 1 Median Dividend Portfolio Average by Month and Year:")
for date, value in above_median_avg.items():
    print(f"{date}: {value}")


def sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

    print("exchange_rates: ", exchange_rates, " div_yields: ", div_yields, " pd.isna: ", pd.isna(div_yields), " is None: ", div_yields is None)

   
    return exchange_rates, div_yields

   
   
   
   

def honest_sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

    print("exchange_rates: ", exchange_rates, " div_yields: ", div_yields, " pd.isna: ", pd.isna(div_yields), " is None: ", div_yields is None)

   
    return exchange_rates + div_yields


honest_no_dividend_avg = {date: honest_sum_tuple(tuple) / 100 for date, tuple in no_dividend_avg.items()}
honest_below_median_avg = {date: honest_sum_tuple(tuple) / 100 for date, tuple in below_median_avg.items()}
honest_above_median_avg = {date: honest_sum_tuple(tuple) / 100 for date, tuple in above_median_avg.items()}


data = {
    'Date': list(honest_no_dividend_avg.keys()),
    'no div': list(honest_no_dividend_avg.values()),
    'below': [honest_below_median_avg[date] for date in honest_no_dividend_avg.keys()],
    'above': [honest_above_median_avg[date] for date in honest_no_dividend_avg.keys()]
}

df = pd.DataFrame(data)


output_filename = "../data/three_portfolio_returns.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns Summary')





no_dividend_avg = {date: sum_tuple(tuple) for date, tuple in no_dividend_avg.items()}
below_median_avg = {date: sum_tuple(tuple) for date, tuple in below_median_avg.items()}
above_median_avg = {date: sum_tuple(tuple) for date, tuple in above_median_avg.items()}


print("No Dividend Portfolio Average by Month and Year:")
for date, value in no_dividend_avg.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio Average by Month and Year:")
for date, value in below_median_avg.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio Average by Month and Year:")
for date, value in above_median_avg.items():
    print(f"{date}: {value}")










def transform_data(portfolio):
    return {date: (value[0] + (0 if pd.isna(value[1]) else value[1]))
            for date, value in portfolio.items()}


portfolio_1_transformed = transform_data(no_dividend_avg)
portfolio_2_transformed = transform_data(below_median_avg)
portfolio_3_transformed = transform_data(above_median_avg)



returns_1 = np.array(list(portfolio_1_transformed.values()))
returns_2 = np.array(list(portfolio_2_transformed.values()))
returns_3 = np.array(list(portfolio_3_transformed.values()))


data = {
    'Date': list(honest_no_dividend_avg.keys()),
    'no dy': list(returns_1),
    'below dy': list(returns_2),
    'above dy': list(returns_3)
}

df = pd.DataFrame(data)


output_filename = "stat_test_for_portfolios.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns')










def remove_outliers(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
   
    return data[(data >= lower_bound) & (data <= upper_bound)]


def equalize_arrays(arr1, arr2):
    min_length = min(len(arr1), len(arr2))
    return arr1[:min_length], arr2[:min_length]


returns_1_no_outliers = remove_outliers(returns_1)
returns_2_no_outliers = remove_outliers(returns_2)


returns_1, returns_2 = equalize_arrays(returns_1_no_outliers, returns_2_no_outliers)


print(f"Size of returns_1_final: {len(returns_1)}")
print(f"Size of returns_2_final: {len(returns_2)}")



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


t_statistic, p_value = ttest_ind(returns_1, returns_2)


print(f"Portfolio 1 normality test p-value: {normal_test_1.pvalue:.3f}")
print(f"Portfolio 2 normality test p-value: {normal_test_2.pvalue:.3f}")
print(f"T-statistic: {t_statistic:.3f}, P-value: {p_value:.3f}")

if normal_test_1.pvalue < 0.05 or normal_test_2.pvalue < 0.05:
    print("Один или оба портфеля не прошли тест на нормальность распределения.")
else:
    print("Оба портфеля имеют нормальное распределение доходностей.")

if p_value < 0.05:
    print("Существуют статистически значимые различия между средними доходностями портфелей.")
else:
    print("Статистически значимые различия между средними доходностями портфелей отсутствуют.")
















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
        cumulative_product += (tuple_return[1] / 100)
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


above_median_avg['2014-03'] = (1, 0)







cum_no_dividend_avg = calculate_cumulative_returns_separatly(no_dividend_avg)
cum_below_median_avg = calculate_cumulative_returns_separatly(below_median_avg)
cum_above_median_avg = calculate_cumulative_returns_separatly(above_median_avg)






print("cum_no_dividend_avg: ", cum_no_dividend_avg)
print("cum_below_median_avg: ", cum_below_median_avg)
print("cum_above_median_avg: ", cum_above_median_avg)





plot_portfolio_returns(cum_no_dividend_avg, "Без Дивидендов")
plot_portfolio_returns(cum_below_median_avg, "Ниже медианы")
plot_portfolio_returns(cum_above_median_avg, "Выше медианы")
