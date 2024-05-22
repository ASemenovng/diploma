import pandas as pd
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


file_path = 'RGBITR.xml'
xml_content = read_xml_file(file_path)
data_meogtr = aggregate_data(xml_content)
print(data_meogtr)

def add_percentage_change(df):
    df['PctChange'] = df['CLOSE'].pct_change() * 100
    df['PctChange'].fillna(0, inplace=True)
    return df


data_meogtr = add_percentage_change(data_meogtr)


result_file_path = 'RGBITR.xlsx'
data_meogtr.to_excel(result_file_path, index=False)
