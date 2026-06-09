import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="연령대별 교통사고 사상자 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 연령대별 교통사고 사상자 분석")

uploaded_file = st.file_uploader(
    "CSV 파일을 업로드하세요",
    type=["csv"]
)

if uploaded_file:

    # CSV 읽기
    df = pd.read_csv(uploaded_file, encoding="cp949")

    st.success("파일 업로드 완료!")

    # 연도 추출
    year_cols = [col for col in df.columns if str(col).startswith("20")]
    years = sorted(list(set([str(col).split(".")[0] for col in year_cols])))

    selected_year = st.selectbox(
        "📅 연도 선택",
        years
    )

    # 서울시 합계 행 찾기
    total_df = df[
        (df["자치구별(1)"] == "합계") &
        (df["자치구별(2)"] == "소계")
    ]

    death_row = total_df[total_df["항목"] == "사망자수"]
    injury_row = total_df[total_df["항목"] == "부상자수"]

    if not death_row.empty and not injury_row.empty:

        age_labels = [
            "12세 이하",
            "13~19세",
            "20~29세",
            "30~39세",
            "40~49세",
            "50~59세",
            "60~64세",
            "65세 이상"
        ]

        injury_values = []
        death_values = []

        for age in age_labels:

            col_name = f"{selected_year}.{age}"

            if col_name in df.columns:

                injury = injury_row.iloc[0][col_name]
                death = death_row.iloc[0][col_name]

                injury_values.append(int(injury))
                death_values.append(int(death))

        st.subheader(f"📊 {selected_year}년 연령대별 교통사고 사상자")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(
            age_labels,
            injury_values,
            marker="o",
            linewidth=3,
            color="blue",
            label="부상자수"
        )

        ax.plot(
            age_labels,
            death_values,
            marker="o",
            linewidth=3,
            color="red",
            label="사망자수"
        )

        ax.set_xlabel("연령대")
        ax.set_ylabel("인원수")
        ax.set_title(f"{selected_year}년 연령대별 교통사고 사상자")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        result_df = pd.DataFrame({
            "연령대": age_labels,
            "부상자수": injury_values,
            "사망자수": death_values
        })

        st.dataframe(
            result_df,
            use_container_width=True
        )

else:
    st.info("CSV 파일을 업로드해주세요.")
