import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 ID)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="MSDS 통합관리", layout="wide")
st.title("🚢 현장 MSDS 통합 검색 시스템")
st.info("💡 목록에서 'MSDS명'을 클릭하면 해당 MSDS 파일을 바로 확인할 수 있습니다.")

try:
    @st.cache_data(ttl=5)
    def load_data():
        # 시트를 읽어오고 빈칸은 빈 문자열로 처리
        data = pd.read_csv(CSV_URL)
        return data.fillna("")

    df = load_data()

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요 (물질명, 제조사, 비고 색인 등)", "")

    # 검색 로직
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # 2. 표 설정 (MSDS명에 링크 걸기)
    st.data_editor(
        display_df,
        column_config={
            "MSDS명": st.column_config.LinkColumn(
                "MSDS명 (클릭 시 열림)",
                display_text=None, # 링크 주소 대신 MSDS명 텍스트 그대로 표시
                help="클릭하면 해당 MSDS 파일을 엽니다."
            ),
            "링크": None, # 원본 링크 컬럼은 숨깁니다 (MSDS명에 합쳐졌으므로)
        },
        hide_index=True,
        use_container_width=True,
        disabled=True # 편집은 불가능하게 설정
    )

except Exception as e:
    st.error(f"데이터 로딩 중 오류 발생: {e}")

st.markdown("---")
st.caption("비고란의 색인으로도 검색이 가능합니다. 예: '인화성', 'A구역' 등")
