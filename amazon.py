from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


path = r"your chromdriver file path\chromedriver"
driver = webdriver.Chrome(path)


web = "https://www.amazon.in/"
driver.get(web)
driver.maximize_window()


wait = WebDriverWait(driver, 10)


search = wait.until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
search_button = wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button")))

search.send_keys("laptops under 50000")
search_button.click()

wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))

products_name = driver.find_elements_by_xpath('//h2//span[contains(@class,"a-text-normal")]')
products_price = driver.find_elements_by_xpath('//span[@class="a-price"]//span[@class="a-price-whole"]')
products_link = driver.find_elements_by_xpath('//h2/a')

names = []
prices = []
links = []

for count, product_name in enumerate(products_name):
    try:
        name = product_name.text
        names.append(name)
        
        price = products_price[count].text
        prices.append(price)
        
        link = products_link[count].get_attribute('href')
        links.append(link)
        
        print(f"Product name is: {name}, Price: ₹{price}, link: {link}")
    except IndexError:
        continue

driver.quit()

df_products = pd.DataFrame(
    {"product": names, 
     "price": prices,
     "link": links
     })

df_products.to_csv(r"amazon_products-1.csv", index=False)
print(df_products)
