제주도 여행 가이드 웹페이지를 실행하기 위한 코드

폴더 위치는 다음과 같아야 함
jeju_project/ 
├── static/
│   └── JEJU/
│       ├── market.png
│       ├── orem.png
│       └── ...
├── templates/
│   ├── jeju.html
│   ├── market.html
│   └── ...
└── jeju_server.py

jeju.html이 메인 홈페이지
나머지는 카테고리별 하위 페이지

jeju_server.py는 서버 구동 코드 (포트번호 5001)
