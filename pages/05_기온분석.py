import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="서울 기온 분석 및 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석 및 미래 예측")

# --------------------
# 데이터 불러오기
# --------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        try:
            df = pd.read_csv("seoul.csv", encoding="utf-8")
        except:
            df = pd.read_csv("seoul.csv", encoding="euc-kr")

    df.columns = df.columns.str.strip()

    date_col = [c for c in df.columns if "날짜" in c][0]

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    df = df.dropna(subset=[date_col])

    return df, date_col


df, date_col = load_data()

# --------------------
# 날짜 선택
# --------------------
selected_date = st.date_input(
    "📅 날짜 선택",
    value=df[date_col].max().date()
)

selected_date = pd.to_datetime(selected_date)
selected_year = selected_date.year

year_df = df[df[date_col].dt.year == selected_year]

st.subheader(f"📈 {selected_year}년 기온 변화")

# --------------------
# 꺾은선 그래프
# --------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=year_df[date_col],
        y=year_df["최고기온(℃)"],
        mode="lines",
        name="최고기온",
        line=dict(
            color="red",
            width=3
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=year_df[date_col],
        y=year_df["최저기온(℃)"],
        mode="lines",
        name="최저기온",
        line=dict(
            color="lightskyblue",
            width=3
        )
    )
)

fig.update_layout(
    height=600,
    xaxis_title="날짜",
    yaxis_title="기온(℃)",
    legend_title="범례",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 선택 날짜 정보
# --------------------
selected_row = year_df[
    year_df[date_col].dt.date == selected_date.date()
]

if not selected_row.empty:

    st.subheader("📋 선택 날짜 정보")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🔥 최고기온",
            f"{selected_row.iloc[0]['최고기온(℃)']:.1f}℃"
        )

    with col2:
        st.metric(
            "❄️ 최저기온",
            f"{selected_row.iloc[0]['최저기온(℃)']:.1f}℃"
        )

# --------------------
# 연도별 최고/최저 집계
# --------------------
annual = (
    df.groupby(df[date_col].dt.year)
    .agg({
        "최고기온(℃)": "max",
        "최저기온(℃)": "min"
    })
    .reset_index()
)

annual.columns = [
    "연도",
    "연간최고기온",
    "연간최저기온"
]

# --------------------
# 미래 연도 예측
# --------------------
st.header("🔮 미래 기온 예측")

future_year = st.slider(
    "예측할 미래 연도",
    min_value=2025,
    max_value=2100,
    value=2050
)

X = annual[["연도"]]

# 최고기온 모델
model_max = LinearRegression()
model_max.fit(X, annual["연간최고기온"])

# 최저기온 모델
model_min = LinearRegression()
model_min.fit(X, annual["연간최저기온"])

future_X = np.array([[future_year]])

pred_max = model_max.predict(future_X)[0]
pred_min = model_min.predict(future_X)[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"{future_year}년 예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with col2:
    st.metric(
        f"{future_year}년 예상 최저기온",
        f"{pred_min:.1f}℃"
    )

# --------------------
# 예측 시각화
# --------------------
future_years = np.arange(
    annual["연도"].max() + 1,
    future_year + 1
)

future_max = model_max.predict(
    future_years.reshape(-1, 1)
)

future_min = model_min.predict(
    future_years.reshape(-1, 1)
)

fig2 = go.Figure()

# 실제 최고기온
fig2.add_trace(
    go.Scatter(
        x=annual["연도"],
        y=annual["연간최고기온"],
        mode="lines",
        name="실제 최고기온",
        line=dict(color="red")
    )
)

# 실제 최저기온
fig2.add_trace(
    go.Scatter(
        x=annual["연도"],
        y=annual["연간최저기온"],
        mode="lines",
        name="실제 최저기온",
        line=dict(color="lightskyblue")
    )
)

# 예측 최고기온
fig2.add_trace(
    go.Scatter(
        x=future_years,
        y=future_max,
        mode="lines",
        name="예측 최고기온",
        line=dict(
            color="darkred",
            dash="dash"
        )
    )
)

# 예측 최저기온
fig2.add_trace(
    go.Scatter(
        x=future_years,
        y=future_min,
        mode="lines",
        name="예측 최저기온",
        line=dict(
            color="blue",
            dash="dash"
        )
    )
)

fig2.update_layout(
    title="서울 미래 기온 예측",
    height=650,
    xaxis_title="연도",
    yaxis_title="기온(℃)",
    hovermode="x unified"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.info(
    "예측값은 선형회귀 기반 단순 예측으로 실제 미래 기온과 다를 수 있습니다."
)
