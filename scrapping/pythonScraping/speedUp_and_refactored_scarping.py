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
import multiprocessing

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class RestaurantScraper:
    def __init__(self, csv_path, output_path, driver_path, si_gun_gu):
        self.csv_path = csv_path
        self.output_path = output_path
        self.driver_path = driver_path
        self.driver = None
        self.si_gun_gu = si_gun_gu
    
    def run(self):
        csv_data = pd.read_csv(self.csv_path)
        # store_names = csv_data['업소명']
        store_names = csv_data['상호명']
        category_name_from_CSV = csv_data['상권업종대분류명']
        si_gun_gu_name_from_CSV = csv_data['시군구명']
        
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(executable_path = self.driver_path, options=options)
        
        # with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        with open(f'{si_gun_gu}.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # writer.writerow(['Name', 'Category', 'Rate', 'Address', 'Time', 'Menu', 'facility'])
            writer.writerow(['상호명', '카테고리', '평점', '주소', '운영시간', '메뉴', '시설'])
        
            for idx, store_name in enumerate(store_names):
                if si_gun_gu_name_from_CSV.iloc[idx] != si_gun_gu:
                    continue
                if category_name_from_CSV.iloc[idx] !='음식':
                    continue
                
                # query = self.correct_name(store_name, "부산")
                query = store_name
                if type(csv_data['지점명'].iloc[idx]) == str:
                    query += (" " + csv_data['지점명'].iloc[idx])
                
                print(query)
                temp = []
                
                
                try:
                    kakao_map_search_url = f"https://map.kakao.com/?q={query}"
                    self.driver.get(kakao_map_search_url)
                    self.driver.implicitly_wait(time_to_wait=10)
                    
                    new_link = self.driver.find_element(by='xpath', value='//*[@id="info.search.place.list"]/li[1]/div[5]/div[4]/a[1]')
                    si_gun_gu_from_internet = self.driver.find_element(by='xpath', value='//*[@id="info.search.place.list"]/li[1]/div[5]/div[2]/p[1]')
                    new_link.send_keys(Keys.ENTER)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    # self.driver.implicitly_wait(time_to_wait=3)
                    wait = WebDriverWait(driver=self.driver
                                          ,timeout=10)
                    element = wait.until(EC.presence_of_element_located((By.ID, 'kakaoFoot')))
                    
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
                    facility_info = self.find_facility()
                    temp.append(facility_info)
                    
                    writer.writerow(temp)
                    
                    # with open(self.output_path, mode='a', newline='') as file:
                    #     writer = writer(file)
                    #     writer.writerow(temp)
                    if idx > 3:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                    
                except:
                    print("query가 없습니다.")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    sleep(0.1)
                    pass

                # else:
                #     if idx>1:
                #         self.driver.close()
                #         self.driver.switch_to.window(self.driver.window_handles[-1])
                # finally:

    
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
        except NoSuchElementException as e:
            print("영업시간정보없음")
            time_info.append("null")
            pass
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
        except NoSuchElementException as e:
            print(e + " : ", end='')
            print("메뉴없음")
        except:
            print("메뉴없음")
            menus_dict["null"] = "null"
        finally:
            return menus_dict
        
    def find_facility(self):
        facility_dict = {}
        try:
            facility_list = self.driver.find_element(by=By.CLASS_NAME, value='list_facility')
            facility_list = facility_list.find_elements(by=By.TAG_NAME, value='li')
            for facility in facility_list:
                facility_name = facility.find_element(by=By.CLASS_NAME, value='color_g').text
                facility_status = "가능"
                
                try:
                    facility_status = facility.find_element(by=By.CLASS_NAME, value='screen_out').text
                except NoSuchElementException as e:
                    pass
                except:
                    pass
                
                facility_dict[facility_name] = facility_status
                print("시설: {}, 상태: {}".format(facility_name, facility_dict[facility_name]))
        except NoSuchElementException as e:
            print(e + " : ", end='')
            print("시설정보없음")
            facility_dict["null"] = "null"               
        except:
            print("시설정보없음")
            facility_dict["null"] = "null"
        finally:
            return facility_dict
        
if __name__ == '__main__':
    common_path = "C:/Users/Young/Desktop/Young/10.sideproject/odego/scrapping/pythonScraping/"
    csv_path = common_path+"Small_Business_Administration_csv_folder/busan_202209_01.csv"
    output_path = "output_2023_05_27.csv"
    driver_path = common_path + "chrome_driver/chromedriver.exe"
    
    si_gun_gu = input()

    scrapper = RestaurantScraper(csv_path=csv_path
                                 , output_path = output_path
                                 , driver_path=driver_path
                                 , si_gun_gu = si_gun_gu)
    scrapper.run()
    cpu_count = multiprocessing.cpu_count()
    print(cpu_count)