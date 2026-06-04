import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

@st.cache_data
def load_data():

    # 인코딩 자동 처리
    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        try:
            df = pd.read_csv("seoul.csv", encoding="utf-8")
        except:
            df = pd.read_csv("seoul.csv", encoding="euc-kr")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 컬럼 찾기
    date_col = [c for c in df.columns if "날짜" in c][0]

    # 날짜 변환 (오류 무시)
    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    # 날짜 없는 행 제거
    df = df.dropna(subset=[date_col])

    return df, date_col


df, date_col = load_data()

# 날짜 선택
selected_date = st.date_input(
    "📅 날짜를 선택하세요",
    value=df[date_col].max().date(),
    min_value=df[date_col].min().date(),
    max_value=df[date_col].max().date()
)

selected_date = pd.to_datetime(selected_date)

# 선택 연도
selected_year = selected_date.year

year_df = df[df[date_col].dt.year == selected_year]

st.subheader(f"📈 {selected_year}년 기온 변화")

# 그래프
fig = go.Figure()

# 최고기온
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

# 최저기온
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

# 선택 날짜 표시
fig.add_vline(
    x=selected_date,
    line_dash="dash",
    line_color="green",
    line_width=2
)

fig.update_layout(
    height=650,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="기온(℃)",
    legend_title="범례"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 선택 날짜 데이터
selected_row = year_df[
    year_df[date_col].dt.date == selected_date.date()
]

st.subheader("📋 선택한 날짜 정보")

if not selected_row.empty:

    max_temp = selected_row.iloc[0]["최고기온(℃)"]
    min_temp = selected_row.iloc[0]["최저기온(℃)"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🔥 최고기온",
            f"{max_temp:.1f}℃"
        )

    with col2:
        st.metric(
            "❄️ 최저기온",
            f"{min_temp:.1f}℃"
        )

else:
    st.warning("선택한 날짜 데이터가 없습니다.")
