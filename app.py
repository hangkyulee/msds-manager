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
        # 컬럼 이름 양옆의 공백을 제거해서 오차 방지
        data.columns = [col.strip() for col in data.columns]
        return data.fillna("")

    df = load_data()

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요", "")

    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # [수정된 부분] LinkColumn 설정
    # 시트의 '링크' 컬럼에 있는 주소를 'MSDS명' 컬럼의 클릭 링크로 사용합니다.
    st.dataframe(
        display_df,
        column_config={
            "MSDS명": st.column_config.LinkColumn(
                "MSDS명 (클릭하면 열림)",
                display_text=None  # 링크 대신 'MSDS명' 텍스트를 그대로 표시
            ),
            "링크": st.column_config.LinkColumn("원본 링크") # 작동 확인을 위해 일단 노출
        },
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
