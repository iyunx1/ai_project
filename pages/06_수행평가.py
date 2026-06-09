import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="연도별 교통사고 사상자 분석",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 연도별 교통사고 사상자 분석")

uploaded_file = st.file_uploader(
    "CSV 파일을 업로드하세요",
    type=["csv"]
)

if uploaded_file is not None:

    # 원본 읽기
    raw = pd.read_csv(uploaded_file)

    # 실제 데이터 시작 부분 추출
    data = raw.iloc[2:].copy()

    # 연도 찾기
    year_cols = [col for col in raw.columns if col.startswith("20")]

    years = sorted(list(set(col.split(".")[0] for col in year_cols)))

    selected_year = st.selectbox(
        "📅 연도를 선택하세요",
        years
    )

    # 해당 연도 컬럼들만 선택
    target_cols = [col for col in raw.columns if col.startswith(selected_year)]

    df = data[["자치구별(1)", "자치구별(2)", "항목"] + target_cols]

    # 서울 전체 합계 데이터
    total_rows = df[
        (df["자치구별(1)"] == "합계") &
        (df["자치구별(2)"] == "소계")
    ]

    death_row = total_rows[
        total_rows["항목"] == "사망자수"
    ]

    injury_row = total_rows[
        total_rows["항목"] == "부상자수"
    ]

    if not death_row.empty and not injury_row.empty:

        total_deaths = death_row.iloc[0][target_cols[0]]
        total_injuries = injury_row.iloc[0][target_cols[0]]

        st.markdown("---")

        st.subheader(f"📊 {selected_year}년 서울시 전체 현황")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🤕 총 부상자 수",
                f"{int(total_injuries):,}명"
            )

        with col2:
            st.metric(
                "⚠️ 총 사망자 수",
                f"{int(total_deaths):,}명"
            )

        st.markdown("---")

        st.subheader("📈 연령대별 부상자 수")

        age_cols = target_cols[1:]

        age_labels = [
            "12세 이하",
            "13~19세",
            "20~29세",
            "30~39세",
            "40~49세",
            "50~59세",
            "60~64세",
            "65세 이상",
            "불명"
        ]

        injury_age = []

        for col in age_cols:
            value = injury_row.iloc[0][col]

            if value == "-":
                value = 0

            injury_age.append(int(value))

        chart_df = pd.DataFrame({
            "연령대": age_labels[:len(injury_age)],
            "부상자수": injury_age
        })

        st.bar_chart(
            chart_df.set_index("연령대")
        )

        st.dataframe(
            chart_df,
            use_container_width=True
        )

else:
    st.info("CSV 파일을 업로드해주세요.")
