import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



file_name = "../data/filtered_blue_chips.xlsx"
file_name = "../data/final_data_for_regression-3.xlsx"


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


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


print("\nmerged_dict by Month and Year:")
for date, tickers in merged_dict.items():
    print(f"{date}: {tickers}")




no_dividend_portfolio_tuples = {date: [] for date in no_dividend_portfolio.keys()}
below_median_portfolio_tuples = {date: [] for date in below_median_portfolio.keys()}
above_median_portfolio_tuples = {date: [] for date in above_median_portfolio.keys()}

merged_dict_portfolio_tuples = {date: [] for date in merged_dict.keys()}














































for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue

    df['year_month'] = pd.to_datetime(df['year_month']).dt.strftime('%Y-%m')

   
    for date in no_dividend_portfolio.keys():
        year_month_target = pd.Timestamp(date)

       
        monthly_data = df[df['year_month'] == date]

        if not monthly_data.empty:
            exchange_rate = monthly_data['exchange_rate_frac'].values[0]
            if exchange_rate > 1 or exchange_rate < -1:
                print("sheet_name: ", sheet_name, " for date: ", date, " with exchange_rate: ", exchange_rate)
                if sheet_name in no_dividend_portfolio[date]:
                    print("no_dividend_portfolio\n")
                if sheet_name in below_median_portfolio[date]:
                    print("below_median_portfolio\n")
                if sheet_name in above_median_portfolio[date]:
                    print("above_median_portfolio\n")

            div_rate = monthly_data['div_rate'].values[0]

           
            if sheet_name in no_dividend_portfolio[date]:
                no_dividend_portfolio_tuples[date].append((exchange_rate, div_rate))

           
            if sheet_name in below_median_portfolio[date]:
                below_median_portfolio_tuples[date].append((exchange_rate, div_rate))

           
            if sheet_name in above_median_portfolio[date]:
                above_median_portfolio_tuples[date].append((exchange_rate, div_rate))

           
           
           

           
            if sheet_name in merged_dict[date]:

                cur_cup = 0
                for t in merged_dict[date]:
                    if not monthly_data.empty:
                        cp = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                        cur_cup += cp
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
                if sheet_name == 'RTKM':
                    print("weight: ", weight, " cap: ", cap, " cur_cup: ", cur_cup, " for date: ", date)
               
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

                merged_dict_portfolio_tuples[date].append((weighted_exchange, weighted_div))




print("No Dividend Portfolio by Month and Year:")
for date, value in no_dividend_portfolio_tuples.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio by Month and Year:")
for date, value in below_median_portfolio_tuples.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio by Month and Year:")
for date, value in above_median_portfolio_tuples.items():
    print(f"{date}: {value}")

print("\nmerged_dict_portfolio_tuples by Month and Year:")
for date, value in merged_dict_portfolio_tuples.items():
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
merged_dict_portfolio = {date: average_tuples(tuples) for date, tuples in merged_dict_portfolio_tuples.items()}



print("No 1 Dividend Portfolio Average by Month and Year:")
for date, value in no_dividend_avg.items():
    print(f"{date}: {value}")

print("\nBelow 1 Median Dividend Portfolio Average by Month and Year:")
for date, value in below_median_avg.items():
    print(f"{date}: {value}")

print("\nAbove 1 Median Dividend Portfolio Average by Month and Year:")
for date, value in above_median_avg.items():
    print(f"{date}: {value}")

print("\nmerged_dict_portfolio Average by Month and Year:")
for date, value in merged_dict_portfolio.items():
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


honest_merged_avg = {date: honest_sum_tuple(tuple) / 100 for date, tuple in merged_dict_portfolio.items()}



data = {
    'merged div': list(honest_merged_avg.values())
}
df = pd.read_excel("stat_test_for_portfolios.xlsx")
df['merged dy'] = list(honest_merged_avg.values())
df['merged dy'] = df['merged dy'] * 100

print(df)


output_filename = "stat_test_for_portfolios.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns')







no_dividend_avg = {date: sum_tuple(tuple) for date, tuple in no_dividend_avg.items()}
below_median_avg = {date: sum_tuple(tuple) for date, tuple in below_median_avg.items()}
above_median_avg = {date: sum_tuple(tuple) for date, tuple in above_median_avg.items()}
merged_dict_portfolio = {date: sum_tuple(tuple) for date, tuple in merged_dict_portfolio.items()}



print("No Dividend Portfolio Average by Month and Year:")
for date, value in no_dividend_avg.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio Average by Month and Year:")
for date, value in below_median_avg.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio Average by Month and Year:")
for date, value in above_median_avg.items():
    print(f"{date}: {value}")

print("\nmerged_dict_portfolio Average by Month and Year:")
for date, value in merged_dict_portfolio.items():
    print(f"{date}: {value}")


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


above_median_avg['2014-03'] = 1





cum_mixed_avg = calculate_cumulative_returns_separatly(merged_dict_portfolio)






plot_portfolio_returns(cum_mixed_avg, "Смешанный")

print("cum_mixed_avg: ", cum_mixed_avg)