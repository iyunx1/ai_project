import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="성북구 동별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 성북구 동별 연령 인구 분석")

# CSV 읽기
try:
    df = pd.read_csv("population.csv", encoding="cp949")
except:
    df = pd.read_csv("population.csv", encoding="utf-8")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 첫 번째 컬럼을 동 이름 컬럼으로 사용
dong_col = df.columns[0]

# 연령대 컬럼 자동 찾기
age_cols = []
for col in df.columns:
    if ("세" in str(col)) or ("이상" in str(col)):
        age_cols.append(col)

# 총계 컬럼 찾기
total_col = None
for col in df.columns:
    if "계" in str(col):
        total_col = col
        break

# 데이터 확인
st.sidebar.subheader("데이터 정보")
st.sidebar.write(f"동 컬럼: {dong_col}")
st.sidebar.write(f"연령 컬럼 수: {len(age_cols)}")

# 전체 행 제거
dong_df = df.copy()

if len(dong_df) > 1:
    dong_df = dong_df.iloc[1:]

# 동 선택
selected_dong = st.selectbox(
    "🏘️ 동을 선택하세요",
    dong_df[dong_col].tolist()
)

# 선택 데이터
row = dong_df[dong_df[dong_col] == selected_dong].iloc[0]

# 인구 데이터
population = []
for col in age_cols:
    try:
        population.append(int(str(row[col]).replace(",", "")))
    except:
        population.append(0)

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
            color="#87CEEB",
            size=8
        )
    )
)

fig.update_layout(
    title=f"{selected_dong} 연령별 인구 분포",
    plot_bgcolor="#f5f5f5",
    paper_bgcolor="#f5f5f5",
    xaxis_title="나이",
    yaxis_title="인구수",
    height=600
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

# 총 인구
if total_col:
    st.metric(
        "👥 총 인구",
        f"{int(str(row[total_col]).replace(',', '')):,}명"
    )

# 원본 데이터 보기
with st.expander("원본 데이터 확인"):
    st.dataframe(df)
