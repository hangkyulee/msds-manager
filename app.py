import streamlit as st
import pandas as pd

st.set_page_config(page_title="현장 MSDS 관리 시스템", layout="wide")

# 1. 데이터 불러오기 (본인의 구글 시트 주소로 변경 필수)
# 시트의 '분류' 열에 아래 버튼 이름들이 정확히 있어야 필터링이 됩니다.
SHEET_URL = "여기에_본인의_구글_시트_주소를_넣으세요"
CSV_URL = SHEET_URL.replace('/edit#gid=', '/export?format=csv&gid=')

@st.cache_data
def load_data():
    try:
        # 데이터 로드 후 공백 제거 등 전처리
        data = pd.read_csv(CSV_URL)
        return data
    except:
        return pd.DataFrame(columns=["분류", "MSDS명", "Maker", "링크", "비고"])

df = load_data()

# --- 상단 타이틀 ---
st.title("🚢 MSDS 통합 검색 시스템")
st.write("카테고리를 선택하거나 검색창을 이용해 주세요.")

# --- 7대 대분류 버튼 (모바일 앱 스타일) ---
st.subheader("📁 카테고리별 보기")

# 버튼 배치를 위해 4열 구성 (첫 줄 4개, 둘째 줄 3개)
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

category_choice = None

# 첫 번째 줄
with row1_col1:
    if st.button("🎨\n\n1. 도장재", use_container_width=True):
        category_choice = "도장재"
with row1_col2:
    if st.button("⚡\n\n2. 용접재", use_container_width=True):
        category_choice = "용접재"
with row1_col3:
    if st.button("🛢️\n\n3. 오일,락카", use_container_width=True):
        category_choice = "오일,락카"
with row1_col4:
    if st.button("🧵\n\n4. 섬유", use_container_width=True):
        category_choice = "섬유"

# 두 번째 줄
with row2_col1:
    if st.button("🧱\n\n5. 충진재,경화재", use_container_width=True):
        category_choice = "충진재,경화재"
with row2_col2:
    if st.button("🔥\n\n6. 가스", use_container_width=True):
        category_choice = "가스"
with row2_col3:
    if st.button("📦\n\n7. 기타용품", use_container_width=True):
        category_choice = "기타용품"
with row2_col4:
    if st.button("🔄\n\n전체 초기화", use_container_width=True):
        category_choice = None
        st.rerun()

# --- 검색창 ---
st.divider()
search_query = st.text_input("🔍 직접 검색 (물질명 또는 제조사 입력)", "")

# --- 데이터 필터링 로직 ---
if category_choice:
    st.info(f"📍 '{category_choice}' 필터링 결과입니다.")
    # 시트의 '분류' 열에서 선택한 카테고리와 일치하는 행만 추출
    filtered_df = df[df['분류'].str.contains(category_choice, na=False)]
elif search_query:
    # 검색어 입력 시 이름이나 제조사에서 검색
    filtered_df = df[df['MSDS명'].str.contains(search_query, na=False) | 
                     df['Maker'].str.contains(search_query, na=False)]
else:
    filtered_df = df

# --- 결과 표 출력 ---
st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "링크": st.column_config.LinkColumn("MSDS 링크") # 링크를 클릭 가능하게 설정
    }
)

st.caption("※ 카테고리 버튼을 누르면 해당 품목만 모아서 볼 수 있습니다.")
