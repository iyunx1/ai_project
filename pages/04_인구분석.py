import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="성북구 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 성북구 동별 연령 인구 분석")

# CSV 불러오기
df = pd.read_csv("population.csv", encoding="cp949")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 전체 행 제외
dong_df = df[df["행정동"] != "성북구"].copy()

# 동 선택
selected_dong = st.selectbox(
    "🏘️ 동을 선택하세요",
    sorted(dong_df["행정동"].unique())
)

# 선택한 동 데이터
row = dong_df[dong_df["행정동"] == selected_dong].iloc[0]

# 연령 컬럼
age_cols = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

# 데이터 추출
population = [row[col] for col in age_cols]

# 그래프
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=age_cols,
        y=population,
        mode="lines+markers",
        line=dict(
            color="#87CEEB",
            width=4
        ),
        marker=dict(
            size=8,
            color="#87CEEB"
        ),
        name="인구수"
    )
)

fig.update_layout(
    title=f"{selected_dong} 연령별 인구 분포",
    plot_bgcolor="#f5f5f5",
    paper_bgcolor="#f5f5f5",
    xaxis_title="연령대",
    yaxis_title="인구수",
    hovermode="x unified",
    height=600,
    font=dict(size=14)
)

fig.update_xaxes(
    showgrid=True,
    gridcolor="lightgray"
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="lightgray"
)

st.plotly_chart(fig, use_container_width=True)

# 요약 정보
st.subheader("📌 선택한 동 정보")

st.metric(
    "총 인구",
    f"{int(row['계']):,}명"
)
