import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석 및 미래 예측")

# -------------------
# 데이터 불러오기
# -------------------
@st.cache_data
def load_data():

    encodings = ["cp949", "euc-kr", "utf-8"]

    df = None

    for enc in encodings:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            break
        except:
            pass

    if df is None:
        st.error("CSV 파일을 읽을 수 없습니다.")
        st.stop()

    df.columns = df.columns.str.strip()

    # 날짜 컬럼 찾기
    date_candidates = [c for c in df.columns if "날짜" in c]

    if len(date_candidates) == 0:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.write(df.columns.tolist())
        st.stop()

    date_col = date_candidates[0]

    # 날짜 변환
    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    # 날짜 없는 행 제거
    df = df.dropna(subset=[date_col])

    # 기온 컬럼 찾기
    max_col = [c for c in df.columns if "최고기온" in c][0]
    min_col = [c for c in df.columns if "최저기온" in c][0]

    # 숫자형 변환
    df[max_col] = pd.to_numeric(
        df[max_col],
        errors="coerce"
    )

    df[min_col] = pd.to_numeric(
        df[min_col],
        errors="coerce"
    )

    # 결측치 제거
    df = df.dropna(
        subset=[
            max_col,
            min_col
        ]
    )

    return df, date_col, max_col, min_col


df, date_col, max_col, min_col = load_data()

# -------------------
# 날짜 선택
# -------------------
st.header("📅 날짜별 기온 확인")

selected_date = st.date_input(
    "날짜를 선택하세요",
    value=df[date_col].max().date(),
    min_value=df[date_col].min().date(),
    max_value=df[date_col].max().date()
)

selected_date = pd.to_datetime(selected_date)

selected_year = selected_date.year

year_df = df[
    df[date_col].dt.year == selected_year
]

# -------------------
# 연도 그래프
# -------------------
st.subheader(f"{selected_year}년 기온 변화")

fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=year_df[date_col],
        y=year_df[max_col],
        mode="lines",
        name="최고기온",
        line=dict(
            color="red",
            width=3
        )
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=year_df[date_col],
        y=year_df[min_col],
        mode="lines",
        name="최저기온",
        line=dict(
            color="lightskyblue",
            width=3
        )
    )
)

fig.add_vline(
    x=selected_date,
    line_dash="dash",
    line_color="green"
)

fig.update_layout(
    height=600,
    xaxis_title="날짜",
    yaxis_title="기온(℃)",
    legend_title="범례",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# 선택 날짜 정보
# -------------------
selected_row = year_df[
    year_df[date_col].dt.date
    == selected_date.date()
]

st.subheader("📋 선택 날짜 정보")

if not selected_row.empty:

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🔥 최고기온",
            f"{selected_row.iloc[0][max_col]:.1f}℃"
        )

    with col2:
        st.metric(
            "❄️ 최저기온",
            f"{selected_row.iloc[0][min_col]:.1f}℃"
        )

# -------------------
# 미래 예측
# -------------------
st.header("🔮 미래 기온 예측")

annual = (
    df.groupby(
        df[date_col].dt.year
    )
    .agg({
        max_col: "max",
        min_col: "min"
    })
    .reset_index()
)

annual.columns = [
    "연도",
    "연간최고기온",
    "연간최저기온"
]

annual["연간최고기온"] = pd.to_numeric(
    annual["연간최고기온"],
    errors="coerce"
)

annual["연간최저기온"] = pd.to_numeric(
    annual["연간최저기온"],
    errors="coerce"
)

annual = annual.dropna()

if len(annual) < 10:
    st.error("예측에 사용할 데이터가 부족합니다.")
    st.stop()

future_year = st.slider(
    "예측 연도 선택",
    min_value=int(annual["연도"].max()) + 1,
    max_value=2100,
    value=2050
)

X = annual[["연도"]]

# 최고기온 모델
model_max = LinearRegression()
model_max.fit(
    X,
    annual["연간최고기온"]
)

# 최저기온 모델
model_min = LinearRegression()
model_min.fit(
    X,
    annual["연간최저기온"]
)

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

# -------------------
# 예측 그래프
# -------------------
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

fig2.add_trace(
    go.Scatter(
        x=annual["연도"],
        y=annual["연간최고기온"],
        mode="lines",
        name="실제 최고기온",
        line=dict(color="red")
    )
)

fig2.add_trace(
    go.Scatter(
        x=annual["연도"],
        y=annual["연간최저기온"],
        mode="lines",
        name="실제 최저기온",
        line=dict(color="lightskyblue")
    )
)

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
    height=650,
    xaxis_title="연도",
    yaxis_title="기온(℃)",
    hovermode="x unified",
    legend_title="범례"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.info(
    "※ 미래 기온은 과거 데이터의 추세를 이용한 선형회귀 예측 결과입니다."
)
