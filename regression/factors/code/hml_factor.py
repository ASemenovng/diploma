import pandas as pd
from collections import defaultdict
import statistics

from result_code.regression.factors.code.smb_factor import create_weighted_returns_dict, market_capa

black_list = {'MERF', 'VRSB', 'ALBK', 'GTLC', 'ZVEZ', 'CHKZ', 'KRKN', 'ROLO', 'TANL', 'PRFN', 'MRSB', 'USBN', 'VJGZ',
              'YAKG', 'KLSB', 'RUSI', 'VGSB', 'NSVZ', 'PRMB', 'MOBB', 'VDSB', 'IRKT', 'NAUK', 'TGKN', 'APTK', 'RGSS',
              'LNZL', 'ODVA', 'MORI', 'LPSB', 'KTSB', 'ISKJ'}


file_name = "../data/final_data_for_regression-3.xlsx"
file_name = "../data/upt_upt_filtered_bc.xlsx"




with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names if sheet != 'RGBI'}















































all_data = pd.concat(sheets_dict.values(), ignore_index=True)


grouped_data = all_data.groupby('year_month')


median_values = grouped_data['B/M'].median()


median_dict = median_values.to_dict()


print(median_dict)







quantile_70_values = grouped_data['B/M'].quantile(0.70)


quantile_30_values = grouped_data['B/M'].quantile(0.30)


quantile_70_dict = quantile_70_values.to_dict()


print(quantile_70_dict)


quantile_30_dict = quantile_30_values.to_dict()


print(quantile_30_dict)








high_capitalization = defaultdict(list)
low_capitalization = defaultdict(list)


def find_quarter(month):
    if month % 3 == 1:
        return month
    elif month % 3 == 2:
        return month - 1
    else:
        return month - 2


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI' or ticker in black_list:
        continue
    df['year'] = df['year_month'].str.slice(0, 4).astype(int)
    df['month'] = df['year_month'].str.slice(5, 7).astype(int)
    df['quarter_month'] = df['month'].apply(find_quarter)
    df['year_quarter'] = df['year'].astype(str) + '-' + df['quarter_month'].astype(str).str.zfill(2)

    
    for index, row in df.iterrows():
        year_month = row['year_quarter']
        
        
        
        
        if row['B/M'] >= quantile_70_values.get(row['year_month'], 0):
            high_capitalization[year_month].append(ticker)
        elif row['B/M'] <= quantile_30_values.get(row['year_month'], 0):
            low_capitalization[year_month].append(ticker)


high_capitalization = dict(high_capitalization)
low_capitalization = dict(low_capitalization)











for date in high_capitalization:
    high_capitalization[date] = list(set(high_capitalization[date]))

for date in low_capitalization:
    low_capitalization[date] = list(set(low_capitalization[date]))


print("Портфель с B/M выше или равной медианной (уникальные тикеры):")
for date, tickers in high_capitalization.items():
    print(f"{date}: {tickers}")

print("\nПортфель с B/M ниже медианной (уникальные тикеры):")
for date, tickers in low_capitalization.items():
    print(f"{date}: {tickers}")

def fill_missing_quarter_months(cap_dict):
    new_dict = {}
    months_to_add = [1, 2, 3]  

    for date in sorted(cap_dict):
        year, month = map(int, date.split('-'))
        quarter_start_month = 1 + 3 * ((month - 1) // 3)
        for m in months_to_add:
            new_month = quarter_start_month + (m - 1)
            new_date = f"{year}-{new_month:02d}"
            if new_month < month:
                if new_date not in new_dict:  
                    continue
            elif new_month == month:
                new_dict[new_date] = cap_dict[date]
            else:
                if new_month < 13:  
                    new_dict[new_date] = cap_dict[date]

    return new_dict



high_capitalization = fill_missing_quarter_months(high_capitalization)
low_capitalization = fill_missing_quarter_months(low_capitalization)


print("Расширенный B/M high_capitalization:")
for date in sorted(high_capitalization):
    print(f"{date}: {high_capitalization[date]}")

print("\nРасширенный B/M low_capitalization:")
for date in sorted(low_capitalization):
    print(f"{date}: {low_capitalization[date]}")



def create_returns_dict(capitalization_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        for ticker in tickers:
            if ticker in sheets_dict:
                df = sheets_dict[ticker]
                specific_row = df[df['year_month'] == date]
                if not specific_row.empty:
                    exchange_rate_frac = specific_row['exchange_rate_frac'].iloc[0] if 'exchange_rate_frac' in specific_row.columns else 0
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(specific_row['div_rate'].iloc[0]) else 0
                    returns_dict[date].append(exchange_rate_frac + div_rate)
    return dict(returns_dict)


def create_weighted_returns_dict(capitalization_dict, sorted_market_capitalization, sheets_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        year = date[:4]  
        


        for ticker in tickers:
            if ticker in sheets_dict:

                df = sheets_dict[ticker]
                specific_row = df[df['year_month'] == date]

                if not specific_row.empty:
                    cur_cup = 0
                    for t in tickers:
                        cur_ticker_data = sheets_dict.get(ticker)
                        cur_month_data = cur_ticker_data[df['year_month'] == date]
                        cap = cur_month_data['capitalization'].iloc[
                            0] if 'capitalization' in cur_month_data.columns else 0
                        cur_cup += cap

                    cap = specific_row['capitalization'].iloc[0] if 'capitalization' in specific_row.columns else 0
                    exchange_rate_frac = specific_row['exchange_rate_frac'].iloc[
                        0] if 'exchange_rate_frac' in specific_row.columns else 0
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(
                        specific_row['div_rate'].iloc[0]) else 0

                    weight = cap / cur_cup if cur_cup else 0  
                    if weight <= 0.01:
                        print("alert")
                    weighted_exchange = exchange_rate_frac * weight
                    weighted_div = div_rate * weight
                    
                    returns_dict[date].append(weighted_exchange)

    return dict(returns_dict)



high_returns = create_returns_dict(high_capitalization)
low_returns = create_returns_dict(low_capitalization)


high_returns = create_weighted_returns_dict(high_capitalization, market_capa, sheets_dict)
low_returns = create_weighted_returns_dict(low_capitalization, market_capa, sheets_dict)




print("Доходности для портфеля с B/M выше или равной медианной:")
for date, returns in high_returns.items():
    print(f"{date}: {returns}")

print("\nДоходности для портфеля с B/M ниже медианной:")
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


print("Средняя доходность для портфеля с B/M выше или равной медианной:")
for date, avg_return in average_high_returns.items():
    print(f"{date}: {avg_return:.2f}")

print("\nСредняя доходность для портфеля с B/M ниже медианной:")
for date, avg_return in average_low_returns.items():
    print(f"{date}: {avg_return:.2f}")


data = {
    'Date': list(average_high_returns.keys()),
    'High Returns': list(average_high_returns.values()),
    'Low Returns': [average_low_returns[date] for date in average_high_returns.keys()]  
}

df = pd.DataFrame(data)


output_filename = "../data/no_div_weight_hml_factors_bc.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns Summary')

print(f"Данные успешно сохранены в файл {output_filename}")



