import streamlit as st

# 1. 페이지를 가로가 넓은 와이드 모드로 고정합니다.
st.set_page_config(page_title="LEGO Hangeul Tetris", page_icon="🧱", layout="wide")

st.markdown("""
    <style>
    .lego-title { text-align: center; color: #FFD43B; font-size: 40px; font-weight: bold; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px #000; }
    .mission-box { background-color: #f1f3f5; border-radius: 15px; padding: 20px; text-align: center; border: 3px dashed #FFD43B; margin-bottom: 20px; }
    
    /* 상단 블랙 보드 영역 (내부가 완전히 비어 있는 깔끔한 보드) */
    .black-board { 
        background-color: #212529; 
        border-radius: 15px; 
        min-height: 180px; 
        margin-bottom: 30px; 
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.8); 
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
    }
    
    /* 현재 사용자가 타이핑해서 조립해야 하는 '활성화된 타겟 글자' 표시 스타일 */
    .char-box-target {
        border: 3px solid #ff922b !important;
        background-color: rgba(255, 146, 43, 0.1) !important;
        box-shadow: 0px 0px 12px #ff922b;
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
    .space-dash { width: 35px; height: 50px; border: 2px dashed #495057; border-radius: 6px; margin: auto; }
    .space-blue { border: 2px solid #228BE6; background-color: rgba(34, 139, 230, 0.2); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='lego-title'>🧱 LEGO HANGEUL REVERSE TETRIS</div>", unsafe_allow_html=True)
st.write("---")

# 2. 게임 내부 상태 데이터 저장소 세션 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = []
if 'completed_indices' not in st.session_state:
    st.session_state.completed_indices = set()
if 'current_target_idx' not in st.session_state:
    # 🌟 현재 어떤 글자 자리를 조립해야 하는지 추적하는 인덱스 포인터 (0부터 시작)
    st.session_state.current_target_idx = 0

# 🛠️ Developer Sandbox (화면 테스트용 문장 설정창)
st.markdown("<div class='admin-box' style='background-color: #e8f4fd; padding: 15px; border-radius:10px; border: 1px solid #74c0fc; margin-bottom:20px;'>🛠️ <b>Developer Sandbox</b> (자동 글자 이동 추적 시스템 탑재 버전)</div>", unsafe_allow_html=True)
target_sentence = st.text_input("게임판에 띄우고 싶은 문장을 입력하세요:", value="나는 너를 사랑해")

# 3. 상단 가이드 레이아웃
st.markdown(f"""
    <div class='mission-box'>
        <h3>🎵 Mission Sound: "I love you."</h3>
        <p style='font-size:18px; color:#495057;'>Target Sentence: <b>{target_sentence}</b></p>
    </div>
""", unsafe_allow_html=True)

# 4. 상단 Upward LEGO Assembly Board (완전히 비워둔 검은색 상자)
st.write("### 🏗️ Upward LEGO Assembly Board (상단 조립판)")
st.markdown("<div class='black-board'></div>", unsafe_allow_html=True)

# 5. 그 아래 배치되는 가로형 노란색 폰트 문장 및 파란색 실시간 결합 존
st.write("### 🔤 Word Assembly Line (가로형 조립 라인)")

# 문장 글자 수에 맞추어 컬럼 자동 생성
cols = st.columns(len(target_sentence) + 2)

for idx, char in enumerate(target_sentence):
    with cols[idx]:
        if char == " ": # 띄어쓰기 처리
            # 만약 현재 타겟이 공백 위치라면 자동으로 다음 인덱스로 넘겨줌
            if st.session_state.current_target_idx == idx:
                st.session_state.current_target_idx += 1
                st.rerun()
                
            if idx < st.session_state.current_target_idx:
                st.markdown("<div class='space-dash space-blue'></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='space-dash'></div>", unsafe_allow_html=True)
            continue
            
        # 1. 이미 조립 성공한 글자 포지션 -> 파란색으로 고정
        if idx in st.session_state.completed_indices:
            st.markdown(f"<div class='char-box-yellow char-box-blue'>{char}</div>", unsafe_allow_html=True)
        
        # 2. 현재 사용자가 조립해야 하는 활성화된 타겟 포지션 -> 실시간 입력 브릭 노출
        elif idx == st.session_state.current_target_idx:
            if len(st.session_state.current_input) > 0:
                build_str = ""
                for b in st.session_state.current_input:
                    build_str += f"<span class='ing-brick'>{b}</span>"
                st.markdown(f"<div class='char-box-yellow char-box-target'>{build_str}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='char-box-yellow char-box-target'>{char}</div>", unsafe_allow_html=True)
        
        # 3. 아직 도달하지 않은 대기 상태 포지션 -> 노란색 가이드 유지
        else:
            st.markdown(f"<div class='char-box-yellow'>{char}</div>", unsafe_allow_html=True)

# 6. 실시간 자모음 조합 및 자동 인덱스 포커스 이동 로직
if len(st.session_state.current_input) > 0:
    current_target_char = target_sentence[st.session_state.current_target_idx]
    
    # 🌟 '나' 글자 자동 매칭 및 포커스 이동
    if current_target_char == "나" and st.session_state.current_input == ['ㄴ', 'ㅏ']:
        st.session_state.completed_indices.add(st.session_state.current_target_idx)
        st.session_state.current_target_idx += 1 # 자동으로 다음 글자 위치로 타겟 포인터 이동!
        st.session_state.current_input = []
        st.rerun()
        
    # 🌟 '는' 글자 자동 매칭 및 포커스 이동
    elif current_target_char == "는" and st.session_state.current_input == ['ㄴ', 'ㅡ', 'ㄴ']:
        st.session_state.completed_indices.add(st.session_state.current_target_idx)
        st.session_state.current_target_idx += 1 # 자동으로 다음 글자 위치로 타겟 포인터 이동!
        st.session_state.current_input = []
        st.balloons()
        st.rerun()
        
    # 오입력 방지 매커니즘 (3개 이상 잘못 쌓이면 리셋)
    elif len(st.session_state.current_input) >= 3:
        st.session_state.current_input = []
        st.rerun()

# 7. 하단 자판 영역
st.write("---")
st.write("### ⌨️ LEGO Brick Keyboard (하단 자판)")

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
        st.session_state.completed_indices = set()
        st.session_state.current_target_idx = 0
        st.rerun()

st.write("")
if st.button("⌨️ Space Bar (간격 띄우기) ───", key="btn_space", use_container_width=True):
    # 만약 현재 타겟 위치가 마침 공백(스페이스) 자리라면 자동으로 통과시킴
    if target_sentence[st.session_state.current_target_idx] == " ":
        st.session_state.current_target_idx += 1
    st.rerun()
