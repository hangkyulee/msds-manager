import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 웹 페이지 기본 설정 (타이틀, 아이콘, 레이아웃)
st.set_page_config(
    page_title="현장 MSDS 관리 시스템",
    page_icon="🚢",
    layout="wide"
)

# 2. 프로그램 제목 표시
st.title("🚢 현장 MSDS 통합 검색 시스템")
st.markdown("---")

# 3. 구글 스프레드시트 연결 (Secrets 설정을 자동으로 사용함)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # 데이터를 읽어옵니다. (시트의 첫 번째 탭 기준)
    df = conn.read()
    
    # 데이터가 비어있지 않은지 확인
    if df is not None:
        # 4. 검색창 구현 (사이드바 또는 상단)
        st.subheader("🔍 MSDS 검색")
        search_query = st.text_input("물질명(MSDS명) 또는 제조사(Maker)를 입력하세요", placeholder="예: Paint, 오일, KCC 등")

        # 5. 검색 로직 적용
        if search_query:
            # 'MSDS명' 컬럼이나 'Maker' 컬럼에 검색어가 포함된 행만 필터링
            filtered_df = df[
                df['MSDS명'].str.contains(search_query, na=False, case=False) | 
                df['Maker'].str.contains(search_query, na=False, case=False)
            ]
            st.write(f"총 {len(filtered_df)}건의 항목이 검색되었습니다.")
            
            # 링크(URL)가 있다면 클릭 가능한 형태로 표기하기 위해 설정
            st.dataframe(
                filtered_df, 
                use_container_width=True,
                column_config={
                    "링크": st.column_config.LinkColumn("MSDS 원본 링크")
                }
            )
        else:
            # 검색어가 없을 때는 전체 목록 표시
            st.write("현재 등록된 전체 MSDS 목록입니다.")
            st.dataframe(
                df, 
                use_container_width=True,
                column_config={
                    "링크": st.column_config.LinkColumn("MSDS 원본 링크")
                }
            )

    else:
        st.warning("구글 시트에 데이터가 없습니다. 시트를 확인해 주세요.")

except Exception as e:
    st.error("⚠️ 데이터를 불러오는 중 오류가 발생했습니다.")
    st.info("다음을 확인해 보세요:")
    st.markdown("""
    1. **Secrets 설정:** `[connections.gsheets]`와 주소가 정확한지 확인
    2. **구글 시트 공유:** 서비스 계정 이메일을 **'편집자'**로 추가했는지 확인
    3. **컬럼명:** 구글 시트의 첫 줄이 **순번, 분류, MSDS명, Maker, 링크, 비고**인지 확인
    """)
    st.expander("상세 에러 내용 보기").write(e)

# 6. 하단 정보
st.markdown("---")
st.caption("관리자 안내: 항목 추가는 연결된 구글 스프레드시트에서 직접 수행하시면 실시간으로 반영됩니다.")
