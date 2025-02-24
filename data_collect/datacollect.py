from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests # 이미지 저장하기 위해 요청 라이브러리 필요
import os # 폴더 생성
import pandas as pd # csv파일 만들기 위함 


def collect_place(search, page_number):
    """지역과 검색어를 띄어쓰기 하여 스트링으로 입력하세요. 
    크롤링 하고 싶은 페이지의 개수를 정수로 입력하세요. ex) "제주도 박물관", 5
    6개의 리스트 반환합니다."""
    city = search.split()[0]
    category = search.split()[1]
    google_url = f"https://www.google.com/search?q={city}+{category}&sca_esv=7833c6f0638101e1&biw=1278&bih=1304&tbm=lcl&sxsrf=AHTn8zrhLfW17tjrdqE826Y4NIVAvSNyaw%3A1740021107822&ei=c522Z6_vMZXM1e8P9vmF-A0&ved=0ahUKEwjv9KHgo9GLAxUVZvUHHfZ8Ad8Q4dUDCAo&uact=5&oq=%EC%A0%9C%EC%A3%BC%EB%8F%84+%EB%B0%95%EB%AC%BC%EA%B4%80&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhPsoJzso7zrj4Qg67CV66y86rSAMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIEEAAYHjIEEAAYHjIEEAAYHjIKEAAYgAQYFBiHAjIKEAAYgAQYQxiKBTIGEAAYBRgeSP8SUPgIWP8RcAF4AJABAZgBfqABogqqAQMzLjm4AQPIAQD4AQGYAgagArcEwgIEECMYJ8ICDRAAGIAEGLEDGBQYhwLCAgsQABiABBixAxiDAZgDAIgGAZIHAzEuNaAHmUQ&sclient=gws-wiz-local"
    driver = wb.Chrome()
    driver.get(google_url)
    time.sleep(4)

    # search 폴더 만들고 (만약, 있다면 안 만듦)
    if not os.path.isdir(search):
        os.mkdir(search)
    else:
        print(f"{search}폴더가 존재합니다")
    
    # 데이터 저장할 list
    place_list = [] # 장소이름
    score_list = [] # 별점(박물관은 별점 몇점이상인지에 관계없음)
    address_list = [] # 주소
    bushour_list = [] # 영업시간
    summary_list = [] # 개요

    for i in range(page_number):
        # 장소이름
        place = driver.find_elements(By.CSS_SELECTOR, ".rllt__details .dbg0pd .OSrXXb")
    
        # 별점
        score = driver.find_elements(By.CSS_SELECTOR, ".rllt__details .dbg0pd+div")# span .Y0A0hc .yi40Hd.YrbPuc") 

        # 스폰서 인지 아닌지
        sponsor2 = driver.find_elements(By.CSS_SELECTOR, ".pXf2tf.U3A9Ac.qV8iec")
        print("스폰서", len(sponsor2), "개 제외합니다.")
        sp = len(sponsor2)
        
        for pl in place[sp:]:                
            if category == "산":
                if "산" in pl.text:
                    print("산입니다.")
                    pl.click()
                    time.sleep(1)
                else:
                    print("산이 아닙니다.")
                    continue
            else:
                pl.click()
                time.sleep(1)
                
            # pl.click() # 클릭 후에 나머지 정보 추출
            # time.sleep(1)
    
            try:
                # 스폰서 인지 아닌지
                sponsor = driver.find_element(By.CSS_SELECTOR, ".G9DTJe .QGUp7b")
                print(sponsor.text)
                time.sleep(0.5)
                
            except:
                
                print("스폰서 아닙니다.")
                time.sleep(0.5)
                
                try:
                    # 폐업인지 아닌지
                    closedown = driver.find_element(By.CSS_SELECTOR, ".hBA2d,Shyhc")
                    print(closedown.text)
                    time.sleep(0.5)
                    
                except:
                    print("정상 영업합니다.")
                    time.sleep(0.5)
    
                    # 장소이름
                    print(pl.text)
                    place_list.append(pl.text)
                    time.sleep(0.5)
                    
                    # 별점
                    sc = score[place.index(pl)].text
                    # print(sc[:3])
                    if sc[:3] == "리뷰 ":
                        print("해당 장소에 대한 별점이 없습니다.")
                        score_list.append("")
                    else:
                        print(float(sc[:3]))
                        score_list.append(float(sc[:3])) #float(sc.split("(")[0]))
                        time.sleep(0.5)
                    
                    # 개요
                    # 개요 없으면 공백 채움
                    try:
                        summary = driver.find_element(By.CSS_SELECTOR, ".PZPZlf div .kno-rdesc")
                        print("개요:", summary.text)
                        summary_list.append(summary.text)
                    except:
                        print("해당 장소에 대한 설명이 없습니다.")
                        summary_list.append("")
                        pass  # 요소가 없으면 그냥 넘어감
                    time.sleep(0.5)
                    
                    # 주소
                    try: 
                        address = driver.find_element(By.CSS_SELECTOR, ".zloOqf .FoJoyf+.LrzXr")
                        print("주소:", address.text)
                        address_list.append(address.text)
                        time.sleep(0.5)   
                    except:
                        print("해당 장소에 대한 주소 없습니다.")
                        address_list.append(pl.text)
                        pass  # 요소가 없으면 그냥 넘어감
                    
                    # 영업시간
                    # 영업시간 없으면 공백 채움
                    try:
                        button = driver.find_element(By.CSS_SELECTOR, ".BTP3Ac")
                        button.click()
                        time.sleep(1)
                        bushour = driver.find_element(By.CSS_SELECTOR, ".a-h .b2JWxc")
                        print(bushour.text)
                        bushour_list.append(bushour.text)
                        time.sleep(0.5)
                        # bushour = driver.find_element(By.CSS_SELECTOR, ".TLou0b .JjSWRd")
                        # time.sleep(0.5)  
                        # print("영업시간:", bushour.text)
                        # bushour_list.append(bushour.text)
                    except:
                        print("해당 장소에 대한 영업시간 없습니다.")
                        bushour_list.append("")
                        pass  # 요소가 없으면 그냥 넘어감
                    time.sleep(0.5)
                        
                    
                    # 대표 이미지
                    try:
                        img = driver.find_element(By.CSS_SELECTOR, ".vwrQge")
                        img_text = img.get_attribute("style")
                        img_url = img_text.split("(")[1].split(")")[0]
                        response = requests.get(img_url[1:-1])
                        img_data = response.content
                        
                        img_path = f"{search}/{pl.text}.jpg"
                        with open(img_path, "wb") as file: # wb: write byte
                            file.write(img_data)
                            print(f"{pl.text}.jpg 저장 완료")
                        time.sleep(0.5)
                        print("------------------------")
                    except:
                        print("해당 장소에 대한 이미지가 없습니다.")
                        print("------------------------")
        
        try:
            nextpage = driver.find_element(By.CSS_SELECTOR, "#pnnext .oeN89d")
            nextpage.click()
            print("-----------------다음 페이지-----------------")
            time.sleep(3)
        except:
            print("-----------------다음 페이지 없음-----------------")
            break

    
    print(f"{search} 페이지 크롤링 완료")
    driver.close()
    
    print("장소이름", len(place_list))
    print("별점",len(score_list))
    print("주소",len(address_list))
    print("영업시간",len(bushour_list))
    print("개요",len(summary_list))

    category_list = [category] * len(place_list)

    return category_list, place_list, score_list, address_list, bushour_list, summary_list





