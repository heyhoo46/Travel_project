import csv
from datetime import date, timedelta
from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

index = "제주시"

# 날짜 계산 (내일부터 10일간의 날짜)
today = date.today() + timedelta(days=1)  # 내일부터 시작
today1 = today.strftime('%m%d')

# CSV 파일 열기 (덮어쓰기 모드)
with open('weather_data_with_images.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['현재 기온(C)', '이미지 URL', '오늘 기온', '오늘 날씨', '날짜', '최고 기온(C)', '최저 기온(C)', '이미지 URL 날짜별']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 헤더 작성
    writer.writeheader()

    # 크롬 브라우저 실행
    driver = wb.Chrome()
    url = "https://www.kr-weathernews.com/mv4/html/today.html?loc=1100000000"
    driver.get(url)

    # '검색' 버튼 클릭
    button = driver.find_element(By.ID, "searchDiv")
    button.click()
    time.sleep(1)

    # 지역 입력란에 "제주시" 입력
    search = driver.find_element(By.ID, "searchFormInput")
    search.send_keys(index)
    search.send_keys(Keys.ENTER)
    time.sleep(1)

    # 검색된 장소 클릭
    okay = driver.find_element(By.CLASS_NAME, "searchedPlaceData")
    okay.click()
    time.sleep(1)

    # tw = TodayWeather #오늘 날씨 정보
    tw_list = driver.find_element(By.CSS_SELECTOR, ".cur-title-wrap .flex-between .temp")  
    today_temp = tw_list.text  # 현재 기온
    time.sleep(0.5)

    # 이미지 URL 추출
    image_element = driver.find_element(By.CSS_SELECTOR, ".cur-title-wrap .flex-between .weather-img .lazy")
    image_url = image_element.get_attribute("src") if image_element else "No Image Found"
    time.sleep(0.5)

    # 오늘 기온(최고, 최저)
    tw_tempp = driver.find_elements(By.CSS_SELECTOR, ".weather-text")
    for i in range(len(tw_tempp)):
        tw_temp = tw_tempp[i].text
        # print(tw_temp)
    time.sleep(0.5)

    okay2 = driver.find_element(By.CLASS_NAME, "tablet-weekly-nav")
    okay2.click()
    time.sleep(1)

    # 오늘 날씨 텍스트 출력
    tw_ment = driver.find_elements(By.CSS_SELECTOR, "p.weather-txt")
    today_ment = tw_ment[1].text if tw_ment else "정보 없음"

    writer.writerow({
        '현재 기온(C)': today_temp,
        '오늘 날씨': today_ment,
        '이미지 URL': image_url,
        '오늘 기온': tw_temp
    })

    

    # 날짜별로 10일 기온 정보 출력
    for i in range(10):
        future_day = today + timedelta(days=i)  # 내일부터 i일 후의 날짜 계산
        date_str = future_day.strftime('%m%d')  # 날짜를 MMDD 형식으로 변환
        date1 = future_day.strftime('%m')
        date2 = future_day.strftime('%d') 
        
        # 각 날짜에 해당하는 요소를 찾기
        try:
            next_day = driver.find_element(By.ID, date_str)  # 해당 날짜로 찾아가서
            elements_max = next_day.find_elements(By.CSS_SELECTOR, ".maxt")
            elements_min = next_day.find_elements(By.CSS_SELECTOR, ".mint")

            max_temp = elements_max[0].text if len(elements_max) > 0 else "N/A"
            min_temp = elements_min[0].text if len(elements_min) > 0 else "N/A"
            time.sleep(0.5)

            weatherimg = next_day.find_element(By.CSS_SELECTOR, ".detail-close-icon.weekly-wx-img .lazy")
            weatherimg_url = weatherimg.get_attribute("src") if weatherimg else "No Image Found"

            # CSV에 날짜별 데이터 기록
            writer.writerow({
                '날짜': f"{date1}월{date2}일",
                '최고 기온(C)': max_temp,
                '최저 기온(C)': min_temp,
                '이미지 URL 날짜별': weatherimg_url
            })
        except Exception as e:
            print(f"날짜 {date1}월{date2}일에 대한 정보 가져오기에 실패했습니다: {e}")

    time.sleep(1)

    # 브라우저 종료
    driver.close()

print("CSV 파일로 저장 완료!")
