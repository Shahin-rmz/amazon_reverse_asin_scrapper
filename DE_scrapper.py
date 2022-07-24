#!/usr/bin/env python
# coding: utf-8

# In[28]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import itertools
import re
from pymongo import MongoClient


# In[29]:
number = 2935

mongo_client = MongoClient()
db = mongo_client.Amazon_de
col = db.produkten


# # Original

# ad, first raw: B07DLGZH28
# second in search results B07WH8BJSR, B08PSKLDDQ, B07BPC6F3C, B013IJLUQ2

# ## copy

# In[81]:


#initializing Selenium
chrome_options = Options()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
# ## feature extraction

# In[82]:

def feature_extraction():
    try:
        mongo_docs = []
            
        feature1_titles= driver.find_element(By.ID,'productDetails_techSpec_section_1').find_elements(By.TAG_NAME,'th')
        feature1_answers= driver.find_element(By.ID,'productDetails_techSpec_section_1').find_elements(By.TAG_NAME,'td')

        features2_titles = driver.find_element(By.ID,'productDetails_detailBullets_sections1').find_elements(By.TAG_NAME,'th')
        features2_answers = driver.find_element(By.ID,'productDetails_detailBullets_sections1').find_elements(By.TAG_NAME,'td')

        for f1 in range(len(feature1_titles)):
            feature_dict.append(feature1_titles[f1].text)
            feature_dict.append(feature1_answers[f1].text)
        for f2 in range(len(features2_titles)):
            feature_dict.append(features2_titles[f2].text)
            feature_dict.append(features2_answers[f2].text)
        result_dict = {feature_dict[i]: feature_dict[i + 1] for i in range(0, len(feature_dict), 2)}
        result_dict['number'] = number
        result_dict['ads'] = ads
        try:
            image_src = driver.find_element(By.XPATH,'//*[@id="landingImage"]').get_attribute('src')
            result_dict['image_source'] = image_src   
        except:
            pass
        try:
            title = driver.find_element(By.ID, 'productTitle').get_attribute('innerHTML')
            result_dict['title'] = title
        except:
            pass
        try:
            price = driver.find_element(By.XPATH,'//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]').text
            result_dict['price'] = price
        except:
            pass



        doc_body = result_dict 
        mongo_docs.append(doc_body)
        result = col.insert_many(mongo_docs)
    except:
        pass


# In[ ]:


with open('DE_2.txt') as f:
    for line in f.readlines():
        try:
            number += 1
            s = Service('/home/shahin/Downloads/chromedriver')
            driver = webdriver.Chrome(service=s,options = chrome_options)
            driver.get("https://amazon.de")
            #cookies
            driver.find_element(By.ID,'sp-cc-customize').click()
            driver.implicitly_wait(3)
            driver.find_element(By.CLASS_NAME,'a-button-input').click()

            #opening amazon and search for the ASIN
            searchbox = driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
            current_asin = line.strip() 

            searchbox.send_keys(current_asin)
            searchbox.send_keys(Keys.RETURN)
            #Get the results and see how many results are in page
            chosen_products = driver.find_elements(By.CLASS_NAME,'s-image')




            #see if there are ads in products by checking Xpath of the "sponsored " label
            feature_dict =[]
            if len(chosen_products) > 1 :
                ads = True
                driver.find_element(By.XPATH,"//span[contains(@data-a-popover,'asin={}')]/parent::span/parent::div/parent::div/parent::div/div/h2/a".format(current_asin)).click()
                feature_extraction()
            elif len(chosen_products) <= 1:
                ads = False
                try:
                    chosen_products[0].click()
                    feature_extraction()
                except IndexError:
                    mongo_docs = []
                    doc_body = {'data': NAN} 
                    mongo_docs.append(doc_body)
                    result = col.insert_many(mongo_docs)
        except:
            pass