def collect_restaurant(search, page_number, review_number, star_number):
    """지역과 검색어(맛집, 카페, 숙소)를 띄어쓰기 하여 스트링으로 입력하세요. 
    크롤링 하고 싶은 페이지의 개수를 정수로 입력하세요. 
    원하는 리뷰 개수(정수)와 별점(float)을 입력하세요.
    ex) "수원시 맛집", 5, 200, 4.0 --> 리뷰가 200개 이상이고 별점이 4.0이상인 수원시 맛집을 추출합니다.
    6개의 리스트 반환합니다."""
    city = search.split()[0]
    category = search.split()[1]
    
    driver = wb.Chrome()
    url = f"https://www.google.co.kr/search?sca_esv=90548b20b23b480c&tbm=lcl&q={city}+{category}&rflfq=1&num=10&sa=X&ved=2ahUKEwjyx_7Vo8-LAxXZ2TQHHQ1lBwoQjGp6BAgwEAE&biw=694&bih=1225&dpr=1#rlfi=hd:;si:;mv:[[37.2920221,127.0484462],[37.2460498,126.99459900000001]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9"
    driver.get(url)
    time.sleep(4)

    # search 폴더 만들고 (만약, 있다면 안 만듦)
    if not os.path.isdir(search):
        os.mkdir(search)
    else:
        print(f"{search}폴더가 존재합니다")

    # - 한 번 클릭
    zoom_out = driver.find_element(By.CSS_SELECTOR, ".C1R54d+.WvCRR .QBykre .NMm5M")
    zoom_out.click()
    time.sleep(2)

    # 데이터 저장할 list
    restaurant_list = []
    score_list = []
    address_list = []
    comment_list = []
    bushour_list = []

    # score_l = []
    
    # 리뷰 개수 200개 이상이고, 별점 4.0이상인 식당 저장
    for j in range(page_number):
        # 리뷰 개수 확인
        comment_num_list = []
        comment_num = driver.find_elements(By.CSS_SELECTOR, ".Y0A0hc .RDApEe,YrbPuc")
        for c in comment_num:
            result = c.text[1:-1]
            # print(result)
            
            if "천" in result:
                result = result.replace("천", "")
                result = float(result) * 1000
                # print(result)
            
            if result != "":
                comment_num_list.append(int(result))   
        # print(comment_num_list)
        
        # 리뷰 개수가 150 넘으면 그 인덱스 기억해둠
        index1 = []
        for num in comment_num_list:
            if num > review_number:
                index1.append(comment_num_list.index(num))
        
        # 별점 확인 및 추출
        score_str = driver.find_elements(By.CSS_SELECTOR, ".rllt__details div+div span .Y0A0hc .yi40Hd") 
        # for i in index1:
        #     score_l.append(float(score_str[i].text))
        #     # print(score_str[i].text)

        # 리뷰 확인
        comment = driver.find_elements(By.CSS_SELECTOR, ".uDyWh.OSrXXb.btbrud")
        # print(comment)
            
        
        # 별점이 3.5가 넘으면
        # 클릭!
        for i, idx1 in enumerate(index1):
            if float(score_str[idx1].text) > star_number:
                score_str[idx1].click()
                time.sleep(1)
                
                try:
                    # 스폰서 인지 아닌지
                    sponsor = driver.find_element(By.CSS_SELECTOR, ".G9DTJe .QGUp7b")
                    print(sponsor.text)
                    time.sleep(0.5)
                
                except:
                    print("스폰서 아닙니다.")
                    time.sleep(0.5)
                
                    try:
                        # 폐업인지 아닌지
                        closedown = driver.find_element(By.CSS_SELECTOR, ".hBA2d,Shyhc")
                        print(closedown.text)
                        time.sleep(0.5)
                    
                    except:
                        print("정상 영업합니다.")  
                        time.sleep(0.5)
                        # 맛집명, 별점, 주소, 리뷰, 영업시간, 대표이미지 추출
                        # 맛집명
                        restaurant = driver.find_element(By.CSS_SELECTOR, ".qrShPb,pXs6bb,PZPZlf,q8U8x,aTI8gc,PPT5v")
                        restaurant_list.append(restaurant.text)
                        print(restaurant.text)
                        time.sleep(0.5)

                        # 별점
                        score_list.append(float(score_str[idx1].text))
                        print(float(score_str[idx1].text))
                        time.sleep(0.5)
                            
                        # 주소
                        address = driver.find_element(By.CSS_SELECTOR, ".LrzXr")
                        address_list.append(address.text)
                        print(address.text)
                        time.sleep(0.5)
                
                        # 리뷰 추출
                        # 리뷰 150개 넘고 별점 3.5넘는 가게의 리뷰만 추출
                        if comment == []:
                            print("한 줄 리뷰 생략합니다.")
                            comment_list.append("")
                            time.sleep(0.5)
                        else:
                            print(comment[idx1].text)
                            comment_list.append(comment[idx1].text)
                            time.sleep(0.5)
                
                        # 영업시간
                        # 영업시간 없는 경우 추가 해줘야됨!!!!!
                        try:
                            button = driver.find_element(By.CSS_SELECTOR, ".BTP3Ac")
                            button.click()
                            time.sleep(1)
                            bushour = driver.find_element(By.CSS_SELECTOR, ".a-h .b2JWxc")
                            print(bushour.text)
                            bushour_list.append(bushour.text)
                            time.sleep(0.5)
                            # bushour = driver.find_element(By.CSS_SELECTOR, ".JjSWRd span span")
                            # bushour_list.append(bushour.text)
                            # print(bushour.text)
                            # time.sleep(0.5)
                        except:
                            print("해당 장소에 대한 영업시간 없습니다.")
                            bushour_list.append("")
                            pass  # 요소가 없으면 그냥 넘어감
                            time.sleep(0.5)
                
                        # 대표 이미지
                        try:
                            img = driver.find_element(By.CSS_SELECTOR, ".vwrQge")
                            img_text = img.get_attribute("style")
                            img_url = img_text.split("(")[1].split(")")[0]
                            response = requests.get(img_url[1:-1])
                            img_data = response.content
                    
                            img_path = f"{search}/{restaurant.text}.jpg"
                            with open(img_path, "wb") as file: # wb: write byte
                                file.write(img_data)
                                print(f"{restaurant.text}.jpg 저장 완료")
                            print("------------------------")
                            time.sleep(0.5)
                        except:
                            print("해당 장소에 대한 이미지가 없습니다.")
                            print("------------------------")
    
        try:
            nextpage = driver.find_element(By.CSS_SELECTOR, "#pnnext .oeN89d")
            nextpage.click()
            print("-----------------다음 페이지-----------------")
            time.sleep(3)
        except:
            print("-----------------다음 페이지 없음-----------------")
            break

    
    print(f"{search} 페이지 크롤링 완료")
    
    print("장소이름", len(restaurant_list))
    print("별점",len(score_list))
    print("주소",len(address_list))
    print("영업시간",len(bushour_list))
    print("리뷰",len(comment_list))

    category_list = [category] * len(restaurant_list)

    return category_list, restaurant_list, score_list, address_list, bushour_list, comment_list    





        