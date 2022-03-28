from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=opts)
driver.get('https://www.olx.pl/d/oferta/mieszkanie-2-pok-bohaterow-wrzesnia-35m2-przy-parku-nowe-CID3-IDGCXzp.html#da965dda4a')

rps_wrapper = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ul.css-sfcl1s")))


for table in rps_wrapper:
    newTable = pd.read_html(table.get_attribute('outerHTML'))
    print(newTable)