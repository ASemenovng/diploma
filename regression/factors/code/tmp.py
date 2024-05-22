import json

import pandas as pd
import requests

base_url = "http://iss.moex.com/iss/history/engines/stock/markets/index/boards/SNDX/securities.json" 
response = requests.get(base_url) 
result = json.loads(response.text)
col_name = result['history']['columns'] 
data_index = pd.DataFrame(columns = col_name)

print(data_index)

url_index = 'http://iss.moex.com/iss/history/engines/stock/markets/index/boards/SNDX/securities/rgbitr.json' 

response = requests.get(url_index)
result = json.loads(response.text)
resp_date = result['history']['data']

data_index  = pd.DataFrame(resp_date, columns = col_name)

a = len(resp_date)

b = 100
while a == 100:
    url_opt = '?start=' + str(b)
    url_next_page  = (url_index + url_opt)
    response = requests.get(url_next_page)
    result = json.loads(response.text)
    resp_date = result['history']['data']
    data_next_page = pd.DataFrame(resp_date, columns = col_name)
    data_index  = pd.concat([data_index, data_next_page], ignore_index=True)
    a = len(resp_date)
    b = b + 100

print(data_index)


j = requests.get('http://iss.moex.com/iss/engines/stock/markets/shares/securities/RGBITR/candles.json?from=2023-05-25&till=2023-09-01&interval=24').json()
data = [{k : r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
frame = pd.DataFrame(data)

print(frame)

