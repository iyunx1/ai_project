import streamlit as st

st.set_page_config(
    page_title="✨ MBTI 진로 추천기",
    page_icon="🚀",
    layout="centered"
)

# MBTI별 진로 데이터
mbti_data = {
    "INTJ": [
        {
            "job": "🧠 데이터 분석가",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "논리적이고 계획 세우는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 5,000만~7,000만원 💰"
        },
        {
            "job": "🔬 연구원",
            "major": "생명과학과, 화학과",
            "personality": "혼자 깊게 탐구하는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,500만~8,000만원 💡"
        }
    ],

    "INTP": [
        {
            "job": "💻 프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "아이디어 많고 분석적인 사람!",
            "salary": "평균 연봉 약 4,500만~8,000만원 🚀"
        },
        {
            "job": "🧪 과학자",
            "major": "물리학과, 화학과",
            "personality": "궁금한 걸 끝까지 파고드는 사람!",
            "salary": "평균 연봉 약 5,000만~9,000만원 🔍"
        }
    ],

    "ENTJ": [
        {
            "job": "📈 CEO",
            "major": "경영학과",
            "personality": "리더십 강하고 추진력 있는 사람!",
            "salary": "평균 연봉 매우 높음 😎"
        },
        {
            "job": "⚖️ 변호사",
            "major": "법학과",
            "personality": "토론 잘하고 자신감 있는 사람!",
            "salary": "평균 연봉 약 7,000만~1억원 💼"
        }
    ],

    "ENTP": [
        {
            "job": "🎤 마케터",
            "major": "광고홍보학과",
            "personality": "아이디어 넘치고 말 잘하는 사람!",
            "salary": "평균 연봉 약 4,000만~6,000만원 📢"
        },
        {
            "job": "📺 콘텐츠 크리에이터",
            "major": "미디어학과",
            "personality": "창의적이고 새로운 걸 좋아하는 사람!",
            "salary": "인기에 따라 다양함 🌟"
        }
    ],

    "INFJ": [
        {
            "job": "💖 상담사",
            "major": "심리학과",
            "personality": "공감 능력 뛰어난 사람!",
            "salary": "평균 연봉 약 3,500만~5,500만원 🌷"
        },
        {
            "job": "📚 작가",
            "major": "문예창작과",
            "personality": "감수성 풍부하고 상상력 좋은 사람!",
            "salary": "실력과 경력에 따라 다양 ✍️"
        }
    ],

    "INFP": [
        {
            "job": "🎨 일러스트레이터",
            "major": "디자인학과",
            "personality": "감성적이고 창의적인 사람!",
            "salary": "평균 연봉 약 3,000만~5,000만원 🖌️"
        },
        {
            "job": "🎬 영화 감독",
            "major": "영화영상학과",
            "personality": "자기만의 세계관이 있는 사람!",
            "salary": "성공 여부에 따라 다양 🎥"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과",
            "personality": "사람 챙기는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,000만~7,000만원 🍎"
        },
        {
            "job": "🎙️ 아나운서",
            "major": "언론정보학과",
            "personality": "말 잘하고 밝은 에너지 가진 사람!",
            "salary": "평균 연봉 약 5,000만~8,000만원 📺"
        }
    ],

    "ENFP": [
        {
            "job": "🌈 광고 기획자",
            "major": "광고홍보학과",
            "personality": "재밌는 아이디어가 많은 사람!",
            "salary": "평균 연봉 약 4,000만~6,000만원 💡"
        },
        {
            "job": "🎵 작곡가",
            "major": "실용음악과",
            "personality": "감각적이고 자유로운 사람!",
            "salary": "성공 여부에 따라 다양 🎶"
        }
    ],

    "ISTJ": [
        {
            "job": "🏦 회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 책임감 강한 사람!",
            "salary": "평균 연봉 약 6,000만~1억원 💵"
        },
        {
            "job": "👮 경찰관",
            "major": "경찰행정학과",
            "personality": "원칙 중요하게 생각하는 사람!",
            "salary": "평균 연봉 약 4,000만~6,000만원 🚓"
        }
    ],

    "ISFJ": [
        {
            "job": "🏥 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 성실한 사람!",
            "salary": "평균 연봉 약 4,000만~6,000만원 💉"
        },
        {
            "job": "👶 유치원 교사",
            "major": "유아교육과",
            "personality": "따뜻하고 친절한 사람!",
            "salary": "평균 연봉 약 3,000만~5,000만원 🧸"
        }
    ],

    "ESTJ": [
        {
            "job": "📊 경영 관리자",
            "major": "경영학과",
            "personality": "체계적이고 리더십 있는 사람!",
            "salary": "평균 연봉 약 5,000만~8,000만원 📈"
        },
        {
            "job": "🏛️ 공무원",
            "major": "행정학과",
            "personality": "책임감 강하고 안정 추구하는 사람!",
            "salary": "평균 연봉 약 4,000만~7,000만원 🏢"
        }
    ],

    "ESFJ": [
        {
            "job": "💄 승무원",
            "major": "항공서비스학과",
            "personality": "친화력 좋고 밝은 사람!",
            "salary": "평균 연봉 약 4,000만~6,000만원 ✈️"
        },
        {
            "job": "🩺 의료 코디네이터",
            "major": "보건행정학과",
            "personality": "사람 도와주는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 3,500만~5,500만원 🏥"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 엔지니어",
            "major": "기계공학과",
            "personality": "손재주 좋고 문제 해결 좋아하는 사람!",
            "salary": "평균 연봉 약 5,000만~8,000만원 ⚙️"
        },
        {
            "job": "🚗 자동차 디자이너",
            "major": "산업디자인학과",
            "personality": "실용적이고 감각 있는 사람!",
            "salary": "평균 연봉 약 4,500만~7,000만원 🚘"
        }
    ],

    "ISFP": [
        {
            "job": "📸 사진작가",
            "major": "사진영상학과",
            "personality": "감각적이고 조용한 열정 있는 사람!",
            "salary": "경력에 따라 다양 📷"
        },
        {
            "job": "🎮 게임 그래픽 디자이너",
            "major": "게임디자인학과",
            "personality": "예술 감각 좋은 사람!",
            "salary": "평균 연봉 약 4,000만~6,500만원 🎨"
        }
    ],

    "ESTP": [
        {
            "job": "🏆 스포츠 선수",
            "major": "체육학과",
            "personality": "에너지 넘치고 활동적인 사람!",
            "salary": "종목과 실력에 따라 다양 ⚽"
        },
        {
            "job": "💼 영업 전문가",
            "major": "경영학과",
            "personality": "사람 만나는 거 좋아하는 사람!",
            "salary": "평균 연봉 약 4,000만~8,000만원 📞"
        }
    ],

    "ESFP": [
        {
            "job": "🎤 연예인",
            "major": "연극영화과",
            "personality": "끼 많고 사람 좋아하는 사람!",
            "salary": "인기에 따라 엄청 다양 🌟"
        },
        {
            "job": "🎉 이벤트 플래너",
            "major": "관광경영학과",
            "personality": "분위기 메이커 스타일!",
            "salary": "평균 연봉 약 3,500만~5,500만원 🎈"
        }
    ]
}

st.title("✨ MBTI 진로 추천기 🚀")
st.write("너의 MBTI에 딱 맞는 진로를 추천해줄게! 😎")

mbti_list = list(mbti_data.keys())

selected_mbti = st.selectbox(
    "👉 너의 MBTI를 골라봐!",
    mbti_list
)

if st.button("🔍 진로 추천 받기"):
    st.balloons()

    st.header(f"🎯 {selected_mbti} 추천 진로")

    careers = mbti_data[selected_mbti]

    for career in careers:
        st.subheader(career["job"])

        st.write(f"📚 추천 학과: {career['major']}")
        st.write(f"💖 잘 맞는 성격: {career['personality']}")
        st.write(f"💰 평균 연봉: {career['salary']}")

        st.markdown("---")

    st.success("✨ 미래의 멋진 너를 응원할게!! 화이팅 😆")
