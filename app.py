import streamlit as st
import pandas as pd
import os

# 파일 저장 경로 (데이터베이스 역할)
DATA_FILE = 'msds_list.csv'

# 데이터 불러오기 함수
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # 초기 데이터 구조 설정
        return pd.DataFrame(columns=['순번', '분류', 'MSDS명', 'Maker', '구글드라이브 링크', '비고'])

# 프로그램 제목
st.title("🚢 MSDS 통합 관리 시스템")

# 1. 데이터 로드
df = load_data()

# 2. 검색 기능
st.subheader("🔍 MSDS 검색")
search_term = st.text_input("물질명 또는 제조사를 입력하세요")
filtered_df = df[df['MSDS명'].str.contains(search_term, na=False) | 
                 df['Maker'].str.contains(search_term, na=False)]
st.dataframe(filtered_df, use_container_width=True)

# 3. 항목 추가 기능 (사이드바 또는 하단)
st.divider()
st.subheader("➕ 새 MSDS 항목 추가")
with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("분류", ["Paint류", "Oil류", "용제류", "기타"])
        msds_name = st.text_input("MSDS명")
    with col2:
        maker = st.text_input("Maker (제조사)")
        link = st.text_input("구글 드라이브 링크 (URL)")
    
    note = st.text_area("비고")
    submit = st.form_submit_button("항목 추가하기")

    if submit:
        new_no = len(df) + 1
        new_data = pd.DataFrame([[new_no, category, msds_name, maker, link, note]], 
                                columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"'{msds_name}' 항목이 추가되었습니다!")
        st.rerun()
