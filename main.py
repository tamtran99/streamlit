import streamlit as st

# Hiển thị link và nút
if st.button('Click here to see "KHOA MỘT LẰN"'):
    st.markdown('<p style="color: black; font-size: 20px;">KHOA MỘT LẰN</p>', unsafe_allow_html=True)
else:
    st.markdown('<a href="#" style="color: blue; font-size: 20px;">Click here to see "KHOA MỘT LẰN"</a>', unsafe_allow_html=True)
