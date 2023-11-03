# -*- coding: utf-8 -*-
import re
import os
import time
import random
import pandas
import requests
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

def get_page():
    headerText = int(driver.find_element(By.XPATH, '//h4[@class="List-headerText"]/span').text.replace(" 个回答", '').replace(',',''))
    page = 1
    while True:
        try:
            page_number = 8000*page
            js_d = f'scrollTo(0, {page_number})'
            js_u = f'scrollTo(0, 1000)'
            driver.execute_script(js_d)
            time.sleep(random.random()+1)
            driver.execute_script(js_u)
            time.sleep(random.random())
            page += 1

            if headerText > 100:
                try:
                    driver.find_element(By.XPATH,'//button[@class="Button QuestionAnswers-answerButton FEfUrdfMIKpQDJDqkjte Button--blue Button--spread JmYzaky7MEPMFcJDLNMG GMKy5J1UWc7y8NF_V8YA"]')
                    break
                except:
                    driver.find_element(By.XPATH, '//div[@class=" css-0"]/div[@class="List-item"][30]')
                    break
            else:
                driver.find_element(By.XPATH,'//button[@class="Button QuestionAnswers-answerButton FEfUrdfMIKpQDJDqkjte Button--blue Button--spread JmYzaky7MEPMFcJDLNMG GMKy5J1UWc7y8NF_V8YA"]')
                break
        except:
            continue


#创建文件夹
os.makedirs(f'知乎/',exist_ok=True)

#读取txt网址列表#单个网页
with open("知乎标题.txt","r",encoding='utf-8') as file:
    title_data = file.readline().replace('[','').replace(']', '').replace("'",'').split(", ")
#读取txt网址列表#单个网页
with open("知乎网址.txt","r",encoding='utf-8') as file:
    href_data = file.readline().replace('[','').replace(']', '').replace("'",'').split(", ")

options = webdriver.ChromeOptions()
options.debugger_address = '127.0.0.1:9222'
driver = webdriver.Chrome(service=Service(r'd:\selenium\chromedriver.exe'),options=options)
driver.set_page_load_timeout(8)
# driver.implicitly_wait(10)

for index in range(611, len(title_data)):#len(title_data)
    print(index)
    time_list = list()
    content_list = list()
    number_list = list()

    title = title_data[index]
    url = href_data[index]
    print(title)
    print(url)
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, f'//div[@class=" css-0"]/div[@class="List-item"][1]')
    except:
        driver.refresh()
    # driver.refresh()

    get_page()
    headerText = int(driver.find_element(By.XPATH, '//h4[@class="List-headerText"]/span').text.replace(" 个回答", '').replace(',',''))
    for index_index in range(1, 101):#int(headerText)
        try:
            time_data = driver.find_element(By.XPATH, f'//div[@class=" css-0"]/div[@class="List-item"][{index_index}]//div[@class="ContentItem-time"]//span').text.split(" ")[1]
            number = int(driver.find_element(By.XPATH, f'//div[@class=" css-0"]/div[@class="List-item"][{index_index}]//button[@class="Button VoteButton VoteButton--up FEfUrdfMIKpQDJDqkjte"]').get_attribute('aria-label').replace("赞同",'').replace(",",''))
            content = driver.find_element(By.XPATH, f'//div[@class=" css-0"]/div[@class="List-item"][{index_index}]//div[@class="RichContent-inner"]').text.replace("\n",'')

            sj_list = time_data.split('-')
            sj = int(''.join(sj_list))
            if (sj >= 20191227) and (sj <= 20221207) == True:
                time_list.append(time_data)
                number_list.append(number)
                content_list.append(content)

            # print(time_data,number,content)
        except:
            continue



    try:
        max_number = max(number_list)
        number_index = number_list.index(max(number_list))
        sj_max = time_list[number_index]
        content_max = content_list[number_index]
        print("结束")
        print(sj_max,max_number,content_max)

        new_title = re.sub(r'[><"*/|\\:?]', "", title).replace(" ",'')
        #保存为Txt
        with open(f'知乎/{new_title}---{sj_max}.txt', 'a+', encoding="utf-8") as file:
            file.write(str(content_max))
    except:
        continue








