import streamlit as st

# 페이지 설정
st.set_page_config(page_title="LEGO Hangeul Tetris", page_icon="🧱", layout="wide")

# 스타일 정의
st.markdown("""
    <style>
    .lego-title { text-align: center; color: #FFD43B; font-size: 40px; font-weight: bold; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px #000; }
    .mission-box { background-color: #f1f3f5; border-radius: 15px; padding: 20px; text-align: center; border: 3px dashed #FFD43B; margin-bottom: 20px; }
    .black-board { background-color: #212529; border-radius: 15px; min-height: 180px; margin-bottom: 30px; box-shadow: inset 0px 0px 20px rgba(0,0,0,0.8); }
    .char-box-yellow { color: #FFD43B; font-size: 36px; font-weight: bold; font-family: 'Malgun Gothic', sans-serif; padding: 12px 22px; border: 2px solid #FFD43B; border-radius: 8px; background-color: transparent; text-shadow: 1px 1px #000; min-width: 75px; text-align: center; }
    .char-box-target { border: 3px solid #ff922b !important; background-color: rgba(255, 146, 43, 0.1) !important; box-shadow: 0px 0px 12px #ff922b; }
    .char-box-blue { color: white !important; background-color: #228BE6 !important; border: 2px solid #1c7ed6 !important; box-shadow: 0px 4px #1864ab; text-shadow: none; }
    .ing-brick { color: #228BE6; font-size: 34px; font-weight: bold; }
    .space-dash { width: 35px; height: 50px; border: 2px dashed #495057; border-radius: 6px; margin: auto; }
    .space-blue { border: 2px solid #228BE6; background-color: rgba(34, 139, 230, 0.2); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='lego-title'>🧱 LEGO HANGEUL REVERSE TETRIS</div>", unsafe_allow_html=True)
st.write("---")

# 세션 상태 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = []
if 'completed_indices' not in st.session_state:
    st.session_state.completed_indices = set()
if 'current_target_idx' not in st.session_state:
    st.session_state.current_target_idx = 0

# 개발자 샌드박스
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 상단 레이아웃
st.markdown(f"""
    <div class='mission-box'>
        <h3>🎵 Mission Sound: "I love you."</h3>
        <p style='font-size:18px; color:#495057;'>Target Sentence: <b>{target_sentence}</b></p>
    </div>
""", unsafe_allow_html=True)

st.write("### 🏗️ Upward LEGO Assembly Board (상단 조립판)")
st.markdown("<div class='black-board'></div>", unsafe_allow_html=True)

st.write("### 🔤 Word Assembly Line (가로형 조립 라인)")
cols = st.columns(len(target_sentence) + 2)

for idx, char in enumerate(target_sentence):
    with cols[idx]:
        if char == " ":
            if st.session_state.current_target_idx == idx:
                st.session_state.current_target_idx += 1
                st.rerun()
            if idx < st.session_state.current_target_idx:
                st.markdown("<div class='space-dash space-blue'></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='space-dash'></div>", unsafe_allow_html=True)
            continue
        if idx in st.session_state.completed_indices:
            st.markdown(f"<div class='char-box-yellow char-box-blue'>{char}</div>", unsafe_allow_html=True)
        elif idx == st.session_state.current_target_idx:
            if len(st.session_state.current_input) > 0:
                build_str = "".join([f"<span class='ing-brick'>{b}</span>" for b in st.session_state.current_input])
                st.markdown(f"<div class='char-box-yellow char-box-target'>{build_str}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='char-box-yellow char-box-target'>{char}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='char-box-yellow'>{char}</div>", unsafe_allow_html=True)

# 자동 매칭 규칙
match_rules = {
    "나": ['ㄴ', 'ㅏ'],
    "는": ['ㄴ', 'ㅡ', 'ㄴ'],
    "너": ['ㄴ', 'ㅓ'],
    "를": ['ㄹ', 'ㅡ', 'ㄹ'],
    "사": ['ㅅ', 'ㅏ'],
    "랑": ['ㄹ', 'ㅏ', 'ㅇ'],
    "해": ['ㅎ', 'ㅐ'],
}

if len(st.session_state.current_input) > 0:
    current_target_char = target_sentence[st.session_state.current_target_idx]
    if current_target_char in match_rules and st.session_state.current_input == match_rules[current_target_char]:
        st.session_state.completed_indices.add(st.session_state.current_target_idx)
        st.session_state.current_target_idx += 1
        st.session_state.current_input = []
        st.balloons()
        st.rerun()
    elif len(st.session_state.current_input) >= 3:
        st.session_state.current_input = []
        st.rerun()

# 하단 자판: 현재 타겟 글자에 맞게 자동 변경
st.write("---")
st.write("### ⌨️ LEGO Brick Keyboard (하단 자판)")

current_target_char = target_sentence[st.session_state.current_target_idx]
available_keys = match_rules.get(current_target_char, [])

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
    if st.button("⌨️ Space Bar (간격 띄우기)", key="btn_space", use_container_width=True):
        if target_sentence[st.session_state.current_target_idx] == " ":
            st.session_state.current_target_idx += 1
        st.rerun()
