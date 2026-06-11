import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="교통사고 연령별 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 2025년 교통사고 연령별 분석")

# ==========================
# CSV 불러오기
# ==========================
df = pd.read_csv("jjjjjjjh.csv", encoding="cp949")

# 서울 전체 데이터
death_row = df.iloc[2]
injury_row = df.iloc[3]

ages = [
    "12세 이하",
    "13~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~64세",
    "65세 이상"
]

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

# ==========================
# 부상자수 그래프
# ==========================
st.subheader("🔵 연령별 부상자수")

fig_injury = go.Figure()

fig_injury.add_trace(
    go.Scatter(
        x=ages,
        y=injury_values,
        mode="lines+markers",
        line=dict(color="blue", width=4),
        marker=dict(size=10),
        name="부상자수"
    )
)

fig_injury.update_layout(
    title="연령별 부상자수",
    xaxis_title="연령대",
    yaxis_title="부상자수(명)",
    height=500
)

fig_injury.update_yaxes(
    tickvals=[0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000],
    ticktext=[
        "0명","1천명","2천명","3천명","4천명",
        "5천명","6천명","7천명","8천명","9천명","1만명"
    ]
)

st.plotly_chart(fig_injury, use_container_width=True)

# ==========================
# 사망자수 그래프
# ==========================
st.subheader("🔴 연령별 사망자수")

fig_death = go.Figure()

fig_death.add_trace(
    go.Scatter(
        x=ages,
        y=death_values,
        mode="lines+markers",
        line=dict(color="red", width=4),
        marker=dict(size=10),
        name="사망자수"
    )
)

fig_death.update_layout(
    title="연령별 사망자수",
    xaxis_title="연령대",
    yaxis_title="사망자수(명)",
    height=500
)

fig_death.update_yaxes(
    tickvals=[0,20,40,60,80,100,120],
    ticktext=[
        "0명","20명","40명","60명",
        "80명","100명","120명"
    ]
)

st.plotly_chart(fig_death, use_container_width=True)

# ==========================
# 표
# ==========================
st.subheader("📋 데이터")

injury_table = pd.DataFrame({
    "연령대": ages,
    "부상자수": injury_values
})

death_table = pd.DataFrame({
    "연령대": ages,
    "사망자수": death_values
})

col1, col2 = st.columns(2)

with col1:
    st.write("🔵 부상자수")
    st.dataframe(injury_table, use_container_width=True)

with col2:
    st.write("🔴 사망자수")
    st.dataframe(death_table, use_container_width=True)
