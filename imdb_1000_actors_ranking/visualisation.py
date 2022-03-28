# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:31:04 2021

@author: Szymon
"""
import json
import pandas as pd
from collections import defaultdict

with open('./result.json') as f:
   data = defaultdict(list)
   
   for item in json.load(f):
        for key in item.keys():
            print(item[key])
            data[key].append(item[key])
    


df = pd.DataFrame(data).drop_duplicates()
df.to_csv('./imdb1000actors.csv', sep=';',index=False, encoding="UTF-8")
pd.set_option("display.max_rows", None, "display.max_columns", None)
