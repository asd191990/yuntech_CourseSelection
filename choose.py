from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

options = Options()
options.add_argument("--disable-notifications")

Acc = "xx" #帳號
P = "xx" #密碼
classid_array = ["0245"] #選課陣列



def login():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(
        r"https://webapp.yuntech.edu.tw/YunTechSSO/Account/Login?ReturnUrl=%2fYunTechSSO")
    driver.implicitly_wait(20)

    driver.find_element(By.ID, "pLoginName").send_keys(Acc)
    driver.find_element(By.ID, "pLoginPassword").send_keys(P)
    driver.find_element(By.ID, "LoginSubmitBtn").click()
    return driver

driver=login()

def use_check(useid):
    try:
        driver.get(r"https://webapp.yuntech.edu.tw/AAXCCS/CourseSelectionRegister.aspx")
        driver.implicitly_wait(10)
        driver.find_element(By.ID, "ContentPlaceHolder1_CurrentSubjTextBox").send_keys(useid)
        driver.find_element(By.ID, "ContentPlaceHolder1_CurrentSubjRegisterButton").click()
        time.sleep(1)
        driver.find_element(By.ID, "ContentPlaceHolder1_NextStepButton").click()
        driver.implicitly_wait(10)
        driver.find_element(By.ID, "ContentPlaceHolder1_SaveButton").click()
        driver.implicitly_wait(10)
        driver.get(
                r"https://webapp.yuntech.edu.tw/WebNewCAS/Course/QueryCour.aspx")
        return "end"
    except:

        pass
    finally:
        
        return "end"
    
def find_class():

    for findid in classid_array:
        driver.get(
            r"https://webapp.yuntech.edu.tw/WebNewCAS/Course/QueryCour.aspx")
        driver.implicitly_wait(10)
        driver.find_element(
            By.ID, "ctl00_MainContent_CurrentSubj").send_keys(findid)
        driver.find_element(By.ID, "ctl00_MainContent_Submit").click()
        driver.implicitly_wait(20)

        num = driver.find_element(
            By.XPATH, '//*[@id="ctl00_MainContent_Course_GridView"]/tbody/tr[2]/td[10]').text
        maxnum = driver.find_element(
            By.XPATH, '//*[@id="ctl00_MainContent_Course_GridView"]/tbody/tr[2]/td[11]').text.replace("限","").replace("人","")
        num = int(num)
        maxnum = int(maxnum)
        print(f"課程代碼:{findid} 修課人數:{num} 人數限制{maxnum}")
        if maxnum > num:
            print("可以選課!!")
            use_check(findid)
            classid_array.remove(findid)
            return
        else:
            print("人數已滿無法選課")

while(len(classid_array)):
    try:
        print(f"時間為 {datetime.now().strftime('%H:%M:%S')}")
        find_class()
        time.sleep(5)
    except:
        pass
    finally:
        pass

print("感謝使用")
input("bye!")