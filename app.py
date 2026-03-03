import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 ID)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="현장 MSDS 통합검색", layout="wide")

# 타이틀 부분
st.title("🚢 현장 MSDS 통합 검색 시스템")
st.info("💡 아래 MSDS 명칭(파란색 글자)을 누르면 원본 파일이 바로 열립니다.")

try:
    @st.cache_data(ttl=1)
    def load_data():
        data = pd.read_csv(CSV_URL)
        data.columns = [col.strip() for col in data.columns]
        return data.fillna("")

    df = load_data()

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요 (물질명, 제조사, 비고 색인 등)", "")

    # 검색 필터링
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # [핵심] 표 대신 '카드 형태'로 리스트 출력
    if not display_df.empty:
        for _, row in display_df.iterrows():
            # 디자인용 컨테이너 생성
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    # 마크다운 방식으로 이름에 링크를 겁니다 (가장 확실한 방법)
                    st.markdown(f"### [📄 {row['MSDS명']}]({row['링크']})")
                    st.write(f"**제조사:** {row['Maker']} | **분류:** {row['분류']}")
                with col2:
                    if row['비고']:
                        st.caption(f"📌 **비고**")
                        st.caption(row['비고'])
                st.divider() # 구분선
    else:
        st.warning("검색 결과가 없습니다.")

except Exception as e:
    st.error(f"데이터 로딩 중 오류 발생: {e}")
