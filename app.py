import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 ID)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="MSDS 통합관리", layout="wide")
st.title("🚢 현장 MSDS 통합 검색 시스템")

try:
    @st.cache_data(ttl=1) # 즉각 반영을 위해 1초 설정
    def load_data():
        data = pd.read_csv(CSV_URL)
        # 컬럼 이름의 앞뒤 공백을 강제로 제거해서 오차 방지
        data.columns = [col.strip() for col in data.columns]
        return data.fillna("")

    df = load_data()

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요", "")

    # 검색 필터링
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # [중요] 링크 데이터가 있는 컬럼명을 자동으로 찾기
    # '링크', '주소', 'URL' 중 하나라도 포함된 컬럼을 찾습니다.
    link_col = next((c for c in df.columns if '링크' in c or 'URL' in c or '주소' in c), None)

    if link_col:
        st.data_editor(
            display_df,
            column_config={
                "MSDS명": st.column_config.LinkColumn(
                    "MSDS명 (클릭하면 열림)",
                    # '링크'라고 적힌 컬럼의 실제 데이터를 주소로 사용함
                    url_template=display_df[link_col], 
                    display_text=None
                ),
                link_col: None # 실제 주소가 적힌 열은 화면에서 숨김
            },
            hide_index=True,
            use_container_width=True,
            disabled=True
        )
    else:
        # 링크 컬럼을 못 찾았을 경우 일반 표로 출력
        st.warning("시트에서 '링크'라는 제목의 칸을 찾을 수 없습니다. 제목을 확인해주세요.")
        st.dataframe(display_df, use_container_width=True)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
