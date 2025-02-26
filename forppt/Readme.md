## 코드 설명

1. change_csv.ipunb -This notebook identifies data with incorrectly entered addresses and uses web crawling to retrieve the correct address data from Naver.
(주소가 제대로 입력되지 않은 데이터를 찾아 네이버에서 웹크롤링을 진행해 주소 데이터를 가져옵니다.)
2. get_distance.ipynb - This notebook calculates the straight-line distance between locations using latitude and longitude, and identifies restaurants, cafes, and accommodations within a 1km radius of each location.
(위도/경도를 사용하여 위치 간의 직선 거리를 계산하고, 각 위치에서 반경 1km 이내의 식당, 카페, 숙박 시설을 식별합니다.)
3. get_lac_loc.ipynb - This notebook uses the Google Cloud API to calculate latitude and longitude coordinates.
(Google Cloud API를 사용하여 위도 및 경도 좌표를 계산합니다.)
4. jeju_final.ipynb - This notebook consolidates data from various files to build the final database.
(다양한 파일의 데이터를 통합하여 최종 데이터베이스를 구축합니다.)
5. road_func.ipynb - This notebook inputs the addresses stored for each location into Naver Maps' route finding, and uses web scraping to output the walking distance and time required.
(각 위치에 저장된 주소를 네이버 지도 길 찾기에 입력하고 웹 스크래핑을 사용하여 도보 거리와 소요 시간을 출력합니다.)
