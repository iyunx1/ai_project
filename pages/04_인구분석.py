import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="성북구 연령대별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 성북구 연령대별 인구 많은 동 찾기")

# CSV 불러오기
try:
    df = pd.read_csv("population.csv", encoding="cp949")
except:
    df = pd.read_csv("population.csv", encoding="utf-8")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 첫 번째 컬럼 = 동 이름
dong_col = df.columns[0]

# 연령대 컬럼 찾기
age_cols = [
    col for col in df.columns
    if ("세" in str(col)) or ("이상" in str(col))
]

# 전체 행 제거
df = df.iloc[1:].copy()

st.subheader("연령대를 선택하세요")

selected_age = st.selectbox(
    "연령대",
    age_cols
)

# 숫자 변환
df[selected_age] = (
    df[selected_age]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df[selected_age] = pd.to_numeric(
    df[selected_age],
    errors="coerce"
).fillna(0)

# 정렬
top_df = df.sort_values(
    selected_age,
    ascending=False
)

# 상위 10개
top10 = top_df.head(10)

# 색상
colors = ["hotpink"] + ["lightgreen"] * (len(top10) - 1)

# 그래프
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=top10[selected_age],
        y=top10[dong_col],
        orientation="h",
        marker_color=colors
    )
)

fig.update_layout(
    title=f"{selected_age} 인구가 많은 동 TOP 10",
    xaxis_title="인구수",
    yaxis_title="행정동",
    plot_bgcolor="#f5f5f5",
    paper_bgcolor="#f5f5f5",
    height=700
)

fig.update_yaxes(
    autorange="reversed"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 순위표
st.subheader("🏆 순위")

rank_df = top10[[dong_col, selected_age]].reset_index(drop=True)
rank_df.index = rank_df.index + 1

st.dataframe(
    rank_df,
    use_container_width=True
)
