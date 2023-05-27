import pandas as pd
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup
import re
import numpy as np
import math
# from csv import writer
import csv


class RestaurantScraper:
    def __init__(self, csv_path, output_path, driver_path):
        self.csv_path = csv_path
        self.output_path = output_path
        self.driver_path = driver_path
        self.driver = None
    
    def run(self):
        csv_data = pd.read_csv(self.csv_path)
        # store_names = csv_data['업소명']
        store_names = csv_data['상호명']
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(executable_path = self.driver_path, options=options)
        
        with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Category', 'Rate', 'Address', 'Time', 'Menu'])
        
            for idx, store_name in enumerate(store_names):
                # query = self.correct_name(store_name, "부산")
                query = store_name
                if type(csv_data['지점명'].iloc[idx]) == str:
                    query += (" " + csv_data['지점명'].iloc[idx])
                
                print(query)
                temp = []
                
                if idx == 5:
                    break
                
                try:
                    kakao_map_search_url = f"https://map.kakao.com/?q={query}"
                    self.driver.get(kakao_map_search_url)
                    self.driver.implicitly_wait(time_to_wait=3)
                    
                    new_link = self.driver.find_element(by='xpath', value='//*[@id="info.search.place.list"]/li[1]/div[5]/div[4]/a[1]')
                    new_link.send_keys(Keys.ENTER)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.implicitly_wait(time_to_wait=3)
                    
                    name = self.find_name()
                    temp.append(name)
                    category = self.find_category()
                    temp.append(category)
                    rate = self.find_rate()
                    temp.append(rate)
                    address = self.find_address()
                    temp.append(address)
                    # traffic = self.csv_find_traffic(csv_data, idx)
                    # temp.append(traffic)
                    time_info = self.find_time()
                    temp.append(time_info)
                    menu_info = self.find_menu()
                    temp.append(menu_info)
                    
                    writer.writerow(temp)
                    
                    # with open(self.output_path, mode='a', newline='') as file:
                    #     writer = writer(file)
                    #     writer.writerow(temp)
                    
                except:
                    print("query가 없습니다.")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    sleep(0.1)
                    pass
                else:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                finally:
                    if idx>3:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    @staticmethod
    def correct_name(name, location):
        if "점" not in name:
            keyword = name
            query = keyword + " " + location
        else:
            query = name
        query = re.sub(r'\([^)]*\)', '', query)
        query = re.sub(r'\[[^)]*\]', '', query)
        query = re.sub(r'\<[^)]*\>', '', query)
        query = re.sub(r'\{[^)]*\}', '', query)
        print("==========================[" + query + "]==========================")
        return query
    
    def find_name(self):
        name = self.driver.find_element(by='xpath', value='//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/h2').text
        print(f"가게이름: {name}")
        return name
    
    def find_category(self):
        category = self.driver.find_element(by='xpath', value='//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/span[1]').text
        print(f"가게이름: {category}")
        return category
    
    def find_rate(self):
        rate_num = self.driver.find_element(by='xpath', value='//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/a[1]/span[1]').text
        print("평점: " + rate_num)
        return rate_num

    def find_address(self):
        address = self.driver.find_element(by='xpath', value='//*[@id="mArticle"]/div[1]/div[2]/div[1]/div/span[1]').text
        print("주소: " + address)
        return address

    def csv_find_traffic(self, csv_data, idx):
        traffic = csv_data.iloc[idx][4]
        print("traffic: " + str(traffic))
        return traffic

    def find_time(self):
        time_info = []
        try:
            time_list = self.driver.find_element(by=By.CLASS_NAME, value='list_operation')
            period_time = time_list.find_elements(by=By.CLASS_NAME, value='txt_operation')
            detail_time = time_list.find_elements(by=By.CLASS_NAME, value='time_operation')
            sleep(0.1)
            if detail_time:
                for i in period_time:
                    time_info.append(i.text)
                    print(f"영업시간정보: {i.text}")
            else:
                print("영업시간정보: null")
                time_info.append("null")
        except:
            print("영업시간정보없음")
            time_info.append("null")
            pass
        finally:
            return time_info

    def find_menu(self):
        menus_dict = {}
        try:
            menu_list = self.driver.find_element(by=By.CLASS_NAME, value='list_menu')
            menus = menu_list.find_elements(by=By.CLASS_NAME, value='loss_word')
            menus_price = menu_list.find_elements(by=By.CLASS_NAME, value='price_menu')
            for a, b in zip(menus, menus_price):
                menus_dict[a.text] = b.text
            for j in menus_dict:
                print("메뉴: {}, 가격: {}".format(j, menus_dict[j]))
        except:
            print("메뉴없음")
            menus_dict["null"] = "null"
        finally:
            return menus_dict
        
if __name__ == '__main__':
    common_path = "C:/Users/Young/Desktop/Young/10.sideproject/odego/scrapping/pythonScraping/"
    csv_path = common_path+"Small_Business_Administration_csv_folder/busan_202209.csv"
    output_path = "output_2023_05_27.csv"
    driver_path = common_path + "chrome_driver/chromedriver.exe"

    scrapper = RestaurantScraper(csv_path=csv_path
                                 , output_path = output_path
                                 , driver_path=driver_path)
    scrapper.run()