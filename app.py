import streamlit as st

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(page_title="LEGO Hangeul Tetris", page_icon="🧱", layout="centered")

st.markdown("""
    <style>
    .lego-title { text-align: center; color: #FFD43B; font-size: 40px; font-weight: bold; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px #000; }
    .mission-box { background-color: #f1f3f5; border-radius: 15px; padding: 20px; text-align: center; border: 3px dashed #FFD43B; margin-bottom: 20px; }
    
    /* 실제 레고 조립판 영역 디자인 */
    .slot-container { 
        background-color: #343a40; 
        border-radius: 15px; 
        padding: 40px 20px; 
        text-align: center; 
        min-height: 180px; 
        margin-bottom: 25px; 
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.6); 
    }
    
    /* 문장 정렬 컨테이너 */
    .sentence-box {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        align-items: center;
    }
    
    /* 기본 가이드 상태인 노란색 레고 글자 블록 스타일 */
    .lego-char-guide {
        color: #FFD43B;
        font-size: 34px;
        font-weight: bold;
        padding: 10px 20px;
        border: 2px solid #FFD43B;
        border-radius: 8px;
        background-color: transparent;
        text-shadow: 1px 1px #000;
        transition: all 0.3s ease;
    }
    
    /* 하단 버튼 클릭 시 위로 발사되어 파란색으로 착 채워진 상태의 스타일 */
    .lego-char-filled {
        color: white;
        background-color: #228BE6;
        border: 2px solid #1c7ed6;
        box-shadow: 0px 4px #1864ab;
        transform: translateY(-5px);
    }
    
    /* 띄어쓰기(스페이스) 블록 스타일 */
    .lego-space-block {
        width: 30px;
        height: 50px;
        border: 2px dashed #555;
        border-radius: 6px;
        background-color: rgba(255,255,255,0.05);
    }
    
    /* 실제 채워진 띄어쓰기 블록 스타일 */
    .lego-space-filled {
        border: 2px solid #228BE6;
        background-color: rgba(34, 139, 230, 0.2);
    }
    
    .success-banner { background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb; border-radius: 10px; padding: 15px; text-align: center; font-size: 22px; font-weight: bold; margin-top: 15px; }
    .admin-box { background-color: #e8f4fd; border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid #74c0fc; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='lego-title'>🧱 LEGO HANGEUL REVERSE TETRIS</div>", unsafe_allow_html=True)
st.write("---")

# 2. 게임 내부 상태 저장소 초기화
if 'bricks' not in st.session_state:
    st.session_state.bricks = []
if 'unlocked_chars' not in st.session_state:
    st.session_state.unlocked_chars = set()
if 'space_count' not in st.session_state:
    st.session_state.space_count = 0

# 🛠️ Developer Sandbox (화면 테스트용 문장 입력창)
st.markdown("<div class='admin-box'>🛠️ <b>Developer Sandbox</b> (화면상 작동 테스트용 문장 설정)</div>", unsafe_allow_html=True)
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 3. 미국인을 위한 사운드 및 미션 가이드 문구
st.markdown(f"""
    <div class='mission-box'>
        <h3>🎵 Mission Sound: "Interactive Mode"</h3>
        <p style='font-size:18px; color:#495057;'>Target Sentence (Guide): <b>{target_sentence}</b></p>
    </div>
""", unsafe_allow_html=True)

# 4. 상단: 아래에서 위로 쌓이는 레고 조립판 시각화
st.write("### 🏗️ Upward LEGO Assembly Board (상단 조립판)")
st.markdown("<div class='slot-container'><div class='sentence-box'>", unsafe_allow_html=True)

# 문장을 공백 기준으로 쪼개서 인덱싱하여 스페이스바 작동 구현
space_idx = 0
for char in target_sentence:
    if char == " ": # 띄어쓰기 공간 처리
        space_idx += 1
        # 스페이스바를 누른 횟수가 이 공백의 위치에 도달하면 파란색으로 활성화
        if st.session_state.space_count >= space_idx:
            st.markdown("<div class='lego-space-block lego-space-filled'></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='lego-space-block'></div>", unsafe_allow_html=True)
        continue
        
    if char in st.session_state.unlocked_chars:
        st.markdown(f"<div class='lego-char-guide lego-char-filled'>{char}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='lego-char-guide'>{char}</div>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# 5. 한글 오토마타 조립 판정 로직
if len(st.session_state.bricks) > 0:
    if st.session_state.bricks == ['ㄴ', 'ㅏ']:
        st.session_state.unlocked_chars.add("나")
        st.markdown("<div class='success-banner'>🎵 딸깍! (CLICK!) LEGO 'ㄴ' + 'ㅏ' ➡️ 【 나 】 완성! ✨</div>", unsafe_allow_html=True)
        st.session_state.bricks = []
    elif st.session_state.bricks == ['ㄴ', 'ㅡ', 'ㄴ']:
        st.session_state.unlocked_chars.add("는")
        st.markdown("<div class='success-banner'>🎵 딸깍! (CLICK!) LEGO 'ㄴ' + 'ㅡ' + 'ㄴ' ➡️ 【 는 】 완성! ✨</div>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.bricks = []
    elif len(st.session_state.bricks) >= 3:
        st.session_state.bricks = []

# 6. 하단: 자모음 보관소 + 🌟 스페이스 바 자판 추가
st.write("### ⌨️ LEGO Brick Keyboard (하단 자판)")

# 상단 자모음 버튼 레이아웃
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🔵 ㄴ (Shoot!)", key="btn_n", use_container_width=True):
        st.session_state.bricks.append("ㄴ")
        st.rerun()
with col2:
    if st.button("🔴 ㅡ (Shoot!)", key="btn_eu", use_container_width=True):
        st.session_state.bricks.append("ㅡ")
        st.rerun()
with col3:
    if st.button("🔵 ㄹ (Shoot!)", key="btn_r", use_container_width=True):
        st.session_state.bricks.append("ㄹ")
        st.rerun()
with col4:
    if st.button("🔴 ㅏ (Shoot!)", key="btn_a", use_container_width=True):
        st.session_state.bricks.append("ㅏ")
        st.rerun()
with col5:
    if st.button("🟡 Reset 🔄", key="btn_reset", use_container_width=True):
        st.session_state.bricks = []
        st.session_state.unlocked_chars = set()
        st.session_state.space_count = 0
        st.rerun()

# 🌟 하단에 길쭉한 스페이스바 버튼 배치
st.write("")
if st.button("⌨️ Space Bar (간격 띄우기) ───", key="btn_space", use_container_width=True):
    st.session_state.space_count += 1
    st.rerun()
