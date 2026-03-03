import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 ID)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="현장 MSDS 통합검색", layout="wide")
st.title("🚢 현장 MSDS 통합 검색 시스템")

try:
    @st.cache_data(ttl=1)
    def load_data():
        data = pd.read_csv(CSV_URL)
        data.columns = [col.strip() for col in data.columns]
        return data.fillna("")

    df = load_data()

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요 (물질명, 제조사, 비고 등)", "")

    # 검색 필터링
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask].copy()
    else:
        display_df = df.copy()

    # [핵심] HTML을 이용해 MSDS명에 클릭 가능한 링크 심기
    def make_clickable(name, link):
        # 링크가 있는 경우에만 클릭 가능하게 만듦
        if link.startswith("http"):
            return f'<a href="{link}" target="_blank" style="text-decoration: none; color: #007bff; font-weight: bold;">📄 {name}</a>'
        return name

    # 새로운 '열' 생성 (HTML 링크가 포함된 이름)
    display_df['MSDS명(클릭)'] = display_df.apply(lambda x: make_clickable(x['MSDS명'], x['링크']), axis=1)

    # 화면에 보여줄 순서와 컬럼 정리
    result_df = display_df[['순번', '분류', 'MSDS명(클릭)', 'Maker', '비고']]

    # [중요] HTML 표로 출력
    # st.write 대신 to_html을 사용하여 브라우저가 링크를 직접 인식하게 합니다.
    st.write(
        result_df.to_html(escape=False, index=False, justify='center'),
        unsafe_allow_html=True
    )

    st.markdown("""
        <style>
        table { width: 100%; border-collapse: collapse; }
        th { background-color: #f0f2f6; padding: 10px; text-align: center; border: 1px solid #ddd; }
        td { padding: 10px; border: 1px solid #ddd; text-align: center; }
        tr:hover { background-color: #f5f5f5; }
        </style>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"데이터 로딩 중 오류 발생: {e}")
