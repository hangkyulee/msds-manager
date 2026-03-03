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

    # 검색창
    search = st.text_input("🔍 검색어를 입력하세요 (물질명, 제조사, 비고 등)", "")

    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # [마법의 구간] 표 출력 설정
    st.dataframe(
        display_df,
        column_config={
            "MSDS명": st.column_config.LinkColumn(
                "MSDS명 (클릭하면 열림)",
                # '링크' 컬럼에 있는 주소를 가져와서 'MSDS명' 글자에 연결합니다.
                url_template=display_df["링크"],
                display_text=None # 시트의 MSDS명 텍스트를 그대로 사용
            ),
            "링크": None # 원본 주소 칸은 보기 싫으니까 숨깁니다.
        },
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    # 에러가 날 경우를 대비한 안전 장치 (만약 url_template이 안 먹히는 버전일 때)
    st.warning("표 형식을 다시 로드합니다...")
    st.dataframe(display_df, use_container_width=True)
