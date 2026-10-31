import streamlit as st

# 1. 페이지 와이드 고정 및 디자인 스타일 정의
st.set_page_config(page_title="LEGO Hangeul Tetris", page_icon="🧱", layout="wide")

st.markdown("""
    <style>
    .lego-title { text-align: center; color: #FFD43B; font-size: 40px; font-weight: bold; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px #000; }
    .mission-box { background-color: #f1f3f5; border-radius: 15px; padding: 20px; text-align: center; border: 3px dashed #FFD43B; margin-bottom: 20px; }
    
    /* 상단 블랙 보드 영역 */
    .black-board { 
        background-color: #212529; 
        border-radius: 15px; 
        min-height: 180px; 
        margin-bottom: 30px; 
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.8); 
    }
    
    /* 가이드 상태: 노란색 가로형 폰트 블록 */
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
    
    /* 현재 조립하고 있는 '활성화된 타겟 단어 영역' 표시 스타일 */
    .char-box-target {
        border: 3px solid #ff922b !important;
        background-color: rgba(255, 146, 43, 0.08) !important;
        box-shadow: 0px 0px 15px rgba(255, 146, 43, 0.6);
    }
    
    /* 조립 완료된 파란색 레고 상태 */
    .char-box-blue {
        color: white !important;
        background-color: #228BE6 !important;
        border: 2px solid #1c7ed6 !important;
        box-shadow: 0px 4px #1864ab;
        text-shadow: none;
    }
    
    /* 조립 도중 꽂히는 실시간 브릭 */
    .ing-brick { color: #228BE6; font-size: 34px; font-weight: bold; }
    
    /* 스페이스 공간 */
    .space-dash { width: 35px; height: 50px; border: 2px dashed #495057; border-radius: 6px; margin: auto; }
    .space-blue { border: 2px solid #228BE6; background-color: rgba(34, 139, 230, 0.2); }
    
    /* 힌트 대상 자판 버튼에 들어갈 간접 배경색 스타일 */
    .hint-active-con { background-color: rgba(34, 139, 230, 0.2) !important; border: 2px solid #228BE6 !important; border-radius: 10px; padding: 5px; }
    .hint-inactive-con { background-color: transparent !important; padding: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='lego-title'>🧱 LEGO HANGEUL REVERSE TETRIS</div>", unsafe_allow_html=True)
st.write("---")

# 2. 내부 데이터 및 트래킹 세션 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = []
if 'completed_indices' not in st.session_state:
    st.session_state.completed_indices = set()
if 'current_target_idx' not in st.session_state:
    st.session_state.current_target_idx = 0

target_sentence = "나는 너를 사랑해"

# 3. 미션 가이드 문구
st.markdown(f"""
    <div class='mission-box'>
        <h3>🎵 Mission Sound: "I love you."</h3>
        <p style='font-size:18px; color:#495057;'>Target Sentence: <b>{target_sentence}</b></p>
    </div>
""", unsafe_allow_html=True)

# 4. 상단 블랙 보드
st.write("### 🏗️ Upward LEGO Assembly Board (상단 조립판)")
st.markdown("<div class='black-board'></div>", unsafe_allow_html=True)

# 5. 가로형 조립 라인 구성
st.write("### 🔤 Word Assembly Line (가로형 조립 라인)")
cols = st.columns(len(target_sentence) + 2)

cur_idx = st.session_state.current_target_idx

for idx, char in enumerate(target_sentence):
    with cols[idx]:
        if char == " ":
            if cur_idx == idx:
                st.session_state.current_target_idx += 1
                st.rerun()
            if idx < cur_idx:
                st.markdown("<div class='space-dash space-blue'></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='space-dash'></div>", unsafe_allow_html=True)
            continue
            
        # 완성된 글자 처리
        if idx in st.session_state.completed_indices:
            st.markdown(f"<div class='char-box-yellow char-box-blue'>{char}</div>", unsafe_allow_html=True)
        
        # 현재 실시간 입력 브릭 노출 타겟 포지션
        elif idx == cur_idx:
            if len(st.session_state.current_input) > 0:
                build_str = ""
                for b in st.session_state.current_input:
                    build_str += f"<span class='ing-brick'>{b}</span>"
                st.markdown(f"<div class='char-box-yellow char-box-target'>{build_str}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='char-box-yellow char-box-target'>{char}</div>", unsafe_allow_html=True)
        
        # 🌟 에러 완벽 해결: 빈 상자 없이 단어 단위 매칭 묶음을 안전하게 판정하는 구조
        else:
            is_target_word = False
            if cur_idx in [0, 1] and idx in [0, 1]:
                is_target_word = True
            elif cur_idx in [3, 4] and idx in [3, 4]:
                is_target_word = True
            elif cur_idx in [6, 7, 8] and idx in [6, 7, 8]:
                is_target_word = True
                
            if is_target_word:
                st.markdown(f"<div class='char-box-yellow char-box-target'>{char}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='char-box-yellow'>{char}</div>", unsafe_allow_html=True)

# 6. 현재 조립 단계별 힌트 자모음 리스트 (완벽 고정형 배열 정의)
hint_bricks = set()
if cur_idx in [0, 1]:
    hint_bricks = {'ㄴ', 'ㅏ', 'ㅡ'}
elif cur_idx in [3, 4]:
    hint_bricks = {'ㄴ', 'ㅓ', 'ㄹ', 'ㅡ'}
elif cur_idx in [6, 7, 8]:
    hint_bricks = {'ㅅ', 'ㅏ', 'ㄹ', 'ㅇ', 'ㅎ', 'ㅐ'}

# 7. 실시간 가로형 결합 판정 시스템
if len(st.session_state.current_input) > 0:
    if cur_idx == 0 and st.session_state.current_input == ['ㄴ', 'ㅏ']:
        st.session_state.completed_indices.add(0)
        st.session_state.current_target_idx = 1
        st.session_state.current_input = []
        st.rerun()
    elif cur_idx == 1 and st.session_state.current_input == ['ㄴ', 'ㅡ', 'ㄴ']:
        st.session_state.completed_indices.add(1)
        st.session_state.current_target_idx = 2 
        st.session_state.current_input = []
        st.rerun()
    elif cur_idx == 3 and st.session_state.current_input == ['ㄴ', 'ㅓ']:
        st.session_state.completed_indices.add(3)
        st.session_state.current_target_idx = 4
        st.session_state.current_input = []
        st.rerun()
    elif cur_idx == 4 and st.session_state.current_input == ['ㄹ', 'ㅡ', 'ㄹ']:
        st.session_state.completed_indices.add(4)
        st.session_state.current_target_idx = 5
        st.session_state.current_input = []
        st.rerun()
    elif cur_idx == 6 and st.session_state.current_input == ['ㅅ', 'ㅏ']:
        st.session_state.completed_indices.add(6)
        st.session_state.current_target_idx = 7
        st.session_state.current_input = []
        st.rerun()
    elif cur_idx == 7 and st.session_state.current_input == ['ㄹ', 'ㅏ', 'ㅇ']:
        st.session_state.completed_indices.add(7)
        st.session_state.current_target_idx = 8
        st.session_state.current_input = []
        st.rerun()
    elif cur_idx == 8 and st.session_state.current_input == ['ㅎ', 'ㅐ']:
        st.session_state.completed_indices.add(8)
        st.markdown("<div class='success-banner'>🎉 축하합니다! 모든 단어를 완성하여 전체 문장이 파란색 레고 보드로 채워졌습니다! ✨</div>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.current_input = []
        st.rerun()
    elif len(st.session_state.current_input) >= 3:
        st.session_state.current_input = []
        st.rerun()

# 8. 하단 자판 영역 (전체 자모음 나열형 키보드 + 가변형 간접 배경색 힌트 장착)
st.write("---")
st.write("### ⌨️ LEGO Brick Keyboard (하단 자판 전체 보관소)")
st.caption("현재 타이핑해야 하는 단어에 필요한 필수 자모음 브릭에만 파란색 간접 배경색 힌트(🧱)가 활성화됩니다.")

# 자음 라인 멀티 컬럼 구성
st.write("**[ 자음 브릭 보관 구역 ]**")
con_cols = st.columns(7)
all_consonants = ['ㄴ', 'ㄹ', 'ㅅ', 'ㅇ', 'ㅎ', 'ㄱ', 'ㄷ']

for i, con in enumerate(all_consonants):
    with con_cols[i]:
        style_class = "hint-active-con" if con in hint_bricks else "hint-inactive-con"
        st.markdown(f"<div class='{style_class}'>", unsafe_allow_html=True)
        if st.button(f"🔵 {con}", key=f"btn_{con}", use_container_width=True):
            st.session_state.current_input.append(con)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 모음 라인 멀티 컬럼 구성
st.write("**[ 모음 브릭 보관 구역 ]**")
vow_cols = st.columns(7)
all_vowels = ['ㅏ', 'ㅡ', 'ㅓ', 'ㅐ', 'ㅗ', 'ㅜ', 'ㅣ']

for i, vow in enumerate(all_vowels):
    with vow_cols[i]:
        style_class = "hint-active-con" if vow in hint_bricks else "hint-inactive-con"
        st.markdown(f"<div class='{style_class}'>", unsafe_allow_html=True)
        if st.button(f"🔴 {vow}", key=f"btn_{vow}", use_container_width=True):
            st.session_state.current_input.append(vow)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 시스템 조작 영역
st.write("")
col_space, col_reset = st.columns(2)
with col_space:
    if st.button("⌨️ Space Bar (단어 간격 건너뛰기) ───", key="btn_space", use_container_width=True):
        if cur_idx < len(target_sentence) and target_sentence[cur_idx] == " ":
            st.session_state.current_target_idx += 1
        st.rerun()
with col_reset:
    if st.button("🟡 초기화 🔄", key="btn_reset", use_container_width=True):
        st.session_state.current_input = []
        st.session_state.completed_indices = set()
        st.session_state.current_target_idx = 0
        st.rerun()
