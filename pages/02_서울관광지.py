import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 인기 관광지 TOP10",
    layout="centered"
)

# 제목
st.title("🇰🇷 외국인들이 좋아하는 서울 관광지 TOP10")
st.write("서울의 대표 관광지를 지도에서 확인해보세요! ✨")

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "location": [37.579617, 126.977041],
        "station": "경복궁역 (3호선)",
        "fun": """
🏯 조선 시대 궁궐 분위기를 직접 느낄 수 있어요.
👘 한복을 빌려 입고 사진 찍으면 정말 예쁘게 나와요.
📸 근정전과 경회루는 외국인들에게 인기 포토존이에요.
🌳 주변 삼청동 카페 거리까지 함께 구경하기 좋아요.
"""
    },
    {
        "name": "명동",
        "location": [37.563757, 126.985302],
        "station": "명동역 (4호선)",
        "fun": """
🛍️ 한국 화장품과 패션 쇼핑을 즐기기 좋은 곳이에요.
🍢 길거리 음식이 정말 다양해서 먹거리 천국으로 유명해요.
📷 밤이 되면 네온사인 분위기가 더 화려해져요.
☕ 감성 카페와 디저트 맛집도 많아요.
"""
    },
    {
        "name": "남산서울타워",
        "location": [37.551169, 126.988227],
        "station": "명동역 (4호선)",
        "fun": """
🌃 서울 야경을 한눈에 볼 수 있는 대표 명소예요.
🚠 케이블카를 타고 올라가는 재미도 있어요.
🔒 사랑의 자물쇠 포토존이 유명해요.
🌙 밤에 방문하면 더욱 로맨틱한 분위기를 느낄 수 있어요.
"""
    },
    {
        "name": "홍대거리",
        "location": [37.556268, 126.922641],
        "station": "홍대입구역 (2호선)",
        "fun": """
🎤 거리 버스킹 공연이 자주 열려요.
🍜 맛집과 트렌디한 카페가 정말 많아요.
🛍️ 개성 있는 패션 쇼핑을 즐길 수 있어요.
🎨 젊고 자유로운 분위기를 느끼기 좋은 핫플레이스예요.
"""
    },
    {
        "name": "북촌한옥마을",
        "location": [37.582604, 126.983998],
        "station": "안국역 (3호선)",
        "fun": """
🏡 전통 한옥 골목길을 걸으며 힐링할 수 있어요.
📸 감성적인 사진 촬영 장소로 유명해요.
☕ 조용한 한옥 카페들이 많아 분위기가 좋아요.
🎎 한국 전통문화를 가까이에서 느낄 수 있어요.
"""
    },
    {
        "name": "롯데월드",
        "location": [37.511115, 127.098167],
        "station": "잠실역 (2호선)",
        "fun": """
🎢 다양한 놀이기구와 퍼레이드를 즐길 수 있어요.
❄️ 실내 아이스링크도 유명해요.
🎠 가족, 친구와 함께 하루 종일 놀기 좋아요.
📷 야간 퍼레이드와 조명이 정말 화려해요.
"""
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "location": [37.566526, 127.009223],
        "station": "동대문역사문화공원역 (2호선)",
        "fun": """
✨ 미래적인 건축 디자인으로 유명한 장소예요.
🖼️ 다양한 전시회와 팝업스토어가 열려요.
🌃 밤에는 LED 장미정원이 정말 예뻐요.
🛍️ 근처 쇼핑몰과 야시장도 함께 즐길 수 있어요.
"""
    },
    {
        "name": "한강공원",
        "location": [37.528316, 126.932598],
        "station": "여의나루역 (5호선)",
        "fun": """
🚴 자전거를 타며 한강 바람을 느낄 수 있어요.
🍗 치킨과 라면 먹으며 피크닉하기 좋아요.
🌅 저녁 노을과 야경이 정말 아름다워요.
🛶 수상 스포츠와 유람선 체험도 가능해요.
"""
    },
    {
        "name": "인사동",
        "location": [37.574304, 126.986998],
        "station": "안국역 (3호선)",
        "fun": """
🎁 전통 기념품 쇼핑하기 좋은 거리예요.
🍵 전통찻집에서 여유로운 시간을 보낼 수 있어요.
🎨 골목마다 공예품과 갤러리가 많아요.
📸 한국 전통 감성을 느끼기 좋은 장소예요.
"""
    },
    {
        "name": "코엑스",
        "location": [37.512524, 127.058819],
        "station": "삼성역 (2호선)",
        "fun": """
📚 별마당도서관은 인증샷 명소로 유명해요.
🛍️ 대형 쇼핑몰이라 쇼핑하기 좋아요.
🐠 아쿠아리움에서 다양한 해양 생물을 볼 수 있어요.
☕ 실내 데이트와 휴식 장소로도 인기예요.
"""
    }
]

# 지도 생성
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap"
)

# 🔵 파란색 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"""
        <b>{place['name']}</b><br>
        🚉 {place['station']}
        """,
        tooltip=place["name"],
        icon=folium.Icon(
            color="blue",
            icon="info-sign"
        )
    ).add_to(seoul_map)

# 지도 출력 (기존보다 약 60% 크기)
st_folium(seoul_map, width=720, height=420)

# 구분선
st.markdown("---")

# 관광지 선택
st.subheader("🎈 관광지 상세 정보")

selected_place = st.selectbox(
    "관광지를 선택하세요 👇",
    [place["name"] for place in places]
)

# 선택된 관광지 정보 출력
for place in places:
    if place["name"] == selected_place:
        st.markdown(f"""
## 📍 {place['name']}

### 🚇 가장 가까운 지하철역
**{place['station']}**

### 🎉 여기서 할 수 있는 놀거리
{place['fun']}
""")

st.markdown("---")
st.caption("Made with Streamlit + Folium 💙")
