# 🗺️ 서울 인기 관광지 TOP10 지도 앱 (Streamlit + Folium)

아래 내용을 그대로 사용하세요.

---

# 📄 app.py

```python
import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="서울 인기 관광지 TOP10", layout="wide")

# 제목
st.title("🇰🇷 외국인들이 좋아하는 서울 관광지 TOP10")
st.write("서울의 대표 관광지를 지도에서 확인해보세요! ✨")

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "location": [37.579617, 126.977041],
        "station": "경복궁역 (3호선)",
        "fun": "한복 체험, 궁궐 산책, 사진 촬영"
    },
    {
        "name": "명동",
        "location": [37.563757, 126.985302],
        "station": "명동역 (4호선)",
        "fun": "쇼핑, 길거리 음식, 화장품 투어"
    },
    {
        "name": "남산서울타워",
        "location": [37.551169, 126.988227],
        "station": "명동역 (4호선)",
        "fun": "야경 감상, 케이블카, 사랑의 자물쇠"
    },
    {
        "name": "홍대거리",
        "location": [37.556268, 126.922641],
        "station": "홍대입구역 (2호선)",
        "fun": "버스킹 공연, 맛집 탐방, 카페 투어"
    },
    {
        "name": "북촌한옥마을",
        "location": [37.582604, 126.983998],
        "station": "안국역 (3호선)",
        "fun": "전통 한옥 체험, 감성 사진 촬영"
    },
    {
        "name": "롯데월드",
        "location": [37.511115, 127.098167],
        "station": "잠실역 (2호선)",
        "fun": "놀이기구, 아이스링크, 퍼레이드"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "location": [37.566526, 127.009223],
        "station": "동대문역사문화공원역 (2호선)",
        "fun": "야간 산책, 전시회, 쇼핑"
    },
    {
        "name": "한강공원",
        "location": [37.528316, 126.932598],
        "station": "여의나루역 (5호선)",
        "fun": "치맥, 자전거 타기, 피크닉"
    },
    {
        "name": "인사동",
        "location": [37.574304, 126.986998],
        "station": "안국역 (3호선)",
        "fun": "전통 기념품 쇼핑, 전통찻집 방문"
    },
    {
        "name": "코엑스",
        "location": [37.512524, 127.058819],
        "station": "삼성역 (2호선)",
        "fun": "별마당도서관, 쇼핑, 아쿠아리움"
    }
]

# 지도 생성
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=place["name"],
        tooltip=f"가까운 지하철역: {place['station']}",
        icon=folium.Icon(color="blue")
    ).add_to(seoul_map)

# 지도 출력
st_folium(seoul_map, width=1200, height=600)

# 설명 영역
st.markdown("---")
st.subheader("🚇 관광지 정보")

for idx, place in enumerate(places, start=1):
    st.markdown(f"""
### {idx}. 📍 {place['name']}
- 🚉 가까운 지하철역: **{place['station']}**
- 🎈 놀거리: {place['fun']}
""")

st.markdown("---")
st.caption("Made with Streamlit + Folium 💙")
```

---

# 📄 requirements.txt

```txt
streamlit
folium
streamlit-folium
```

---

# 🚀 실행 방법

1. app.py 생성
2. requirements.txt 생성
3. GitHub 업로드
4. Streamlit Cloud 배포
5. Main file path를 app.py로 설정
