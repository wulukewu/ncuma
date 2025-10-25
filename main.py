from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
from bs4 import BeautifulSoup
import requests
import datetime
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import os
import json

# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

# Variables - GitHub
line_notify_id = os.environ['LINE_NOTIFY_ID']
discord_webhook_url = os.environ['DISCORD_WEBHOOK_URL']
sheet_key = os.environ['GOOGLE_SHEETS_KEY']
gs_credentials = os.environ['GS_CREDENTIALS']
service = Service(ChromeDriverManager().install())


# Variables - Google Colab
# line_notify_id = LINE_NOTIFY_ID
# sheet_key = GOOGLE_SHEETS_KEY
# gs_credentials = GS_CREDENTIALS
# service = Service(binary_path)

# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

# LINE Notify ID
LINE_Notify_IDs = list(line_notify_id.split())

# 定義查找nid代碼函數
def find_nid(title, text):
    title_line_numbers = []
    for i, line in enumerate(text.split('\n')):
        if title in line:
            title_line_numbers.append(i)

    if not title_line_numbers:
        print(f'Cannot find "{title}" in the text.')
        return None

    title_line_number = title_line_numbers[0]
    title_line = text.split('\n')[title_line_number]

    nid_start_index = title_line.index('nid="') + 5
    nid_end_index = title_line.index('"', nid_start_index)
    nid = title_line[nid_start_index:nid_end_index]

    return nid

# 取得網頁內容
def get_content(url):
  # 發送GET請求獲取網頁內容
  response = requests.get(url)

  # 解析HTML內容
  soup = BeautifulSoup(response.content, 'html.parser')

  # 找到所有的 <p> 標籤
  p_tags = soup.find_all('p')

  # 整理文字內容
  text_list = []
  for p in p_tags:
      text = p.text.strip()
      text_list.append(text)
  text = '\n'.join(text_list)
  # text = ' '.join(text.split())  # 利用 split() 和 join() 將多個空白轉成單一空白
  # text = text.replace(' ', '\n')  # 將空白轉換成換行符號
  # text = text.replace(' ', '')  # 刪除空白
  return text

# text_limit = 1000-20

# Process message
def Process_Message(category, date, title, link, content):

  send_info_1 = f'【{category}】{title}\n⦾發佈日期：{date}'
  send_info_2 = f'⦾內容：' if content != '' else ''
  send_info_3 = f'⦾更多資訊：{link}'

  text_len = len(send_info_1) + len(send_info_2) + len(send_info_3)
  if content != '':
    # if text_len + len(content) > text_limit:
    #   content = f'{content[:(text_limit - text_len)]}⋯'
    params_message = f'{send_info_1}\n{send_info_2}{content}\n{send_info_3}'
  else:
    params_message = f'{send_info_1}\n{send_info_3}'
  
  return params_message

# LINE Notify
def LINE_Notify(message, LINE_Notify_ID):

  headers = {
          'Authorization': 'Bearer ' + LINE_Notify_ID,
          'Content-Type': 'application/x-www-form-urlencoded'
      }
  params = {'message': message}

  r = requests.post('https://notify-api.line.me/api/notify',
                          headers=headers, params=params)
  print(r.status_code)  #200

