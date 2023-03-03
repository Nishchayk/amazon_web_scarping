#This is automation for amazon web scarping only didn't try other website
#if you want to try other website there will only few changes should be done in xpath
#lets start the coding
###################################start##############################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from tabulate import tabulate
import pandas as pd
import math

class amazon_web_scarping():
    def __init__(self,seaching):
        self.searching = seaching
    def list_items (self):
        self.titles = []
        self.descriptions = []
        self.hyperlink = []
        self.prices = []
        self.ratings =[]
    def bring_the_browser(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.searching)
        time.sleep(5)
    def collecting_the_data(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        results = soup.find_all('div', {"data-component-type": "s-search-result"})
        for i in range(len(results)):
            item = results[i]
            atag = item.h2.a
            title = atag.text.strip()
            self.titles.append(title)
            description = atag.text.strip()
            self.descriptions.append(description)
            url = "https://www.amazon.com" + atag.get('href')
            self.hyperlink.append(url)
            parent_price = item.find('span', 'a-price')
            try:
                price = parent_price.text.strip().split("AED")
            except:
                price = "NA"
            self.prices.append(price[1])
            try:
                rating = item.i.text
            except:
                rating = "NA"
            self.ratings.append(rating)
    def automatic_click (self):
        time.sleep(10)
        count = 0
        i = True
        while i:
            try:
                self.collecting_the_data()
                time.sleep(30)
                next_pages = self.driver.find_element(By.XPATH, "//a[normalize-space()='Next']").click()
                time.sleep(10)
                count +=1
                print(count)
            except:
                count +=1
                print(count)
                break
    def creating_excel (self):
        self.header = ["product_name","product_description","product_link","product_price","product_rate"]
        c = 0
        tabulate_data = []
        for name,desc,link,money,rate in zip(self.titles,self.descriptions,self.hyperlink,self.prices,self.ratings):
            c += 1
            tabulate_data.append([name,desc,link,money,rate])
            self.summary_table = tabulate(tabulate_data, headers=self.header)
        df = pd.DataFrame(tabulate_data, columns=self.header)
        df.to_excel("amaxonwed_scariping.xlsx",sheet_name="amazonscarping")

link = "https://www.amazon.ae/s?k=perfumes&i=beauty&rh=n%3A11497859031%2Cp_89%3ALattafa&dc&page=1&crid=KLDI5V2720MR&qid=1677336169&rnid=15703921031&sprefix=perfumes%2Caps%2C340&ref=sr_pg_1"
ama = amazon_web_scarping(link)
ama.list_items()
ama.bring_the_browser()
ama.automatic_click()
ama.creating_excel()
