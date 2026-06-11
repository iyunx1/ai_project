import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="교통사고 연령별 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 교통사고 연령별 사망자·부상자 분석")

# CSV 불러오기
df = pd.read_csv("교통사고.csv", encoding="utf-8")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 연도 컬럼 찾기
year_col = [c for c in df.columns if "연도" in c][0]

# 연도 선택
years = sorted(df[year_col].unique())
selected_year = st.selectbox("📅 연도를 선택하세요", years)

# 선택 연도 데이터
year_df = df[df[year_col] == selected_year]

# 사망자수 / 부상자수 분리
injury_df = year_df[year_df["항목"] == "부상자수"]
death_df = year_df[year_df["항목"] == "사망자수"]

# 연령대 컬럼
age_cols = [
    "12세 이하",
    "13~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~64세",
    "65세 이상"
]

# 서울 전체 합계
injury_values = injury_df[age_cols].sum()
death_values = death_df[age_cols].sum()

st.subheader(f"📊 {selected_year}년 연령별 교통사고 현황")

fig = go.Figure()

# 부상자수
fig.add_trace(
    go.Scatter(
        x=age_cols,
        y=injury_values,
        mode="lines+markers",
        name="부상자수",
        line=dict(color="blue", width=4)
    )
)

# 사망자수
fig.add_trace(
    go.Scatter(
        x=age_cols,
        y=death_values,
        mode="lines+markers",
        name="사망자수",
        line=dict(color="red", width=4)
    )
)

fig.update_layout(
    title="연령별 부상자수 · 사망자수",
    xaxis_title="연령대",
    yaxis_title="인원 수",
    hovermode="x unified",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# 부상자수 표
st.subheader("🔵 연령별 부상자수")

injury_table = pd.DataFrame({
    "연령대": age_cols,
    "부상자수": injury_values.values
})

st.dataframe(
    injury_table,
    use_container_width=True,
    hide_index=True
)

# 사망자수 표
st.subheader("🔴 연령별 사망자수")

death_table = pd.DataFrame({
    "연령대": age_cols,
    "사망자수": death_values.values
})

st.dataframe(
    death_table,
    use_container_width=True,
    hide_index=True
)
