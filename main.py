import streamlit as st

# Tiêu đề
st.title('Tạo Tương Tác Với Chữ "KHOA MỘT LẰN"')

# Thêm một expander cho người dùng để mở rộng phần hướng dẫn
with st.expander("Nhấn để xem hướng dẫn"):
    st.write("Nhấn nút dưới đây để hiển thị chữ 'KHOA MỘT LẰN'.")

# Tạo một nút bấm để người dùng nhấn
if st.button('Nhấn vào đây để xem "KHOA MỘT LẰN"'):
    st.markdown('<p style="color: black; font-size: 40px; font-weight: bold;">KHOA MỘT LẰN</p>', unsafe_allow_html=True)
    st.balloons()  # Hiệu ứng bong bóng khi nhấn nút

# Thêm một selectbox để thay đổi kích thước chữ
font_size = st.selectbox("Chọn kích thước chữ", [20, 30, 40, 50], index=2)

# Hiển thị chữ "KHOA MỘT LẰN" với kích thước tùy chọn
if font_size:
    st.markdown(f'<p style="color: black; font-size: {font_size}px; font-weight: bold;">KHOA MỘT LẰN</p>', unsafe_allow_html=True)

# Đưa ra một hướng dẫn thêm bằng cách sử dụng slider
st.slider('Chỉnh độ đậm nhạt của chữ', 0, 100, 50)
