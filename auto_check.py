import os, sys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, time

from pywinauto import findwindows, win32_element_info
from pywinauto import application
import time as t
from messenger_sender import sendToMe

username = ""
password = ""
url = ''
name = ''



def readData() :
    global username, password, name, url
    with open("./data.txt", mode="r", encoding="utf-8") as f :
        lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]

        username = lines[0]
        password = lines[1]
        name = lines[2]
        url = lines[3]


def setUp() :
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def openAndLogin(driver) :    
    driver.get(url)

    # print(data)
    #  = driver.find_element(By.CSS_SELECTOR, "#root")
    id_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > main > div > div:nth-child(1) > form > fieldset > div.mb-5 > div > input")))
    id_input.send_keys(username)

    driver.find_element(By.CSS_SELECTOR, "#root > div > main > div > div:nth-child(1) > form > fieldset > button").click()

    password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > main > div > div:nth-child(1) > form > fieldset > div.mantine-InputWrapper-root.mantine-TextInput-root.mb-5.mantine-vb1jt1 > div > input")))
    password_input.send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "#root > div > main > div > div:nth-child(1) > form > fieldset > button").click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > div.header-wrapper > div > div > div > div:nth-child(6) > a"))).click()

def goWork() : 
    try :
        print(datetime.now())
        driver = setUp()
        openAndLogin(driver)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > div > section.info-day > div > div.info-day-check > div.box.flex-column.justify-content-between > ul > li:nth-child(1) > button"))).click()
        sendToMe(username, "출근 찍기 Success")
    except Exception as e :        
        sendToMe(username, "출근 찍기 Fail")
        
        print(e)

def leaveWork() :
    try :
        print(datetime.now())
        driver = setUp()
        openAndLogin(driver)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > div > section.info-day > div > div.info-day-check > div.box.flex-column.justify-content-between > ul > li:nth-child(2) > button"))).click()

        WebDriverWait(driver, 20).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        
        sendToMe("퇴근 찍기 Success")
    except Exception as e :
        sendToMe("퇴근 찍기 Fail")
        print(e)

if __name__ == "__main__" :
    readData()
    
    scheduler = BlockingScheduler()

    scheduler.add_job(
        goWork,
        'cron',
        day_of_week='mon-fri',
        hour=8,
        minute=55,
        second=0
    )

    scheduler.add_job(
        leaveWork,
        'cron',
        day_of_week='mon-thu',
        hour=18,
        minute=1,
        second=0
    )

    # 금요일 오전 8시에 실행되는 cron 스케줄 추가
    scheduler.add_job(
        leaveWork,
        'cron',
        day_of_week='fri',
        hour=17,
        minute=1,
        second=0
    )

    # 현재 시간 확인
    
    current_time = datetime.now().time()
    # 만약 현재 시간이 9시 이후라면 바로 실행
    if current_time >= time(9, 0, 0) and current_time <= time(10, 0, 0) :
        goWork()
    
    #스케줄러 실행
    try:
        scheduler.start()
        
    except (KeyboardInterrupt, SystemExit):
        pass
    
        
