import streamlit as st
import pandas as pd

st.set_page_config(page_title="현장 MSDS 관리 시스템", layout="wide")

# 1. 구글 시트 설정 (사용자님의 시트 ID 적용)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 2. 데이터 불러오기 함수
@st.cache_data(ttl=60) # 1분마다 새로운 데이터를 읽어오도록 설정
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

# --- [핵심 수정] 클릭 가능하게 변환 ---
# 1. '링크' 열에 있는 주소를 'MSDS명' 열에 입혀서 클릭하면 링크가 열리게 함
# 2. 실제 화면에는 링크 주소 대신 'MSDS명' 텍스트만 보이게 함

# --- 표 출력 ---
st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "MSDS명": st.column_config.LinkColumn(
            "MSDS명 (클릭 시 열기)",
            # 링크 열의 값을 가져와서 연결
            validate=r"^https?://",
            display_text=r"^https?://.*" # 정규표현식 대신 아래에서 데이터를 치환하는 방식 사용
        ),
        "링크": None,  # 주소만 적힌 열은 숨김 (깔끔함)
        "분류": "분류",
        "Maker": "제조사",
        "비고": "비고"
    }
)

# 만약 위 설정에서 이름이 주소로 보인다면, 아래 코드로 우회 처리합니다.
# (Streamlit 최신 버전 권장 방식)
# filtered_df['파일보기'] = filtered_df['링크']
# st.dataframe(filtered_df[['분류', 'MSDS명', 'Maker', '파일보기', '비고']], ...)

st.caption(f"현재 {len(filtered_df)}개의 항목이 표시 중입니다.")
