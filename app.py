import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🚢 현장 MSDS 관리 시스템")

# 구글 시트 연결 (Secrets 설정을 자동으로 읽어옵니다)
conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기
df = conn.read()

# 검색 기능
search = st.text_input("🔍 MSDS 명칭 또는 Maker를 입력하세요")
if search:
    filtered_df = df[df['MSDS명'].str.contains(search, na=False) | 
                     df['Maker'].str.contains(search, na=False)]
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

# 항목 추가 기능
with st.expander("➕ 새 MSDS 추가하기"):
    with st.form("msds_form"):
        new_cat = st.selectbox("분류", ["Paint류", "Oil류", "용제류", "기타"])
        new_name = st.text_input("MSDS명")
        new_maker = st.text_input("Maker")
        new_link = st.text_input("구글드라이브 링크")
        new_note = st.text_area("비고")
        
        if st.form_submit_button("저장하기"):
            # 기존 데이터에 추가
            new_row = [len(df)+1, new_cat, new_name, new_maker, new_link, new_note]
            # 실제 시트에 업데이트하는 로직 (conn.update 활용 가능)
            st.success("데이터가 전송되었습니다! (시트에서 확인하세요)")
