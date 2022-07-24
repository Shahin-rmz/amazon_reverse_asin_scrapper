#!/usr/bin/env python
# coding: utf-8

# In[58]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import itertools
import re
from pymongo import MongoClient


# In[64]:


mongo_client = MongoClient()
db = mongo_client.amazon_us_911_180
col = db.products


# # Original

# ad, first raw: B07DLGZH28
# second in search results B07WH8BJSR, B08PSKLDDQ, B07BPC6F3C, B013IJLUQ2

# ## copy

# In[68]:


#initializing Selenium
def scrapper():
    with open ('test.txt') as file:
        for line in file:
            try:
                s = Service('/home/shahin/Downloads/chromedriver')
                driver = webdriver.Chrome(service=s)
                driver.get("https://amazon.com")
                #opening amazon and search for the ASIN
                searchbox = driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
                current_asin = line 

                searchbox.send_keys(current_asin)
                searchbox.send_keys(Keys.RETURN)
                #Get the results and see how many results are in page
                chosen_products = driver.find_elements(By.CLASS_NAME,'s-image')

                #see if there are ads in products by checking Xpath of the "sponsored " label
                feature_dict =[]
                if len(chosen_products) > 1 :
                    ads = True
                    driver.find_element(By.XPATH,"//span[contains(@data-a-popover,'asin={}')]/parent::span/parent::div/parent::div/parent::div/div/h2/a".format(current_asin)).click()
                elif len(chosen_products) <= 1:
                    ads = False
                    try:
                        chosen_products[0].click()
                    except IndexError:
                        mongo_docs = []
                        doc_body = {'data': NAN} 
                        mongo_docs.append(doc_body)
                        result = col.insert_many(mongo_docs)

# ## feature extraction

# In[70]:


                features= driver.find_element(By.ID,'detailBullets_feature_div').find_elements(By.TAG_NAME,'ul')

                for feature in features:
                    feature_dict.append(feature.text)

                new_feature_lst = []
                for i in feature_dict:
                    i = re.split("\:|\n",i)
                    new_feature_lst.append(i)
                    flat_new_list = list(itertools.chain(*new_feature_lst))
                flat_new_list
                for j in flat_new_list:
                    if re.search(";",j):
                        flat_new_list.append('pounds_weight')
                        flat_new_list.append(j.split(';')[-1].split(maxsplit=1)[0])
                        j = j.rsplit(';',1)[0]
                flat_new_list
                result_dict = {flat_new_list[i]: flat_new_list[i + 1] for i in range(0, len(flat_new_list), 2)}
                result_dict['ads'] = ads


            # ## Other features

            # In[71]:


                image_src = driver.find_element(By.XPATH,'//*[@id="landingImage"]').get_attribute('src')
                BSR = driver.find_element(By.XPATH,'//*[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span').text
                title = driver.find_element(By.ID, 'productTitle').get_attribute('innerHTML')
                price = driver.find_element(By.XPATH,'//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]').text
                stars = driver.find_element(By.CLASS_NAME, 'a-icon-alt').get_attribute('innerHTML')
                review_count= driver.find_element(By.XPATH,'//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]').text

                result_dict['image_source'] = image_src
                result_dict['Best Seller Rank'] = BSR
                result_dict['title'] = title
                result_dict['price'] = price
                result_dict['stars'] = stars
                result_dict['review_count'] = review_count


                # In[72]:


                mongo_docs = []
                doc_body = result_dict 
                mongo_docs.append(doc_body)
                result = col.insert_many(mongo_docs)


# In[ ]:




