import streamlit as st
import time

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
st.set_page_config(page_title="두벌식 LEGO Keyboard", layout="wide")

# 세션 상태 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = []
if 'completed_indices' not in st.session_state:
    st.session_state.completed_indices = set()
if 'current_target_idx' not in st.session_state:
    st.session_state.current_target_idx = 0
if 'last_sentence' not in st.session_state:
    st.session_state.last_sentence = ""

# 문장 입력
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 새로운 문장이 입력되면 상태 초기화
if st.session_state.last_sentence != target_sentence:
    st.session_state.current_input = []
    st.session_state.completed_indices = set()
    st.session_state.current_target_idx = 0
    st.session_state.last_sentence = target_sentence

# 문장 표시 + 자모 분해
cols = st.columns(len(target_sentence))
for idx, char in enumerate(target_sentence):
    with cols[idx]:
        # 마지막 음절은 1.5배 크기
        if idx == len(target_sentence)-1:
            st.markdown(f"<div style='font-size:180px; color:#FFD43B; text-align:center;'>{char}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:120px; color:#FFD43B; text-align:center;'>{char}</div>", unsafe_allow_html=True)

        # 자모 분해 표시 (빈 공간 유지)
        jamos = decompose(char)
        if jamos:
            st.markdown("<div style='font-size:60px; color:#228BE6; text-align:center;'>"
                        + " + ".join(jamos) + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:60px; color:#868e96; text-align:center;'>아직 입력 없음</div>", unsafe_allow_html=True)

# 두벌식 자판 배열
row1_keys = ['ㅂ','ㅈ','ㄷ','ㄱ','ㅅ','ㅛ','ㅕ','ㅑ']
row2_keys = ['ㅁ','ㄴ','ㅇ','ㄹ','ㅎ','ㅗ','ㅓ','ㅏ','ㅣ']
row3_keys = ['ㅋ','ㅌ','ㅊ','ㅍ','ㅠ','ㅜ','ㅡ']

st.write("---")
st.markdown("<h2 style='color:#228BE6; font-size:100px;'>⌨️ 두벌식 LEGO Keyboard</h2>", unsafe_allow_html=True)

# 윗줄
row1 = st.columns(len(row1_keys))
for i, key in enumerate(row1_keys):
    with row1[i]:
        if st.button(key, key=f"row1_{i}", use_container_width=True):
            st.session_state.current_input.append(key)
            st.rerun()

# 중간줄
row2 = st.columns(len(row2_keys))
for i, key in enumerate(row2_keys):
    with row2[i]:
        if st.button(key, key=f"row2_{i}", use_container_width=True):
            st.session_state.current_input.append(key)
            st.rerun()

# 아랫줄
row3 = st.columns(len(row3_keys))
for i, key in enumerate(row3_keys):
    with row3[i]:
        if st.button(key, key=f"row3_{i}", use_container_width=True):
            st.session_state.current_input.append(key)
            st.rerun()

# Backspace, Reset, Space 버튼
col_backspace, col_reset, col_space = st.columns(3)

with col_backspace:
    if st.button("Backspace ⌫"):
        if len(st.session_state.current_input) > 0:
            st.session_state.current_input.pop()
        st.rerun()

with col_reset:
    if st.button("Reset 🔄"):
        st.session_state.current_input = []
        st.session_state.completed_indices = set()
        st.session_state.current_target_idx = 0
        st.rerun()

with col_space:
    if st.button("Space ␣"):
        if st.session_state.current_target_idx < len(target_sentence) and target_sentence[st.session_state.current_target_idx] == " ":
            st.session_state.current_target_idx += 1
        st.rerun()
