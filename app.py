import streamlit as st

# 초성, 중성, 종성 리스트
CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

def decompose(char):
    """한글 글자를 자모로 분해"""
    code = ord(char) - 0xAC00
    if code < 0 or code > 11171:
        return [char]  # 한글이 아니면 그대로 반환
    chosung = CHOSUNG_LIST[code // 588]
    jungsung = JUNGSUNG_LIST[(code % 588) // 28]
    jongsung = JONGSUNG_LIST[code % 28]
    return [chosung, jungsung] + ([jongsung] if jongsung else [])

# 페이지 설정
st.set_page_config(page_title="LEGO Hangeul Tetris", page_icon="🧱", layout="wide")

# 세션 상태 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = []
if 'completed_indices' not in st.session_state:
    st.session_state.completed_indices = set()
if 'current_target_idx' not in st.session_state:
    st.session_state.current_target_idx = 0

# 문장 입력
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 상단 배경 문장
st.markdown(f"### 배경 문장: {target_sentence}")

# Word Assembly Line
cols = st.columns(len(target_sentence) + 2)
for idx, char in enumerate(target_sentence):
    with cols[idx]:
        if char == " ":
            if st.session_state.current_target_idx == idx:
                st.session_state.current_target_idx += 1
                st.rerun()
            st.write("␣")
            continue
        if idx in st.session_state.completed_indices:
            st.write(f"✅ {char}")
        elif idx == st.session_state.current_target_idx:
            if len(st.session_state.current_input) > 0:
                st.write("".join(st.session_state.current_input))
            else:
                st.write(f"👉 {char}")
        else:
            st.write(char)

# 자동 매칭
if len(st.session_state.current_input) > 0:
    current_target_char = target_sentence[st.session_state.current_target_idx]
    jamos = decompose(current_target_char)
    if st.session_state.current_input == jamos:
        st.session_state.completed_indices.add(st.session_state.current_target_idx)
        st.session_state.current_target_idx += 1
        st.session_state.current_input = []
        st.balloons()
        st.rerun()
    elif len(st.session_state.current_input) >= 4:
        st.session_state.current_input = []
        st.rerun()

# 하단 자판: 현재 글자 자모 자동 표시
st.write("---")
st.write("### ⌨️ LEGO Brick Keyboard")

current_target_char = target_sentence[st.session_state.current_target_idx]
available_keys = decompose(current_target_char)

cols = st.columns(len(available_keys) + 2)
for i, key in enumerate(available_keys):
    with cols[i]:
        if st.button(key, key=f"btn_{key}", use_container_width=True):
            st.session_state.current_input.append(key)
            st.rerun()

# Reset 버튼
with cols[-2]:
    if st.button("Reset 🔄", key="btn_reset", use_container_width=True):
        st.session_state.current_input = []
        st.session_state.completed_indices = set()
        st.session_state.current_target_idx = 0
        st.rerun()

# Space Bar 버튼
with cols[-1]:
    if st.button("Space ␣", key="btn_space", use_container_width=True):
        if target_sentence[st.session_state.current_target_idx] == " ":
            st.session_state.current_target_idx += 1
        st.rerun()
