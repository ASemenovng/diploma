import requests
import pandas as pd
import xml.etree.ElementTree as et

from final.create_dataset import read

tickers = read("../data/tmp")

res = []

for t in tickers:
    
    url = "https://iss.moex.com/iss/securities/" + t

    
    response = requests.get(url)

    
    if response.status_code == 200:
        
        root = et.fromstring(response.content)

        
        rows = root.findall(".//row")

        
        issue_size = None

        
        for row in rows:
            if row.get('name') == 'ISSUESIZE':
                issue_size = row.get('value')
                break

        
        if issue_size:
            
            
            res.append((t, issue_size))
        else:
            print("Данные о количестве акций в обращении не найдены.")
    else:
        print("Ошибка при запросе страницы:", response.status_code)

print(res)




































