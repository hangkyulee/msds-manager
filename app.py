import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 주소로 교체하세요)
# 주의: 주소 끝의 /edit... 부분을 지우고 /export?format=csv 를 붙여야 합니다.
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="MSDS 통합관리", layout="wide")
st.title("🚢 현장 MSDS 통합 검색 시스템")

# 2. 데이터 불러오기
try:
    # 캐시를 사용하여 성능 향상 (st.cache_data)
    @st.cache_data(ttl=60) # 1분마다 업데이트 확인
    def load_data():
        return pd.read_csv(CSV_URL)

    df = load_data()

    # 3. 검색창
    search = st.text_input("🔍 찾으시는 MSDS 이름이나 제조사(Maker)를 입력하세요", "")

    if search:
        # 검색 필터링 (MSDS명 또는 Maker 컬럼 기준)
        res = df[df['MSDS명'].str.contains(search, na=False, case=False) | 
                 df['Maker'].str.contains(search, na=False, case=False)]
        st.write(f"검색 결과: {len(res)}건")
        st.dataframe(res, use_container_width=True)
    else:
        st.write("전체 목록 (구글 시트에서 수정하면 자동 반영됩니다)")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("데이터를 불러올 수 없습니다. 시트 공유 설정을 '링크가 있는 모든 사용자'로 바꿔주세요.")
