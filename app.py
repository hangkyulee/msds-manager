import streamlit as st
import pandas as pd

st.set_page_config(page_title="현장 MSDS 관리 시스템", layout="wide")

# 1. 구글 시트 ID 설정 (주소창의 d/ 와 /edit 사이의 복잡한 문자열을 넣으세요)
# 예: https://docs.google.com/spreadsheets/d/1A2B3C... 에서 1A2B3C... 부분
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig/export?format=csv"

# --- [진단 모드] 데이터가 안 나올 때 확인용 ---
with st.expander("🛠️ 시스템 연결 상태 확인 (데이터가 안 나오면 클릭)"):
    st.write(f"접속 시도 주소: {https://docs.google.com/spreadsheets/d/1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig/edit?gid=0#gid=0}")
    try:
        test_df = pd.read_csv(https://docs.google.com/spreadsheets/d/1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig/edit?gid=0#gid=0)
        st.success(f"연결 성공! 현재 시트에 저장된 파일 개수: {len(test_df)}개")
        st.write("시트 컬럼명(제목):", test_df.columns.tolist())
    except Exception as e:
        st.error(f"연결 실패 사유: {e}")
        st.info("💡 구글 시트의 [공유] 설정이 '링크가 있는 모든 사용자 - 뷰어'로 되어 있는지 꼭 확인하세요!")

# 2. 데이터 불러오기 함수
def load_data():
    try:
        # 캐시 없이 실시간으로 읽어오기 (오류 방지)
        df = pd.read_csv(https://docs.google.com/spreadsheets/d/1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig/edit?gid=0#gid=0)
        # 모든 데이터를 문자열로 변환하고 앞뒤 공백 제거
        df = df.fillna('').astype(str)
        for col in df.columns:
            df[col] = df[col].str.strip()
        return df
    except:
        return pd.DataFrame(columns=["분류", "MSDS명", "Maker", "링크", "비고"])

df = load_data()

# --- 메인 화면 UI ---
st.title("🚢 현장 MSDS 통합 검색 시스템")
st.write("원하는 카테고리 버튼을 누르거나 직접 검색하세요.")

# --- 7대 대분류 버튼 ---
st.subheader("📁 카테고리별 보기")
row1 = st.columns(4)
row2 = st.columns(4)

category_choice = None

# 버튼 정의
categories = [
    ("🎨", "1. 도장재", "도장재"),
    ("⚡", "2. 용접재", "용접재"),
    ("🛢️", "3. 오일,락카", "오일,락카"),
    ("🧵", "4. 섬유", "섬유"),
    ("🧱", "5. 충진재,경화재", "충진재,경화재"),
    ("🔥", "6. 가스", "가스"),
    ("📦", "7. 기타용품", "기타용품")
]

# 버튼 생성 로직
for i, (icon, label, val) in enumerate(categories):
    target_row = row1 if i < 4 else row2
    if target_row[i % 4].button(f"{icon}\n\n{label}", use_container_width=True):
        category_choice = val

with row2[3]:
    if st.button("🔄\n\n전체 초기화", use_container_width=True):
        st.rerun()

# --- 검색창 ---
st.divider()
search_query = st.text_input("🔍 직접 검색 (물질명 또는 제조사)", placeholder="예: Paint, KCC, 가스 등")

# --- 데이터 필터링 ---
if category_choice:
    st.info(f"📍 '{category_choice}' 필터링 결과입니다.")
    # 분류 컬럼에서 선택한 글자가 포함된 것 찾기
    filtered_df = df[df['분류'].str.contains(category_choice, na=False)]
elif search_query:
    # 검색어 포함 여부 확인
    filtered_df = df[
        df['MSDS명'].str.contains(search_query, case=False) | 
        df['Maker'].str.contains(search_query, case=False)
    ]
else:
    filtered_df = df

# --- 최종 결과 표 출력 ---
st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "링크": st.column_config.LinkColumn("파일 열기", help="클릭하면 구글 드라이브 파일로 연결됩니다.")
    }
)

st.caption(f"총 {len(filtered_df)}개의 항목이 표시되고 있습니다.")
