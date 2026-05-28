# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="🌍 MBTI 국가 분석기",
    page_icon="🌈",
    layout="wide"
)

# ---------------------------
# 제목
# ---------------------------
st.title("🌍 MBTI 국가 분석 대시보드")
st.markdown("국가별 MBTI 비율과 MBTI TOP 국가를 분석해보자 💖")

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# ---------------------------
# MBTI 컬럼
# ---------------------------
mbti_columns = [
    'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
    'ISTP', 'ISFP', 'INFP', 'INTP',
    'ESTP', 'ESFP', 'ENFP', 'ENTP',
    'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
]

# =========================================================
# 1️⃣ 국가 선택 → MBTI 그래프
# =========================================================

st.divider()
st.header("🌎 국가별 MBTI 비율 분석")

countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "국가를 선택하세요 ✨",
    countries
)

country_data = df[df["Country"] == selected_country].iloc[0]

mbti_values = country_data[mbti_columns] * 100

country_chart_df = pd.DataFrame({
    "MBTI": mbti_columns,
    "Percentage": mbti_values
})

# ---------------------------
# 정렬
# ---------------------------
country_chart_df = country_chart_df.sort_values(
    by="Percentage",
    ascending=False
).reset_index(drop=True)

# ---------------------------
# 색상
# 1등 = 핫핑크
# 나머지 = 초록 그라데이션
# ---------------------------
green_colors = [
    "#d8f3dc",
    "#b7e4c7",
    "#95d5b2",
    "#74c69d",
    "#52b788",
    "#40916c",
    "#2d6a4f",
    "#1b4332",
    "#081c15"
]

colors = []

for i in range(len(country_chart_df)):
    if i == 0:
        colors.append("#ff1493")
    else:
        idx = min(i - 1, len(green_colors)-1)
        colors.append(green_colors[idx])

country_chart_df["Color"] = colors

# ---------------------------
# 그래프 생성
# ---------------------------
fig1 = go.Figure()

fig1.add_trace(
    go.Bar(
        x=country_chart_df["MBTI"],
        y=country_chart_df["Percentage"],
        marker_color=country_chart_df["Color"],
        text=country_chart_df["Percentage"].round(2).astype(str) + "%",
        textposition="outside"
    )
)

fig1.update_layout(
    title=f"📊 {selected_country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    height=650,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=15)
)

fig1.update_yaxes(
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)"
)

# ---------------------------
# 최고 MBTI 표시
# ---------------------------
top_mbti = country_chart_df.iloc[0]["MBTI"]
top_value = country_chart_df.iloc[0]["Percentage"]

st.success(
    f"💖 {selected_country}에서 가장 높은 MBTI는 "
    f"**{top_mbti} ({top_value:.2f}%)** 입니다!"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# 2️⃣ MBTI 선택 → TOP 10 국가
# =========================================================

st.divider()
st.header("🧠 MBTI 유형별 TOP 10 국가")

selected_mbti = st.selectbox(
    "MBTI 유형을 선택하세요 🔍",
    mbti_columns
)

# ---------------------------
# TOP 10 국가 추출
# ---------------------------
top10_df = (
    df[["Country", selected_mbti]]
    .sort_values(by=selected_mbti, ascending=False)
    .head(10)
)

top10_df[selected_mbti] = top10_df[selected_mbti] * 100

top10_df = top10_df.reset_index(drop=True)

# ---------------------------
# 색상
# ---------------------------
colors2 = []

for i in range(len(top10_df)):
    if i == 0:
        colors2.append("#ff1493")
    else:
        idx = min(i - 1, len(green_colors)-1)
        colors2.append(green_colors[idx])

top10_df["Color"] = colors2

# ---------------------------
# TOP 10 그래프
# ---------------------------
fig2 = go.Figure()

fig2.add_trace(
    go.Bar(
        x=top10_df["Country"],
        y=top10_df[selected_mbti],
        marker_color=top10_df["Color"],
        text=top10_df[selected_mbti].round(2).astype(str) + "%",
        textposition="outside"
    )
)

fig2.update_layout(
    title=f"🌍 {selected_mbti} 비율 TOP 10 국가",
    xaxis_title="국가",
    yaxis_title="비율 (%)",
    height=700,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=15)
)

fig2.update_yaxes(
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)"
)

# ---------------------------
# 최고 국가 표시
# ---------------------------
top_country = top10_df.iloc[0]["Country"]
top_percent = top10_df.iloc[0][selected_mbti]

st.success(
    f"🏆 {selected_mbti} 비율이 가장 높은 나라는 "
    f"**{top_country} ({top_percent:.2f}%)** 입니다!"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# 데이터 보기
# =========================================================

st.divider()

with st.expander("📄 전체 데이터 보기"):
    st.dataframe(df)
