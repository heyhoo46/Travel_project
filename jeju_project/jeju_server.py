from flask import Flask, render_template, request, redirect
from datetime import date, timedelta
from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

def get_weather():
    index = "제주시"

    # 날짜 계산 (내일부터 10일간의 날짜)
    today = date.today() + timedelta(days=1)  # 내일부터 시작
    today1 = today.strftime('%m%d')

    # 크롬 브라우저 실행
    driver = wb.Chrome()
    url = "https://www.kr-weathernews.com/mv4/html/weekly.html?loc=1100000000"
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
    okay2 = driver.find_element(By.CLASS_NAME, "tablet-weekly-nav")
    okay2.click()

    # 오늘 날씨 정보
    tw_list = driver.find_element(By.CSS_SELECTOR, ".weekly-middle-left .mint")
    today_temp = tw_list.text

    tw_ment = driver.find_elements(By.CSS_SELECTOR, "p.weather-txt")
    today_weather = tw_ment[1].text if len(tw_ment) > 1 else "정보 없음"

    # 10일간의 날씨 정보
    weather_data = []
    for i in range(10):
        future_day = today + timedelta(days=i)
        date_str = future_day.strftime('%m%d')
        date1 = future_day.strftime('%m')
        date2 = future_day.strftime('%d')

        next_day = driver.find_element(By.ID, date_str)
        elements_max = next_day.find_elements(By.CSS_SELECTOR, ".maxt")
        elements_min = next_day.find_elements(By.CSS_SELECTOR, ".mint")

        max_temp = elements_max[0].text if len(elements_max) > 0 else "N/A"
        min_temp = elements_min[0].text if len(elements_min) > 0 else "N/A"

        weather_data.append({
            "date": f"{date1}월 {date2}일",
            "max_temp": max_temp,
            "min_temp": min_temp
        })

    # 브라우저 종료
    driver.close()

    return {
        "today_temp": today_temp,
        "today_weather": today_weather,
        "weather_data": weather_data
    }

@app.route('/')
def index():
    return render_template('jeju.html')

@app.route('/market')
def market():
    weather_info = get_weather()  # 날씨 정보 가져오기
    return render_template('market.html',**weather_info)

@app.route('/orem')
def orem():
    weather_info = get_weather()  # 날씨 정보 가져오기
    return render_template('orem.html',**weather_info)

@app.route('/dullegil')
def dullegil():
    weather_info = get_weather()  # 날씨 정보 가져오기
    return render_template('dullegil.html',**weather_info)

@app.route('/museum')
def museum():
    weather_info = get_weather()  # 날씨 정보 가져오기
    return render_template('museum.html',**weather_info)

@app.route('/entertain')
def entertain():
    weather_info = get_weather()  # 날씨 정보 가져오기
    return render_template('entertain.html',**weather_info)

@app.route('/mountain')
def mountain():
    weather_info = get_weather()  # 날씨 정보 가져오기
    return render_template('mountain.html', **weather_info)

@app.route('/beach')
def beach():
    weather_info = get_weather()  # 날씨 정보 가져오기
    return render_template('beach.html',**weather_info)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
