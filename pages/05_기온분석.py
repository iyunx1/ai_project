import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")
st.write("날짜를 선택하면 해당 연도의 최고기온과 최저기온 변화를 확인할 수 있습니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    return df

df = load_data()

# 날짜 선택
selected_date = st.date_input(
    "📅 날짜를 선택하세요",
    value=df["날짜"].max().date(),
    min_value=df["날짜"].min().date(),
    max_value=df["날짜"].max().date()
)

selected_date = pd.to_datetime(selected_date)

# 선택한 연도 추출
selected_year = selected_date.year

year_df = df[df["날짜"].dt.year == selected_year].copy()

st.subheader(f"📈 {selected_year}년 최고·최저 기온 변화")

# 그래프 생성
fig = go.Figure()

# 최고기온 (빨간색)
fig.add_trace(
    go.Scatter(
        x=year_df["날짜"],
        y=year_df["최고기온(℃)"],
        mode="lines",
        name="최고기온",
        line=dict(color="red", width=3)
    )
)

# 최저기온 (연한 하늘색)
fig.add_trace(
    go.Scatter(
        x=year_df["날짜"],
        y=year_df["최저기온(℃)"],
        mode="lines",
        name="최저기온",
        line=dict(color="lightskyblue", width=3)
    )
)

# 선택한 날짜 표시
selected_row = year_df[year_df["날짜"] == selected_date]

if not selected_row.empty:
    max_temp = selected_row.iloc[0]["최고기온(℃)"]
    min_temp = selected_row.iloc[0]["최저기온(℃)"]

    fig.add_vline(
        x=selected_date,
        line_width=2,
        line_dash="dash",
        line_color="green"
    )

    st.success(
        f"""
        📅 선택 날짜: {selected_date.strftime('%Y-%m-%d')}

        🔥 최고기온: {max_temp:.1f}℃

        ❄️ 최저기온: {min_temp:.1f}℃
        """
    )

# 그래프 설정
fig.update_layout(
    height=600,
    xaxis_title="날짜",
    yaxis_title="기온(℃)",
    hovermode="x unified",
    legend=dict(
        title="범례",
        orientation="h",
        y=1.08,
        x=0
    )
)

st.plotly_chart(fig, use_container_width=True)

# 선택 날짜 정보 표시
st.subheader("📋 선택 날짜 상세 정보")

if not selected_row.empty:
    st.dataframe(
        selected_row[
            ["날짜", "평균기온(℃)", "최저기온(℃)", "최고기온(℃)"]
        ],
        use_container_width=True
    )
