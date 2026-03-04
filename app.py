import streamlit as st
import pandas as pd

st.set_page_config(page_title="현장 MSDS 관리 시스템", layout="wide")

# 1. 구글 시트 설정
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 2. 데이터 불러오기 함수
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.fillna('').astype(str)
        for col in df.columns:
            df[col] = df[col].str.strip()
        return df
    except:
        return pd.DataFrame(columns=["분류", "MSDS명", "Maker", "링크", "비고"])

df = load_data()

# --- 메인 UI ---
st.title("🚢 현장 MSDS 통합 검색 시스템")
st.info("💡 리스트에서 **물질명(MSDS명)**을 클릭하면 해당 파일을 바로 볼 수 있습니다.")

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

if row2[3].button("🔄\n\n전체 초기화", use_container_width=True):
    st.rerun()

# --- 검색창 ---
st.divider()
search_query = st.text_input("🔍 직접 검색 (물질명 또는 제조사)", placeholder="예: Paint, KCC, 가스 등")

# --- 데이터 필터링 ---
if category_choice:
    st.success(f"📍 '{category_choice}' 필터링 결과")
    filtered_df = df[df['분류'].str.contains(category_choice, na=False)].copy()
elif search_query:
    filtered_df = df[
        df['MSDS명'].str.contains(search_query, case=False, na=False) | 
        df['Maker'].str.contains(search_query, case=False, na=False)
    ].copy()
else:
    filtered_df = df.copy()

# --- [중요] 링크 연결 로직 ---
# 'MSDS명'에 링크 주소를 직접 심을 수는 없어서, Streamlit의 LinkColumn 기능을 사용합니다.
# 링크가 있는 행들만 골라내어 MSDS명 컬럼을 링크형태로 변환합니다.

# --- 표 출력 ---
st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "링크": st.column_config.LinkColumn(
            "MSDS 열기", 
            display_text="문서 열기 📄" # 링크 주소 대신 이 글자가 보임
        ),
        "MSDS명": st.column_config.TextColumn("물질명", width="medium"),
        "분류": "분류",
        "Maker": "제조사",
        "비고": "비고"
    }
)

st.caption(f"현재 {len(filtered_df)}개의 항목이 표시 중입니다. '문서 열기'를 누르면 파일이 연결됩니다.")
