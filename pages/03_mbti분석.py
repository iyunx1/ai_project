# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="🌍 국가별 MBTI 분석",
    page_icon="🌈",
    layout="wide"
)

# ---------------------------
# 제목
# ---------------------------
st.title("🌍 국가별 MBTI 비율 분석기")
st.markdown("국가를 선택하면 MBTI 비율을 예쁜 그래프로 보여줘요 💖")

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# ---------------------------
# 국가 선택
# ---------------------------
countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "🌎 국가를 선택하세요",
    countries
)

# ---------------------------
# 선택 국가 데이터
# ---------------------------
country_data = df[df["Country"] == selected_country].iloc[0]

mbti_columns = [
    'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
    'ISTP', 'ISFP', 'INFP', 'INTP',
    'ESTP', 'ESFP', 'ENFP', 'ENTP',
    'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
]

mbti_values = country_data[mbti_columns] * 100

chart_df = pd.DataFrame({
    "MBTI": mbti_columns,
    "Percentage": mbti_values
})

# ---------------------------
# 색상 설정
# 1등 = 핫핑크
# 나머지 = 초록 그라데이션
# ---------------------------
max_value = chart_df["Percentage"].max()

green_colors = [
    "#d8f3dc",
    "#b7e4c7",
    "#95d5b2",
    "#74c69d",
    "#52b788",
    "#40916c",
    "#2d6a4f",
    "#1b4332"
]

sorted_df = chart_df.sort_values(
    by="Percentage",
    ascending=False
).reset_index(drop=True)

colors = []

for i, row in sorted_df.iterrows():
    if row["Percentage"] == max_value:
        colors.append("#ff1493")  # 핫핑크
    else:
        idx = min(i, len(green_colors)-1)
        colors.append(green_colors[idx])

sorted_df["Color"] = colors

# ---------------------------
# 그래프
# ---------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=sorted_df["MBTI"],
        y=sorted_df["Percentage"],
        marker_color=sorted_df["Color"],
        text=sorted_df["Percentage"].round(2).astype(str) + "%",
        textposition="outside"
    )
)

fig.update_layout(
    title=f"📊 {selected_country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    height=650,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=15),
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)"
)

# ---------------------------
# 최고 MBTI 표시
# ---------------------------
top_mbti = sorted_df.iloc[0]["MBTI"]
top_value = sorted_df.iloc[0]["Percentage"]

st.success(
    f"💖 {selected_country}에서 가장 높은 MBTI는 "
    f"**{top_mbti} ({top_value:.2f}%)** 입니다!"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 데이터 테이블
# ---------------------------
with st.expander("📄 데이터 보기"):
    st.dataframe(
        sorted_df[["MBTI", "Percentage"]]
        .style.format({"Percentage": "{:.2f}%"})
    )
