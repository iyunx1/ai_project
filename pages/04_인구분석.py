import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="성북구 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 성북구 인구 분석 대시보드")

# CSV 읽기
try:
    df = pd.read_csv("population.csv", encoding="cp949")
except:
    df = pd.read_csv("population.csv", encoding="utf-8")

# 컬럼명 정리
df.columns = df.columns.str.strip()

# 첫 번째 컬럼 = 동 이름
dong_col = df.columns[0]

# 연령 컬럼 찾기
age_cols = [
    col for col in df.columns
    if ("세" in str(col)) or ("이상" in str(col))
]

# 전체 행 제거
df = df.iloc[1:].copy()

# 숫자 변환
for col in age_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

tab1, tab2 = st.tabs([
    "📈 동별 연령 분포",
    "🏆 연령대별 동 순위"
])

# ----------------------------
# 탭1
# ----------------------------
with tab1:

    st.subheader("🏘️ 동 선택")

    selected_dong = st.selectbox(
        "동을 선택하세요",
        sorted(df[dong_col].unique())
    )

    row = df[df[dong_col] == selected_dong].iloc[0]

    population = [row[col] for col in age_cols]

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
            )
        )
    )

    fig.update_layout(
        title=f"{selected_dong} 연령별 인구 분포",
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        xaxis_title="연령대",
        yaxis_title="인구수",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# 탭2
# ----------------------------
with tab2:

    st.subheader("🎂 연령대 선택")

    selected_age = st.selectbox(
        "연령대를 선택하세요",
        age_cols
    )

    top10 = (
        df[[dong_col, selected_age]]
        .sort_values(selected_age, ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    top10["순위"] = [
        f"{i+1}위"
        for i in range(len(top10))
    ]

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=top10["순위"],
            y=top10[selected_age],
            mode="lines+markers+text",
            text=top10[dong_col],
            textposition="top center",
            line=dict(
                color="#87CEEB",
                width=4
            ),
            marker=dict(
                size=[14] + [10]*9,
                color=["hotpink"] + ["lightgreen"]*9
            )
        )
    )

    fig2.update_layout(
        title=f"{selected_age} 인구가 많은 동 TOP10",
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        xaxis_title="순위",
        yaxis_title="인구수",
        height=650
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.subheader("📋 순위표")

    rank_df = top10[[dong_col, selected_age]]
    rank_df.index = rank_df.index + 1

    st.dataframe(
        rank_df,
        use_container_width=True
    )
