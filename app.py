import streamlit as st
import pandas as pd

# 1. 설정 (본인의 시트 ID)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="MSDS 통합관리", layout="wide")
st.title("🚢 현장 MSDS 통합 검색 시스템")
st.info("💡 물질명, 제조사뿐만 아니라 '비고'에 적힌 색인으로도 검색이 가능합니다.")

try:
    # 데이터 불러오기 (캐시 설정으로 속도 향상)
    @st.cache_data(ttl=5) # 5초마다 갱신 (현장 대응용)
    def load_data():
        data = pd.read_csv(CSV_URL)
        # 모든 데이터를 문자열로 변환하고 양쪽 공백 제거
        return data.applymap(lambda x: str(x).strip() if pd.notnull(x) else "")

    df = load_data()

    # 검색창 (안내 문구 수정)
    search = st.text_input("🔍 검색어를 입력하세요 (물질명, 제조사, 비고 색인 등)", "")

    if search:
        # 대소문자 구분 없이 모든 컬럼에서 검색어 포함 여부 확인
        # '비고' 컬럼을 포함한 전체 데이터프레임에서 검색을 수행합니다.
        mask = df.apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        res = df[mask]
        
        st.success(f"총 {len(res)}건의 항목이 검색되었습니다.")
        st.dataframe(res, use_container_width=True)
    else:
        st.write("전체 목록 (구글 시트에서 수정하면 즉시 반영됩니다)")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"에러가 발생했습니다. 시트 설정이나 인터넷 연결을 확인해주세요: {e}")

st.markdown("---")
st.caption("Tip: 비고란에 '구역명', '위험특성', '관리번호' 등을 적어두시면 더욱 편리하게 검색할 수 있습니다.")
