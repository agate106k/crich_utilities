import json
import os
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from selenium.webdriver.support.select import Select

import time

import sqlite3

#Webドライバ初期化（2行目コメントアウトしたらブラウザウィンドウ開くのでテスト用に）
option = Options()
option.add_argument('--headless')
chrome_service = service.Service(executable_path='D:\Documents\AkiKyo\chromedriver.exe')
driver = webdriver.Chrome(options=option)

conn = sqlite3.connect("syllabus.db")
cur = conn.cursor()

USER = os.getenv('USER')
PASS = os.getenv('PASSWORD')

CURRENT_YEAR = "2022"
CAMPUS = "日吉"

WEEKDAY = {
    "月": 1,
    "火": 2,
    "水": 3,
    "木": 4,
    "金": 5,
    "土": 6,
    "日": 7
}

COLUMN_DEF = {
    "登録番号": "id",
    "サブタイトル": "subtitle",
    "学期": "term",
    "キャンパス": "campus",
    "教室": "room",
    "設置": "dept",
    "学年": "grade",
    "授業言語": "lang",
    "分野": "field",
    "クラス": "class"
}

#シラバス検索ページを開く
driver.get("https://gslbs.keio.jp/syllabus/login")
time.sleep(10)

login_id = driver.find_element(by=By.ID, value="username")
login_id.send_keys(USER)

login_pass = driver.find_element(by=By.ID, value="password")
login_pass.send_keys(PASS)

login_btn = driver.find_element(by=By.NAME, value="_eventId_proceed")
login_btn.click()

time.sleep(4)

#検索条件設定して実行
search_year = driver.find_element(by=By.NAME, value="KEYWORD_TTBLYR")
select = Select(search_year)
select.select_by_value(CURRENT_YEAR)

search_term = driver.find_element(by=By.ID, value="KEYWORD_SMSCD_screen_3")
search_term.click()

search_campus = driver.find_element(by=By.NAME, value="KEYWORD_CAMPUS")
select = Select(search_campus)
select.select_by_visible_text(CAMPUS)

search_dept = driver.find_element(by=By.NAME, value="KEYWORD_PRGANDFCD")
select = Select(search_dept)
select.select_by_visible_text("すべて")

for i in range(1, 7):
    name = "KEYWORD_LVL_screen_" + str(i)
    search_grade = driver.find_element(by=By.ID, value=name)
    if search_grade.is_selected():
        driver.execute_script("arguments[0].click();", search_grade)

search_btn = driver.find_element(by=By.XPATH, value="//*[@id=\"keyword_search_form\"]/div[10]/button")
driver.execute_script("arguments[0].click();", search_btn)

time.sleep(10)

#時限と教室取得
roomList = []

for i in range(1, 8):
    currDay = WEEKDAY[i] #曜日の漢字
    currHour = 1
    
    tab = driver.find_element(by=By.XPATH, value="//*[@id=\"mainResultTab\"]/li["+ str(i) +"]/a")
    driver.execute_script("arguments[0].click();", tab)

    time.sleep(10)

    results = driver.find_elements(by=By.XPATH, value="//*[@class='search-result-item']")
    for sub in results:
        sub_name = sub.find_element(by=By.CLASS_NAME, value="sbjtnm").text
        prof_name = sub.find_element(by=By.CLASS_NAME, value="lctnm").text

        details = tuple(sub.find_elements(by=By.CLASS_NAME, value="detail-outer"))

        #comaDef = {}
        room = None
        subj_class = None
        coma = []
        for item in details:
            column_name = item.find_element(by=By.CLASS_NAME, value="detail-heading").get_attribute("textContent")
            value = item.find_element(by=By.CLASS_NAME, value="detail-contents").get_attribute("textContent")            
            if column_name == "曜日時限":
                days = value.split("/")
                for i in days:
                    if len(i) > 2:
                        hours = i[1:].split(",")
                        for j in hours:
                            coma.append(i[0] + j)
                    else:
                        coma.append(i)
            elif column_name == "教室" and value is not None:
                if all(item in value for item in [':', ',']):
                    dict((a.strip(), b.strip()) for a, b in (element.split(':')  for element in original_String.split(', ')))
            elif column_name == "登録番号":
                subj_id = value
            elif column_name == "サブタイトル":
                subtitle = value.replace("'", "''") 
            elif column_name == "学期":
                if "春" in value:
                    term = 1
                elif value == "秋":
                    term = 2
                else:
                    term = 3
                    print(value)
            elif column_name == "キャンパス":
                campus = value
            elif column_name == "設置":
                dept = value
            elif column_name == "学年":
                grade = value
            elif column_name == "授業言語":
                lang = value
            elif column_name == "分野":
                field = value
            elif column_name == "クラス":
                subj_class = value
        if coma == []:
            continue

        cur.execute(f"INSERT OR IGNORE INTO items VALUES({subj_id}, {term}, {WEEKDAY[coma[0][0]]}, {coma[0][1]}, \'{campus}\', \'{room}\',  \'{dept}\', \'{grade}\', \'TEST\', \'TEST\', \'{lang}\', \'{field}\', \'{subtitle}\', \'{subj_class}\')")
        conn.commit()

driver.quit()
conn.close()
