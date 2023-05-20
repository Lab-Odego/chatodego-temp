
import pandas as pd

import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from csv import writer
# csv = pd.read_csv("test_restaurant.csv")
# csv = pd.read_csv("restaurant_csv/busan_restaurant.csv")
csv = pd.read_csv("restaurant_csv_folder/busan_restaurant.csv")
print(csv)
print(type(csv))
storName = csv['업소명']
print(type(storName))
data = []
print(storName)



json_data = {}
# file_path = "./restaurants.json"
file_path = "./test.csv"

path = "C:/Users/Young/Desktop/scrapping/chrome_driver/"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(executable_path=path + "chromedriver.exe", options=options)

def correctName(name, location):
    if "점" not in name:
        keyword = name
        query = keyword + " " + location
    else:
        query = name
    query = re.sub(r'\([^)]*\)', '' , query)
    query = re.sub(r'\[[^)]*\]', '' , query)
    query = re.sub(r'\<[^)]*\>', '' , query)
    query = re.sub(r'\{[^)]*\}', '' , query)
    print("==========================["+query+"]==========================")
    return query

def findName(driver):
    name = driver.find_element(by='xpath', value='//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/h2').text
    print(f"가게이름: {name}")
    return name

def findCategory(driver):
    category = driver.find_element(by='xpath', value='//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/span[1]').text
    print(f"가게이름: {category}")
    return category

def findRate(driver):
    rateNum = driver.find_element(by='xpath',value = '//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/a[1]/span[1]').text
    print("rate " + rateNum)
    return rateNum

def findAdress(driver):
    address=driver.find_element(by='xpath',value = '//*[@id="mArticle"]/div[1]/div[2]/div[1]/div/span[1]').text
    print("address: " + address)
    return address
def isPossibleToButton_DetailTimeButton(driver):
    boolean = False
    try:
        driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/ul/li/a/span').click()
        boolean = True
    except:
        boolean = False
        pass
    return boolean
def findTime(driver):
    time1 = []
    try:
        Timelist = driver.find_element(by=By.CLASS_NAME, value = 'list_operation')
        periodTime = Timelist.find_elements(by=By.CLASS_NAME, value = 'txt_operation')
        detailTime = Timelist.find_elements(by=By.CLASS_NAME, value = 'time_operation')
        sleep(0.1)
        if detailTime:
            # time = []
            for i in periodTime:
                time1.append(i.text)
                print(f"영업시간정보: {i.text}")
            
        else:
            print("영업시간정보: null")
            time1.append("null")
    except:
        print("영업시간정보없음")
        time1.append("null")
        pass
    finally:
        # temp.append(time1)
        return time1
def findMenu(driver):
    menus_dic = {}
    try:
        menulist = driver.find_element(by=By.CLASS_NAME, value = 'list_menu')
        menus = menulist.find_elements(by=By.CLASS_NAME, value = 'loss_word')
        menus_price = menulist.find_elements(by=By.CLASS_NAME, value = 'price_menu')
        for a,b in zip(menus,menus_price):
            menus_dic[a.text] = b.text
        for j in menus_dic:
            print("key: {}, value: {}".format(j, menus_dic[j]))
        # content["menu"] = menus_dic
        # temp.append(menus_dic)
    except:
        print("메뉴없음")
        # temp.append("null")
        menus_dic["null"] = "null"
    finally:
        return menus_dic
def csvFindTraffic(idx):
    ######################
    # print는 numpy int 64는 출력이 안됨
    ######################
    traffic = csv.iloc[idx][4]
    print("traffic: " + str(traffic))
    return traffic

# with open('output.csv', mode='w', newline='') as file:
#     writer = writer(file)
#     writer.writerow(['Name', 'Category', 'Rate', 'Address', 'Traffic', 'Time', 'Menu'])

for idx, storeNAME in enumerate(storName):
    # keyword = "카페38.5"
    # query = correctName(keyword, "부산")
    query = correctName(storeNAME, "부산")
    temp = []
    # print("traffic: " + str(csv.iloc[idx, 0])); sleep(0.1)
    # print("traffic: " + str(csv.iloc[idx, 1])); sleep(0.1)
    # print("traffic: " + str(csv.iloc[idx, 2])); sleep(0.1)
    # print("traffic: " + str(csv.iloc[idx, 3])); sleep(0.1)
    # print("traffic: " + str(csv.iloc[idx, 4])); sleep(0.1)
    try:
        kakao_map_search_url = f"https://map.kakao.com/?q={query}"
        driver.get(kakao_map_search_url)
        # sleep(3)
        driver.implicitly_wait(time_to_wait=3)
        
        newlink = driver.find_element(by='xpath',value = '//*[@id="info.search.place.list"]/li[1]/div[5]/div[4]/a[1]').send_keys(Keys.ENTER)
        driver.switch_to.window(driver.window_handles[-1])
        # sleep(1)
        driver.implicitly_wait(time_to_wait=3)
        # ===================NAME======================= #
        name = findName(driver)
        temp.append(name)
        # ===================Category======================= #
        category = findCategory(driver)
        temp.append(category)
        # ===================Rate======================= #
        rate = findRate(driver)
        temp.append(rate)
        # ===================ADDRESS======================= #
        address = findAdress(driver)
        temp.append(address)
        # ===================TRAFFIC======================= #
        traffic = csvFindTraffic(idx)
        temp.append(traffic)
        # ===================TIME======================= #
        time1 = []
        time1 = findTime(driver)
        temp.append(time1)
        # ===================MENU======================= #
        menus_dic1 = {}
        menus_dic1 = findMenu(driver)
        temp.append(menus_dic1)

        with open("output.csv", mode='a', newline='') as file:
            wr = writer(file)
            wr.writerow(temp)
            
    except:
        print("query가 없습니다.")
        driver.switch_to.window(driver.window_handles[-1])
        sleep(0.1)
        # continue
        pass
    else:
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    finally:
        print("temp: " + str(temp))

