import streamlit as st

# 1. 페이지 기본 설정 및 요청하신 화면 정렬(비어있는 검은 보드 + 아래 가로형 문자 결합 기믹) 정의
st.set_page_config(page_title="LEGO Hangeul Tetris", page_icon="🧱", layout="centered")

st.markdown("""
    <style>
    .lego-title { text-align: center; color: #FFD43B; font-size: 40px; font-weight: bold; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px #000; }
    .mission-box { background-color: #f1f3f5; border-radius: 15px; padding: 20px; text-align: center; border: 3px dashed #FFD43B; margin-bottom: 20px; }
    
    /* 1. 상단 블랙 보드 영역 (요청대로 내부를 완전히 비우고 깔끔하게 세팅) */
    .black-board { 
        background-color: #212529; 
        border-radius: 15px; 
        min-height: 180px; 
        margin-bottom: 30px; 
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.8); 
    }
    
    /* 2. 그 아래 가로형 문장 조립 구역 */
    .assembly-zone {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        align-items: center;
        margin-bottom: 35px;
        padding: 10px;
    }
    
    /* 기본 가이드 상태: 노란색 가로형 폰트 블록 */
    .char-box-yellow {
        color: #FFD43B;
        font-size: 36px;
        font-weight: bold;
        font-family: 'Malgun Gothic', sans-serif;
        padding: 12px 22px;
        border: 2px solid #FFD43B;
        border-radius: 8px;
        background-color: transparent;
        text-shadow: 1px 1px #000;
        min-width: 75px;
        text-align: center;
        display: flex;
        flex-direction: row; /* 자모음이 무조건 가로로 배치되도록 강제 */
        justify-content: center;
        gap: 4px;
    }
    
    /* 자판을 조작하여 정답 글자가 완성되었을 때: 파란색 폰트 및 배경으로 진화 */
    .char-box-blue {
        color: white !important;
        background-color: #228BE6 !important;
        border: 2px solid #1c7ed6 !important;
        box-shadow: 0px 4px #1864ab;
        text-shadow: none;
    }
    
    /* 조립 도중 실시간으로 꽂히는 파란색 작은 자모음 브릭 스타일 */
    .ing-brick {
        color: #228BE6;
        font-size: 34px;
        font-weight: bold;
    }
    
    /* 스페이스바 공간 스타일 */
    .space-dash { width: 25px; height: 50px; border: 2px dashed #495057; border-radius: 6px; }
    .space-blue { border: 2px solid #228BE6; background-color: rgba(34, 139, 230, 0.2); }
    
    .success-banner { background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb; border-radius: 10px; padding: 15px; text-align: center; font-size: 22px; font-weight: bold; margin-top: 15px; }
    .admin-box { background-color: #e8f4fd; border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid #74c0fc; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='lego-title'>🧱 LEGO HANGEUL REVERSE TETRIS</div>", unsafe_allow_html=True)
st.write("---")

# 2. 게임 내부 상태 데이터 저장소 세션 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = []
if 'completed_words' not in st.session_state:
    st.session_state.completed_words = set()
if 'spaces' not in st.session_state:
    st.session_state.spaces = 0

# 🛠️ Developer Sandbox (화면 테스트용 문장 설정창)
st.markdown("<div class='admin-box'>🛠️ <b>Developer Sandbox</b> (가로형 자모음 조립 및 블루 체인지 테스트)</div>", unsafe_allow_html=True)
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 3. 상단 가이드 레이아웃
st.markdown(f"""
    <div class='mission-box'>
        <h3>🎵 Mission Sound: "I love you."</h3>
        <p style='font-size:18px; color:#495057;'>Target Sentence: <b>{target_sentence}</b></p>
    </div>
""", unsafe_allow_html=True)

# 4. [요청 사항 ①] 상단 Upward LEGO Assembly Board (완전히 비워둔 검은색 상자)
st.write("### 🏗️ Upward LEGO Assembly Board (상단 조립판)")
st.markdown("<div class='black-board'></div>", unsafe_allow_html=True)

# 5. [요청 사항 ②] 그 아래 배치되는 가로형 노란색 폰트 문장 및 파란색 실시간 결합 존
st.write("### 🔤 Word Assembly Line (가로형 조립 라인)")
st.markdown("<div class='assembly-zone'>", unsafe_allow_html=True)

space_idx = 0
for char in target_sentence:
    if char == " ": # 띄어쓰기 처리
        space_idx += 1
        if st.session_state.spaces >= space_idx:
            st.markdown("<div class='space-dash space-blue'></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='space-dash'></div>", unsafe_allow_html=True)
        continue
        
    # 글자가 완성되었다면 통째로 파란색 박스로 변경
    if char in st.session_state.completed_words:
        st.markdown(f"<div class='char-box-yellow char-box-blue'>{char}</div>", unsafe_allow_html=True)
    else:
        # 현재 조립 중인 첫 글자가 '나'일 때 실시간 자모음 매칭 연출
        if char == "나" and len(st.session_state.current_input) > 0:
            build_str = ""
            for b in st.session_state.current_input:
                build_str += f"<span class='ing-brick'>{b}</span>"
            st.markdown(f"<div class='char-box-yellow'>{build_str}</div>", unsafe_allow_html=True)
        else:
            # 아직 건드리지 않은 기본 상태는 원래 기획하신 노란색 폰트로 유지
            st.markdown(f"<div class='char-box-yellow'>{char}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 6. 실시간 가로 결합 및 블루 체인지 판정 시스템
if len(st.session_state.current_input) > 0:
    # 하단 자판 터치 시 가로 배열 순서에 따라 처리
    if st.session_state.current_input == ['ㄴ', 'ㅏ']:
        st.session_state.completed_words.add("나")
        st.markdown("<div class='success-banner'>🎵 딸깍! 가로 결합 완료! 노란색 '나' ➡️ <b>【 파란색 나 】</b>로 폰트가 변경되었습니다! ✨</div>", unsafe_allow_html=True)
        st.session_state.current_input = []
        st.rerun()
    elif st.session_state.current_input == ['ㄴ', 'ㅡ', 'ㄴ']:
        st.session_state.completed_words.add("는")
        st.markdown("<div class='success-banner'>🎵 딸깍! 가로 결합 완료! 노란색 '는' ➡️ <b>【 파란색 는 】</b>로 폰트가 변경되었습니다! ✨</div>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.current_input = []
        st.rerun()
    elif len(st.session_state.current_input) >= 3:
        # 매칭이 안 된 잘못된 순서일 경우 리셋
        st.session_state.current_input = []
        st.rerun()

# 7. 하단 자판 영역
st.write("### ⌨️ LEGO Brick Keyboard (하단 자판)")
st.info("💡 <b>블루 체인지 구동 테스트 방법</b><br>1. 아래 자판에서 <b>🔵 ㄴ</b> 클릭 (노란색 '나' 자리에 파란색 'ㄴ'이 가로로 안착)<br>2. 곧바로 <b>🔴 ㅏ</b> 클릭 (파란색 'ㅏ'가 가로로 결합하며 글자가 통째로 <b>파란색 【 나 】</b>로 진화!)", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🔵 ㄴ", key="btn_n", use_container_width=True):
        st.session_state.current_input.append("ㄴ")
        st.rerun()
with col2:
    if st.button("🔴 ㅡ", key="btn_eu", use_container_width=True):
        st.session_state.current_input.append("ㅡ")
        st.rerun()
with col3:
    if st.button("🔵 ㄹ", key="btn_r", use_container_width=True):
        st.session_state.current_input.append("ㄹ")
        st.rerun()
with col4:
    if st.button("🔴 ㅏ", key="btn_a", use_container_width=True):
        st.session_state.current_input.append("ㅏ")
        st.rerun()
with col5:
    if st.button("🟡 Reset 🔄", key="btn_reset", use_container_width=True):
        st.session_state.current_input = []
        st.session_state.completed_words = set()
        st.session_state.spaces = 0
        st.rerun()

st.write("")
if st.button("⌨️ Space Bar (간격 띄우기) ───", key="btn_space", use_container_width=True):
    st.session_state.spaces += 1
    st.rerun()
