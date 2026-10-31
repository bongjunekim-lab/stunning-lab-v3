import streamlit as st
import time
import random

# 자모 리스트
JAMOS = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ',
         'ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ']

# 한글 자모 분해 함수
CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

def decompose(char):
    code = ord(char) - 0xAC00
    if code < 0 or code > 11171:
        return [char]
    chosung = CHOSUNG_LIST[code // 588]
    jungsung = JUNGSUNG_LIST[(code % 588) // 28]
    jongsung = JONGSUNG_LIST[code % 28]
    return [chosung, jungsung] + ([jongsung] if jongsung else [])

# 페이지 설정
st.set_page_config(page_title="LEGO Hangeul Tetris", layout="wide")

# 스타일 정의
st.markdown("""
    <style>
    .char-box-yellow { font-size: 120px; color: #FFD43B; font-weight: bold; border: 6px solid #FFD43B; padding: 35px; border-radius: 15px; text-align: center; margin: 15px; }
    .char-box-blue { font-size: 120px; color: white; background-color: #228BE6; font-weight: bold; border: 6px solid #1c7ed6; padding: 35px; border-radius: 15px; text-align: center; margin: 15px; }
    .ing-brick { font-size: 80px; color: #228BE6; font-weight: bold; margin: 12px; }
    .lego-key { font-size: 100px; font-weight: bold; border: 6px solid #495057; border-radius: 12px; padding: 30px; margin: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = []
if 'completed_indices' not in st.session_state:
    st.session_state.completed_indices = set()
if 'current_target_idx' not in st.session_state:
    st.session_state.current_target_idx = 0

# 문장 입력
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 배경 문장 크게 표시
st.markdown(f"<h1 style='color:#FFD43B; text-align:center; font-size:140px;'>{target_sentence}</h1>", unsafe_allow_html=True)

# Word Assembly Line
cols = st.columns(len(target_sentence))
for idx, char in enumerate(target_sentence):
    with cols[idx]:
        if char == " ":
            st.write("␣")
            continue
        if idx in st.session_state.completed_indices:
            st.markdown(f"<div class='char-box-blue'>{char}</div>", unsafe_allow_html=True)
        elif idx == st.session_state.current_target_idx:
            st.markdown(f"<div class='char-box-yellow'>{char}</div>", unsafe_allow_html=True)
            if len(st.session_state.current_input) > 0:
                build_str = "".join([f"<span class='ing-brick'>{b}</span>" for b in st.session_state.current_input])
                st.markdown(build_str, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='char-box-yellow'>{char}</div>", unsafe_allow_html=True)

# 자동 매칭 (단어 단위 유지)
if len(st.session_state.current_input) > 0 and st.session_state.current_target_idx < len(target_sentence):
    current_target_char = target_sentence[st.session_state.current_target_idx]
    jamos = decompose(current_target_char)
    if st.session_state.current_input == jamos:
        st.session_state.completed_indices.add(st.session_state.current_target_idx)
        st.session_state.current_target_idx += 1
        st.session_state.current_input = []
        time.sleep(0.2)  # 0.2초 딜레이 후 파란색 변환
        st.rerun()
    elif len(st.session_state.current_input) > len(jamos):
        st.session_state.current_input = []  # 오입력 시 리셋
        st.rerun()

# 하단 자판: 단어 끝날 때까지 유지
st.write("---")
st.markdown("<h2 style='color:#228BE6; font-size:80px;'>⌨️ LEGO Brick Keyboard</h2>", unsafe_allow_html=True)

if st.session_state.current_target_idx < len(target_sentence):
    # 현재 단어 전체 자모 모으기
    word = ""
    for idx in range(st.session_state.current_target_idx, len(target_sentence)):
        if target_sentence[idx] == " ":
            break
        word += target_sentence[idx]
    # 단어 전체 자모 분해
    word_jamos = []
    for ch in word:
        word_jamos.extend(decompose(ch))
else:
    word_jamos = []

# 후보 자모 8개 (정답 + 랜덤)
candidates = word_jamos + random.sample(JAMOS, max(0, 8 - len(word_jamos)))
random.shuffle(candidates)

cols = st.columns(8)
for i, key in enumerate(candidates):
    with cols[i]:
        if st.button(key, key=f"btn_{i}", use_container_width=True):
            st.session_state.current_input.append(key)
            # 현재 글자 자모 확인
            current_target_char = target_sentence[st.session_state.current_target_idx]
            correct_jamos = decompose(current_target_char)
            if st.session_state.current_input == correct_jamos:
                st.session_state.completed_indices.add(st.session_state.current_target_idx)
                st.session_state.current_target_idx += 1
                st.session_state.current_input = []
                time.sleep(0.2)
                st.rerun()
            elif len(st.session_state.current_input) > len(correct_jamos):
                st.session_state.current_input = []  # 오입력 시 리셋
                st.rerun()

# Reset 버튼
if st.button("Reset 🔄"):
    st.session_state.current_input = []
    st.session_state.completed_indices = set()
    st.session_state.current_target_idx = 0
    st.rerun()
