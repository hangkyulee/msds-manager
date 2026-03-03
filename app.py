import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 ID)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="MSDS 통합관리", layout="wide")
st.title("🚢 현장 MSDS 통합 검색 시스템")

try:
    @st.cache_data(ttl=1)
    def load_data():
        data = pd.read_csv(CSV_URL)
        data.columns = [col.strip() for col in data.columns]
        return data.fillna("")

    df = load_data()

    # [핵심 로직] MSDS명 칸에 링크 주소를 덮어씌웁니다.
    # 이렇게 해야 클릭했을 때 해당 주소로 이동합니다.
    if 'MSDS명' in df.columns and '링크' in df.columns:
        df['MSDS명'] = df['링크'] 

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요 (물질명, 제조사, 비고 등)", "")

    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # 표 출력
    st.data_editor(
        display_df,
        column_config={
            "MSDS명": st.column_config.LinkColumn(
                "파일 열기 (클릭)",
                help="주소를 클릭하면 MSDS 파일이 새 창에서 열립니다."
            ),
            "링크": None # 주소 열은 중복이므로 숨깁니다.
        },
        hide_index=True,
        use_container_width=True,
        disabled=True
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
