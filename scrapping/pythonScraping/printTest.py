import pandas as pd

import os
from time import sleep

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from csv import writer

busan_restaurant = pd.read_csv("restaurant_csv_folder/busan_restaurant.csv")
print(busan_restaurant)
busan_restaurant = pd.read_csv("restaurant_csv_folder/output_restaurant_from_kakao.csv")
print(busan_restaurant)