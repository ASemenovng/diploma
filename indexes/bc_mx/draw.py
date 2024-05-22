import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
import xml.etree.ElementTree as ET
from datetime import datetime


def read_xml_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def aggregate_data(xml_data):
    root = ET.fromstring(xml_data)
    index_data = defaultdict(list)

    for row in root.findall('.//row'):
        trade_date = row.get("TRADEDATE")
        close_value = float(row.get("CLOSE").replace(',', '.'))
        date_obj = datetime.strptime(trade_date, "%Y-%m-%d")
        month_year = date_obj.strftime("%Y-%m")
        index_data[month_year].append((date_obj, close_value))

   
    min_date_and_close = {}
    for key, values in index_data.items():
        min_date = min(values, key=lambda x: x[0])[0]
        close_for_min_date = [v[1] for v in values if v[0] == min_date][0]
        min_date_and_close[key] = (key, close_for_min_date)

    data_result = pd.DataFrame(list(min_date_and_close.values()), columns=["Дата", "CLOSE"])
    data_result.sort_values("Дата", inplace=True)
    return data_result





def plot_data(data1, label1, data2, label2):
    plt.figure(figsize=(10, 5))

    dates1 = mdates.date2num(data1['Дата'])

   
    width = 20

   
    plt.bar(dates1, data1['PctChange'], width=width, label=label1, align='center')

   
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1, 6]))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(''))
    plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%b %Y'))

    plt.gca().xaxis.set_tick_params(which='major', size=0)
    plt.gca().xaxis.set_tick_params(which='minor', rotation=45)

    plt.title('Спред доходностей индексов MOEXBC и MCXSM')
    plt.xlabel('Дата')
    plt.ylabel('Процентное изменение')
    plt.legend()

    plt.gcf().autofmt_xdate()
    plt.show()




file_path = 'MOEXBC.xml'
xml_content = read_xml_file(file_path)
data_mmvb = aggregate_data(xml_content)
print(data_mmvb)


file_path = 'MCXSM.xml'
xml_content = read_xml_file(file_path)
data_rts = aggregate_data(xml_content)
print(data_rts)




def add_percentage_change(df):
    df['PctChange'] = df['CLOSE'].pct_change() * 100
    df['PctChange'].fillna(0, inplace=True)
    return df

data_mmvb = add_percentage_change(data_mmvb)
data_rts = add_percentage_change(data_rts)

print("MMVB Data with Percentage Change:")
print(data_mmvb)
print("\nRTS Data with Percentage Change:")
print(data_rts)




plot_data(data_mmvb, 'MOEXBC', data_rts, 'MCXSM')

merged_data = pd.merge(data_mmvb[['Дата', 'PctChange']], data_rts[['Дата', 'PctChange']],
                       on='Дата', how='outer', suffixes=('_mmvb', '_rts'))


merged_data['Multiplier_mmvb'] = 1 + merged_data['PctChange_mmvb'] / 100
merged_data['Multiplier_rts'] = 1 + merged_data['PctChange_rts'] / 100


merged_data['CumReturn_mmvb'] = merged_data['Multiplier_mmvb'].cumprod()
merged_data['CumReturn_rts'] = merged_data['Multiplier_rts'].cumprod()

print(merged_data[['Дата', 'CumReturn_mmvb', 'CumReturn_rts']])





merged_data['PctChange'] = merged_data['CumReturn_mmvb'] * 100 - merged_data['CumReturn_rts'] * 100

difference_data = merged_data[['Дата', 'PctChange']]

print(difference_data)

plot_data(difference_data, 'MOEXBC/MCXSM', data_rts, 'MCXSM')
