from datetime import date, timedelta
from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

index = "제주시"

# 날짜 계산 (내일부터 10일간의 날짜)
today = date.today() + timedelta(days=1)  # 내일부터 시작
today1 = today.strftime('%m%d')

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
tw_list = driver.find_element(By.CSS_SELECTOR, ".flex-between .temp")  
print(f"현재 기온은 {tw_list.text}C 입니다")
time.sleep(0.5)

okay2 = driver.find_element(By.CLASS_NAME, "tablet-weekly-nav")
okay2.click()
time.sleep(1)

# 모든 요소의 텍스트 출력 # 두번째 요소에서만 텍스트를 출력하도록 함.
tw_ment = driver.find_elements(By.CSS_SELECTOR, "p.weather-txt")

if tw_ment:
    print(f"오늘, {tw_ment[1].text}")  # 두 번째 요소의 텍스트만 출력
else:
    print("요소를 찾을 수 없습니다.")

# 날짜별로 10일 기온 정보 출력
for i in range(10):
    future_day = today + timedelta(days=i)  # 내일부터 i일 후의 날짜 계산
    date_str = future_day.strftime('%m%d')  # 날짜를 MMDD 형식으로 변환
    date1 = future_day.strftime('%m')
    date2 = future_day.strftime('%d') 
    
    # 각 날짜에 해당하는 요소를 찾기
    next_day = driver.find_element(By.ID, date_str)  # 해당 날짜로 찾아가서
    elements_max = next_day.find_elements(By.CSS_SELECTOR, ".maxt")
    elements_min = next_day.find_elements(By.CSS_SELECTOR, ".mint")

    max_temp = elements_max[0].text if len(elements_max) > 0 else "N/A"
    min_temp = elements_min[0].text if len(elements_min) > 0 else "N/A"

    print(f"{date1}월{date2}일 - 최고 기온: {max_temp}C, 최저 기온: {min_temp}C")

time.sleep(1)

# 브라우저 종료
driver.close()
