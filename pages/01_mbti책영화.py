import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="✨ MBTI 책 & 영화 추천 🎬📚",
    page_icon="🌟",
    layout="centered"
)

# 제목
st.title("🌈 MBTI별 책 & 영화 추천 서비스 🎥📖")
st.markdown("### 😎 너의 MBTI에 딱 맞는 감성 작품을 추천해줄게!")
st.write("취향 저격 받을 준비됐지? 🎯")

# MBTI 데이터
mbti_data = {
    "INTJ": {
        "books": [
            {
                "title": "1984",
                "author": "조지 오웰",
                "year": "1900년대 📚",
                "desc": "통찰력 강한 INTJ에게 딱 맞는 디스토피아 명작 😎"
            },
            {
                "title": "아몬드",
                "author": "손원평",
                "year": "2000년대 이후 ✨",
                "desc": "감정과 인간관계를 깊게 생각하게 만드는 책 💭"
            }
        ],
        "movies": [
            {
                "title": "포레스트 검프",
                "year": "1994 🇺🇸",
                "desc": "인생의 의미를 생각하게 하는 감동 영화 🏃"
            },
            {
                "title": "쇼생크 탈출",
                "year": "1994 🇺🇸",
                "desc": "끈기와 전략을 좋아하는 INTJ 취향 저격 🔥"
            }
        ]
    },

    "INFP": {
        "books": [
            {
                "title": "데미안",
                "author": "헤르만 헤세",
                "year": "1900년대 📚",
                "desc": "자아를 찾아가는 감성 폭발 성장소설 🌙"
            },
            {
                "title": "불편한 편의점",
                "author": "김호연",
                "year": "2000년대 이후 ✨",
                "desc": "따뜻한 위로가 필요한 날 읽기 좋은 책 ☕"
            }
        ],
        "movies": [
            {
                "title": "타이타닉",
                "year": "1997 🇺🇸",
                "desc": "감성 충만 로맨스와 감동 💖"
            },
            {
                "title": "죽은 시인의 사회",
                "year": "1989 🇺🇸",
                "desc": "꿈과 자유를 사랑하는 INFP에게 추천 🍃"
            }
        ]
    },

    "ENFP": {
        "books": [
            {
                "title": "어린 왕자",
                "author": "생텍쥐페리",
                "year": "1900년대 📚",
                "desc": "상상력 가득한 감성 명작 🦊"
            },
            {
                "title": "달러구트 꿈 백화점",
                "author": "이미예",
                "year": "2000년대 이후 ✨",
                "desc": "꿈과 판타지를 좋아하는 ENFP에게 딱 🌈"
            }
        ],
        "movies": [
            {
                "title": "라라랜드",
                "year": "2016 🇺🇸",
                "desc": "열정과 낭만 가득한 영화 🎹"
            },
            {
                "title": "백 투 더 퓨처",
                "year": "1985 🇺🇸",
                "desc": "모험심 강한 ENFP에게 추천 🚀"
            }
        ]
    },

    "ISTJ": {
        "books": [
            {
                "title": "노인과 바다",
                "author": "어니스트 헤밍웨이",
                "year": "1900년대 📚",
                "desc": "끈기와 책임감을 보여주는 명작 🎣"
            },
            {
                "title": "세이노의 가르침",
                "author": "세이노",
                "year": "2000년대 이후 ✨",
                "desc": "현실적이고 목표지향적인 사람에게 추천 💪"
            }
        ],
        "movies": [
            {
                "title": "라이언 일병 구하기",
                "year": "1998 🇺🇸",
                "desc": "책임감과 팀워크가 돋보이는 영화 🎖️"
            },
            {
                "title": "머니볼",
                "year": "2011 🇺🇸",
                "desc": "논리와 전략을 좋아한다면 강추 ⚾"
            }
        ]
    }
}

# 나머지 MBTI 자동 채우기
default_data = {
    "books": [
        {
            "title": "위대한 개츠비",
            "author": "F. 스콧 피츠제럴드",
            "year": "1900년대 📚",
            "desc": "인간의 욕망과 꿈을 다룬 고전 명작 ✨"
        },
        {
            "title": "아주 작은 습관의 힘",
            "author": "제임스 클리어",
            "year": "2000년대 이후 ✨",
            "desc": "자기계발 좋아하는 사람들에게 인기 👍"
        }
    ],
    "movies": [
        {
            "title": "인터스텔라",
            "year": "2014 🇺🇸",
            "desc": "몰입감 최고인 SF 영화 🚀"
        },
        {
            "title": "어벤져스",
            "year": "2012 🇺🇸",
            "desc": "팀플과 액션 좋아하면 무조건 😆"
        }
    ]
}

all_mbti = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

for mbti in all_mbti:
    if mbti not in mbti_data:
        mbti_data[mbti] = default_data

# MBTI 선택
selected_mbti = st.selectbox(
    "🧠 너의 MBTI를 골라줘!",
    all_mbti
)

# 결과 출력
if selected_mbti:
    data = mbti_data[selected_mbti]

    st.success(f"🎉 {selected_mbti} 유형 추천 결과야!")

    st.markdown("---")

    # 책 추천
    st.header("📚 추천 책 2권")

    for book in data["books"]:
        st.subheader(f"✨ {book['title']}")
        st.write(f"👨‍💻 작가: {book['author']}")
        st.write(f"🕰️ 시대: {book['year']}")
        st.write(f"💡 추천 이유: {book['desc']}")
        st.markdown("")

    st.markdown("---")

    # 영화 추천
    st.header("🎬 추천 영화 2편")

    for movie in data["movies"]:
        st.subheader(f"🍿 {movie['title']}")
        st.write(f"📅 개봉: {movie['year']}")
        st.write(f"🔥 추천 이유: {movie['desc']}")
        st.markdown("")

    st.balloons()

# 하단 문구
st.markdown("---")
st.caption("🌟 오늘의 작품 추천 완료! 재밌게 감상해봐 😆")
