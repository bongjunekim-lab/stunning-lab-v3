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
        padding: 30px; 
        text-align: center; 
        min-height: 250px; 
        margin-bottom: 25px; 
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.6); 
    }
    .guide-text { color: #FFD43B; font-size: 32px; letter-spacing: 5px; font-weight: bold; margin-bottom: 20px; text-shadow: 1px 1px #000; }
    
    /* 발사되어 올라온 브릭 레이어 스타일 */
    .brick-layer { 
        border-radius: 8px; 
        margin: 6px auto; 
        padding: 12px; 
        width: 50%; 
        font-weight: bold; 
        font-size: 24px; 
        text-align: center; 
        box-shadow: 0px 5px #00000033;
    }
    
    .success-banner { background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb; border-radius: 10px; padding: 15px; text-align: center; font-size: 22px; font-weight: bold; margin-top: 15px; }
    
    /* 관리자 입력창 스타일 설정 */
    .admin-box { background-color: #e8f4fd; border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid #74c0fc; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='lego-title'>🧱 LEGO HANGEUL REVERSE TETRIS</div>", unsafe_allow_html=True)
st.write("---")

# 2. 게임 내부 저장소(데이터 세션) 초기화
if 'bricks' not in st.session_state:
    st.session_state.bricks = []

# 🌟 [추가 기능] 배경 속 가이드 문구 관리자 입력 시스템
st.markdown("<div class='admin-box'>🛠️ <b>Developer Sandbox</b> (화면상 작동 테스트용 문장 설정)</div>", unsafe_allow_html=True)
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 3. 미국인을 위한 사운드 및 미션 가이드 문구 (사용자가 입력한 문장이 실시간 반영됨)
st.markdown(f"""
    <div class='mission-box'>
        <h3>🎵 Mission Sound: "Interactive Mode"</h3>
        <p style='font-size:18px; color:#495057;'>Target Sentence (Guide): <b>{target_sentence}</b></p>
    </div>
""", unsafe_allow_html=True)

# 4. 상단: 아래에서 위로 쌓이는 레고 조립판 시각화
st.write("### 🏗️ Upward LEGO Assembly Board (상단 조립판)")
st.markdown("<div class='slot-container'>", unsafe_allow_html=True)

# 사용자가 입력한 텍스트가 조립판 배경 속에 노란색 가이드 글씨로 실시간 표기됨
st.markdown(f"<div class='guide-text'>{target_sentence}</div>", unsafe_allow_html=True)

# 블록이 3층 -> 2층 -> 1층 순서로 위로 쌓이게 출력 (요청하신 빈 칸 제거 버전 유지)
if len(st.session_state.bricks) >= 3:
    st.markdown(f"<div class='brick-layer' style='background-color:#FCC419; color:black;'>[3층 / 받침] 🧱 {st.session_state.bricks}</div>", unsafe_allow_html=True)

if len(st.session_state.bricks) >= 2:
    st.markdown(f"<div class='brick-layer' style='background-color:#FA5252; color:white;'>[2층 / 모음] 🧱 {st.session_state.bricks}</div>", unsafe_allow_html=True)

if len(st.session_state.bricks) >= 1:
    st.markdown(f"<div class='brick-layer' style='background-color:#228BE6; color:white;'>[1st Floor / 첫자음] 🧱 {st.session_state.bricks}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 5. 한글 오토마타(조합) 판정 시스템
if len(st.session_state.bricks) == 3:
    if st.session_state.bricks == ['ㄴ', 'ㅡ', 'ㄴ']:
        st.markdown("<div class='success-banner'>🎵 딸깍! (CLICK!) LEGO Assembled: 【 는 】 ✨</div>", unsafe_allow_html=True)
        st.balloons()
    else:
        combined = "".join(st.session_state.bricks)
        st.markdown(f"<div class='success-banner'>🎵 딸깍! (CLICK!) LEGO Assembled: 【 {combined} 】 ✨</div>", unsafe_allow_html=True)
    st.session_state.bricks = [] # 완성 후 초기화

# 6. 하단: 자모음 보관소 (키보드 앤 슈팅 시스템)
st.write("### ⌨️ LEGO Brick Keyboard (하단 자판)")
st.info("Click the buttons below in order to shoot bricks upward! (Try: ㄴ ➡️ ㅡ ➡️ ㄴ)")

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
        st.rerun()