# Discord 發送
def dc_send(message, webhook_url):
    payload = {
        "content": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        print(f"Message sent successfully! Status Code: {response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

# Google Sheets 紀錄
scope = ['https://www.googleapis.com/auth/spreadsheets']
info = json.loads(gs_credentials)

creds = Credentials.from_service_account_info(info, scopes=scope)
gs = gspread.authorize(creds)

def google_sheets_refresh():

  global sheet, worksheet, rows_sheets, df

  # 使用表格的key打開表格
  sheet = gs.open_by_key(sheet_key)
  worksheet = sheet.get_worksheet(0)

  # 讀取所有行
  rows_sheets = worksheet.get_all_values()
  # print(len(rows_sheets))
  # 使用pandas創建數據框
  df = pd.DataFrame(rows_sheets)

def main(url, category, card):

    # chromedriver 設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # 等待網頁載入完成
    driver.implicitly_wait(10)

    # 打印整個頁面的 HTML 代碼
    page_source = driver.page_source
    # print(page_source)

    # 抓取公告表格
    top_announcement = driver.find_element(By.ID, card)
    top_announcement_html = top_announcement.get_attribute('outerHTML')

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(top_announcement_html, 'html.parser')

    # 抓取所有公告的標題、日期和連結
    announcements = soup.find_all('li')
    # print(announcements)

    arr_title = []
    arr_date = []
    arr_link = []
    for announcement in announcements:
        a_tag = announcement.find('a')
        if a_tag:  # 確保a標籤存在
            title = a_tag.text.strip()
            relative_link = a_tag['href']
            link = url + relative_link if relative_link.startswith('/') else relative_link
            date_tag = announcement.find('small')
            if date_tag: date = date_tag.text.strip()
            else: continue

            # print("標題:", title)
            # print("日期:", date)
            # print("連結:", link)
            # print("---")

            arr_title.append(title)
            arr_date.append(date)
            arr_link.append(link)

    # print(arr_title, arr_date, arr_link)

    # 定義需要查找的最新幾筆資料
    numbers_of_new_data = 9
    numbers_of_new_data = min(numbers_of_new_data, len(arr_link))

    # 印出最新幾筆資料的標題、單位和連結
    for i in range(numbers_of_new_data - 1, -1, -1):

        title = arr_title[i]
        date = arr_date[i]
        link = arr_link[i]

        # link_publish = f"{url[:url.find('ischool')]}ischool/public/news_view/show.php?nid={nid}"
        # link = f"{url[:url.find('ischool')]}ischool/public/news_view/show.php?nid={nid}"

        # 打開公告詳細頁面
        driver.get(link)
        driver.implicitly_wait(10)

        # 抓取詳細頁面的 HTML 並打印
        detailed_page_html = driver.page_source
        # print("詳細頁面HTML:")
        # print(detailed_page_html)
        # print("---")

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(detailed_page_html, 'html.parser')

        # 抓取內容摘要
        content_element = soup.find('div', class_='content')
        content_paragraphs = content_element.find_all('p') if content_element else []
        content = '\n'.join([p.text.strip() for p in content_paragraphs])
        # print(f'內容摘要:\n{content}')

        print(f'title:{title}\tcategory:{category}\tdate:{date}\tlink:{link}\tcontent:{content}')

        # 獲取當前日期
        today = datetime.date.today()

        # 將日期格式化為2023/02/11的形式
        formatted_date = today.strftime("%Y/%m/%d")

        # 檢查nid是否已經存在於表格中
        sent = not(link in links)
        # print(sent, link, links)

        if sent:

          # 檢查標題是否已經存在於表格中
          titles = df[2].tolist()
          if title in titles:
            continue

          # 獲取新行
          now = datetime.datetime.now() + datetime.timedelta(hours=8)
          new_row = [now.strftime("%Y-%m-%d %H:%M:%S"), category, date, title, link, content]

          # 將新行添加到工作表中
          worksheet.append_row(new_row)

          # 獲取新行的索引
          new_row_index = len(rows_sheets) + 1
          rows_sheets.append([])
          # print(new_row_index)

          # 更新單元格
          cell_list = worksheet.range('A{}:F{}'.format(new_row_index, new_row_index))
          for cell, value in zip(cell_list, new_row):
              cell.value = value
          worksheet.update_cells(cell_list)

          # 更新links列表
          links.append(link)

          # 處理訊息
          params_message = Process_Message(category, date, title, link, content)
          
          # 傳送至LINE Notify
          print(f'Sent: {link}', end=' ')
          # for LINE_Notify_ID in LINE_Notify_IDs:
          #     LINE_Notify(params_message, LINE_Notify_ID)

          # 傳送至Discord
          dc_send(params_message, discord_webhook_url)

        # 刪除nid
        del link

    # 關閉網頁
    driver.quit()

# 開啟網頁
urls = [
    'https://w2.math.ncu.edu.tw/@@置頂公告@top-card@@最新消息@news-card@@學術活動@speeches-card',
]

if __name__ == "__main__":

  # 刷新Google Sheets表格
  google_sheets_refresh_retry_limit = 3
  google_sheets_refresh_not_done = True
  for _ in range(google_sheets_refresh_retry_limit):
    try:
      google_sheets_refresh()
      google_sheets_refresh_not_done = False
      break
    except Exception as e:
      print(f'google_sheets_refresh error: {e}\nretrying...')
  if google_sheets_refresh_not_done:
    print('google_sheets_refresh failed.')
    os._exit(0)

  # 取得Google Sheets nids列表
  _links = df[4].tolist()
  links = []
  for l in _links:
    try:
      links.append(l)
    except:
      continue


  error_links = []
  for temp in urls:
    temp = list(temp.split('@@'))
    url = temp[0]
    temp = temp[1:]

    cards = {}
    for temptemp in temp:
      ttemp = list(temptemp.split('@'))
      cards[ttemp[0]] = ttemp[1]
    # print(cards)

    for category in cards:
      card = cards[category]

      finished = False
      try_times_limit = 2
      for _ in range(try_times_limit):
        try:
          main(url, category, card)
          finished = True
          break
        except:
          print('retrying...')
          next

      if not finished:
        error_links.append([url, category, card])
        print(f'error : {url}')

  if len(error_links) == 0:
    print(f"{'-'*50}\nAll Finished Successfully. ")
  else:
    print(f"{'-'*50}\nAll Finished, Here Are All The Links That Cannot Be Sent Successfully. ({len(error_links)} files)")
    for error_link in error_links:
      print(error_link)
