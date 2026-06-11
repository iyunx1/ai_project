import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="교통사고 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 2025년 교통사고 연령별 분석")

# 파일 읽기
df = pd.read_csv("jjjjjjjh(1).csv", encoding="cp949")

# 실제 헤더 만들기
age_names = [
    "합계",
    "12세 이하",
    "13~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~64세",
    "65세 이상",
    "불명"
]

# 서울 전체 데이터
death_row = df.iloc[2]
injury_row = df.iloc[3]

ages = age_names[1:-1]

death_values = [
    int(death_row["2025.1"]),
    int(death_row["2025.2"]),
    int(death_row["2025.3"]),
    int(death_row["2025.4"]),
    int(death_row["2025.5"]),
    int(death_row["2025.6"]),
    int(death_row["2025.7"]),
    int(death_row["2025.8"])
]

injury_values = [
    int(injury_row["2025.1"]),
    int(injury_row["2025.2"]),
    int(injury_row["2025.3"]),
    int(injury_row["2025.4"]),
    int(injury_row["2025.5"]),
    int(injury_row["2025.6"]),
    int(injury_row["2025.7"]),
    int(injury_row["2025.8"])
]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ages,
        y=injury_values,
        mode="lines+markers",
        name="부상자수",
        line=dict(color="blue", width=4)
    )
)

fig.add_trace(
    go.Scatter(
        x=ages,
        y=death_values,
        mode="lines+markers",
        name="사망자수",
        line=dict(color="red", width=4)
    )
)

fig.update_layout(
    title="연령별 부상자수 · 사망자수",
    xaxis_title="연령대",
    yaxis_title="인원수",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🔵 부상자수")

st.dataframe(
    pd.DataFrame({
        "연령대": ages,
        "부상자수": injury_values
    }),
    use_container_width=True,
    hide_index=True
)

st.subheader("🔴 사망자수")

st.dataframe(
    pd.DataFrame({
        "연령대": ages,
        "사망자수": death_values
    }),
    use_container_width=True,
    hide_index=True
)
