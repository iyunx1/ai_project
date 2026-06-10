import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="연령별 교통사고 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 연령별 교통사고 부상자·사망자 분석")

# CSV 파일 불러오기
csv_path = Path(__file__).parent.parent / "jjjjjjjh.csv"
df = pd.read_csv(csv_path, encoding="utf-8")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 연도 컬럼 찾기
year_col = None
for col in df.columns:
    if "연도" in col:
        year_col = col
        break

if year_col is None:
    st.error("연도 컬럼을 찾을 수 없습니다.")
    st.stop()

# 연도 선택
years = sorted(df[year_col].dropna().unique())
selected_year = st.selectbox("📅 연도를 선택하세요", years)

year_df = df[df[year_col] == selected_year]

# 연령대 컬럼
age_groups = [
    "12세이하",
    "13~15세",
    "16~20세",
    "21~30세",
    "31~40세",
    "41~50세",
    "51~60세",
    "61~64세",
    "65세이상"
]

# 실제 컬럼명 찾기
injury_cols = []
death_cols = []

for age in age_groups:
    injury_match = None
    death_match = None

    for col in df.columns:
        if age in col and "부상" in col:
            injury_match = col
        if age in col and "사망" in col:
            death_match = col

    injury_cols.append(injury_match)
    death_cols.append(death_match)

# 합계 계산
injury_values = []
death_values = []

for icol, dcol in zip(injury_cols, death_cols):

    if icol is not None:
        injury_values.append(year_df[icol].sum())
    else:
        injury_values.append(0)

    if dcol is not None:
        death_values.append(year_df[dcol].sum())
    else:
        death_values.append(0)

# 부상자 그래프
st.subheader("🔵 연령별 부상자 수")

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=age_groups,
        y=injury_values,
        mode="lines+markers",
        line=dict(color="blue", width=4),
        marker=dict(size=8),
        name="부상자"
    )
)

fig1.update_layout(
    xaxis_title="연령대",
    yaxis_title="부상자 수",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# 사망자 그래프
st.subheader("🔴 연령별 사망자 수")

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=age_groups,
        y=death_values,
        mode="lines+markers",
        line=dict(color="red", width=4),
        marker=dict(size=8),
        name="사망자"
    )
)

fig2.update_layout(
    xaxis_title="연령대",
    yaxis_title="사망자 수",
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

# 데이터 표
result_df = pd.DataFrame({
    "연령대": age_groups,
    "부상자수": injury_values,
    "사망자수": death_values
})

st.subheader("📋 데이터")
st.dataframe(result_df, use_container_width=True)
