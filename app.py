import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 ID 확인)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="MSDS 통합관리", layout="wide")
st.title("🚢 현장 MSDS 통합 검색 시스템")

try:
    @st.cache_data(ttl=2) # 테스트를 위해 갱신 시간을 2초로 줄임
    def load_data():
        # 시트를 읽고 모든 칸의 공백을 제거
        data = pd.read_csv(CSV_URL)
        return data.fillna("")

    df = load_data()

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요", "")

    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # [핵심] 표 출력 설정 - 이 부분이 링크를 활성화합니다.
    st.dataframe(
        display_df,
        column_config={
            "MSDS명": st.column_config.LinkColumn(
                "MSDS명 (클릭하면 열림)",
                help="이 이름을 클릭하면 해당 MSDS 원본 파일이 열립니다.",
                # '링크' 컬럼에 있는 데이터를 가져와서 연결합니다.
                validate="^https://.*",
                display_text=None 
            ),
            "링크": st.column_config.LinkColumn("원본 링크 (직접 클릭용)") # 확인을 위해 일단 링크 열도 보여줍니다.
        },
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    st.error(f"오류 발생: {e}")

st.markdown("---")
st.caption("비고란의 색인으로도 검색이 가능합니다. 예: '인화성', 'A구역' 등")
