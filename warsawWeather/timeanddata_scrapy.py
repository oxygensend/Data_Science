from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')

urls = [f'https://www.wunderground.com/history/daily/pl/warsaw/EPWA/date/{r}-{m}-{d}'
          for r in range(2005,2021) for m in range(1,13) for d in range(1,32)]


driver = webdriver.Chrome(options=chrome_options)

tab = pd.DataFrame()
year = 2005
month = 1
day = 1
for url in urls:
    driver.get(url)
    try:
        tables = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mat-table.cdk-table.mat-sort.ng-star-inserted")))
    except TimeoutException as ex:
         print("Exception has been thrown. " + str(ex))
         tables = []
         if day == 31 and month == 12:
            year += 1
            month = 1
            day = 0
         elif day == 31:
            month +=1
            day = 0
         day +=1

    for table in tables:
        newTable = pd.read_html(table.get_attribute('outerHTML'))
     
        try:
            newTable[0]['date'] = pd.Timestamp(str(year)+'-'+str(month)+'-'+str(day))
            tab = tab.append(newTable[0].dropna(), ignore_index=True)
            os.system('clear')
            print(str(year)+'-'+str(month)+'-'+str(day))
            
        except ValueError:
            pass
   
        if day == 31 and month == 12:
            year += 1
            month = 1
            day = 0
        elif day==31:
            month +=1
            day = 0

        day +=1
        
tab.to_csv('./warsaw_weather_2005-2020.csv', sep=';',index=False, encoding="UTF-8")
