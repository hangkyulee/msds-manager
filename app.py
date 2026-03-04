import streamlit as st
import pandas as pd

st.set_page_config(page_title="현장 MSDS 관리 시스템", layout="wide")

# 1. 구글 시트 설정 (사용자님의 시트 ID가 적용되었습니다)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
# 데이터를 읽어오기 위한 전용 주소 형식 (수정됨)
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- [진단 모드] ---
with st.expander("🛠️ 시스템 연결 상태 확인"):
    st.write(f"접속 시도 주소: {SHEET_URL}")
    try:
        # 주소에 따옴표를 추가하여 정상적으로 읽히도록 수정
        test_df = pd.read_csv(SHEET_URL)
        st.success(f"✅ 연결 성공! 시트 데이터 개수: {len(test_df)}개")
        st.write("컬럼명 확인:", test_df.columns.tolist())
    except Exception as e:
        st.error(f"❌ 연결 실패: {e}")
        st.info("💡 구글 시트 우측 상단 [공유] -> [링크가 있는 모든 사용자 - 뷰어]로 되어있는지 꼭 확인하세요!")

# 2. 데이터 불러오기 함수
def load_data():
    try:
        # 실시간으로 CSV 데이터를 읽어옴
        df = pd.read_csv(SHEET_URL)
        df = df.fillna('').astype(str)
        for col in df.columns:
            df[col] = df[col].str.strip()
        return df
    except:
        # 실패 시 빈 표 생성
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

categories = [
    ("🎨", "1. 도장재", "Paint"),
    ("⚡", "2. 용접재", "용접재"),
    ("🛢️", "3. 오일,락카", "오일,락카"),
    ("🧵", "4. 섬유", "섬유"),
    ("🧱", "5. 충진재,경화재", "충진재,경화재"),
    ("🔥", "6. 가스", "가스"),
    ("📦", "7. 기타용품", "기타용품")
]

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
    # 분류 열에 버튼 이름이 포함되어 있는지 확인
    filtered_df = df[df['분류'].str.contains(category_choice, na=False)]
elif search_query:
    filtered_df = df[
        df['MSDS명'].str.contains(search_query, case=False, na=False) | 
        df['Maker'].str.contains(search_query, case=False, na=False)
    ]
else:
    filtered_df = df

# --- 최종 결과 표 출력 ---
st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "링크": st.column_config.LinkColumn("파일 열기")
    }
)

st.caption(f"총 {len(filtered_df)}개의 항목이 표시되고 있습니다.")
