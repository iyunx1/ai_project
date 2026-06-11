import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="2025 서울 교통사고 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 서울시 자치구별 교통사고 분석")

st.info("""
📅 본 서비스는 **2025년 서울시 교통사고 데이터**를 기반으로 제작되었습니다.

🏙️ 자치구를 선택하면 연령별 부상자수와 사망자수를 확인할 수 있습니다.
""")

# =========================
# 데이터 불러오기
# =========================

# CSV가 pages 폴더 밖에 있을 경우
df = pd.read_csv("../jjjjjjjh.csv", encoding="cp949")

# 실제 데이터만 사용
df = df.iloc[2:].reset_index(drop=True)

# =========================
# 자치구 목록
# =========================

gu_list = sorted([
    x for x in df["자치구별(2)"].unique()
    if x not in ["소계", "자치구별(2)"]
])

selected_gu = st.selectbox(
    "🏙️ 자치구를 선택하세요",
    gu_list
)

# =========================
# 선택 구 데이터
# =========================

gu_df = df[df["자치구별(2)"] == selected_gu]

death_row = gu_df[gu_df["항목"] == "사망자수"].iloc[0]
injury_row = gu_df[gu_df["항목"] == "부상자수"].iloc[0]

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

cols = [
    "2025.1",
    "2025.2",
    "2025.3",
    "2025.4",
    "2025.5",
    "2025.6",
    "2025.7",
    "2025.8"
]

def convert_value(v):
    if str(v).strip() == "-":
        return 0
    return int(v)

death_values = [convert_value(death_row[c]) for c in cols]
injury_values = [convert_value(injury_row[c]) for c in cols]

# =========================
# 부상자수 그래프
# =========================

st.subheader(f"🔵 {selected_gu} 연령별 부상자수 (2025년)")

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=ages,
        y=injury_values,
        mode="lines+markers",
        line=dict(color="blue", width=4),
        marker=dict(size=10),
        name="부상자수"
    )
)

fig1.update_layout(
    height=500,
    xaxis_title="연령대",
    yaxis_title="부상자수(명)"
)

fig1.update_yaxes(tickformat=",d")

st.plotly_chart(fig1, use_container_width=True)

# =========================
# 사망자수 그래프
# =========================

st.subheader(f"🔴 {selected_gu} 연령별 사망자수 (2025년)")

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=ages,
        y=death_values,
        mode="lines+markers",
        line=dict(color="red", width=4),
        marker=dict(size=10),
        name="사망자수"
    )
)

fig2.update_layout(
    height=500,
    xaxis_title="연령대",
    yaxis_title="사망자수(명)"
)

fig2.update_yaxes(tickformat=",d")

st.plotly_chart(fig2, use_container_width=True)

# =========================
# 데이터 표
# =========================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 부상자수")

    injury_table = pd.DataFrame({
        "연령대": ages,
        "부상자수": injury_values
    })

    st.dataframe(
        injury_table,
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.subheader("🔴 사망자수")

    death_table = pd.DataFrame({
        "연령대": ages,
        "사망자수": death_values
    })

    st.dataframe(
        death_table,
        hide_index=True,
        use_container_width=True
    )
