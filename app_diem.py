import pandas as pd
import streamlit as st

# 1. Đặt tên file Excel gốc của bạn ở đây
# Đảm bảo file này nằm CÙNG THƯ MỤC với file app.py
FILE_PATH = '261_ELC3020_diem.xlsx' 

# 2. Các cột điểm bạn muốn hiển thị (giữ nguyên)
SCORE_COLUMNS = [
    'Data_mining', 'Laptop_THPT', 'Tu_duy_Dashboard', 'Tien_xu_ly_du_lieu',
    'Bieu_do_nang_cao', 'Chuong1', 'Diem_danh', 'Diem_cong',
    'Diem_qua_trinh', 'Diem_giua_ky'
]

# 3. Đọc file Excel (thay vì CSV)
try:
    df = pd.read_excel(FILE_PATH)
    
    # Đảm bảo cột MSSV (MSV) có định dạng chuỗi (rất quan trọng)
    df['MSV'] = df['MSV'].astype(str)

except FileNotFoundError:
    # Báo lỗi nếu không tìm thấy file
    st.error(f"Lỗi nghiêm trọng: Không tìm thấy file '{FILE_PATH}'.")
    st.error("Vui lòng kiểm tra lại tên file và đảm bảo nó nằm cùng thư mục với code.")
    st.stop() # Dừng ứng dụng nếu không có file
except Exception as e:
    st.error(f"Lỗi khi đọc file Excel: {e}")
    st.stop()


# 4. Hàm tra cứu (Không thay đổi)
def lookup_scores(mssv_input):
    """
    Hàm tra cứu điểm dựa trên MSSV.
    """
    mssv_input = str(mssv_input).strip()
    
    # Lọc DataFrame
    result = df[df['MSV'] == mssv_input]
    
    if not result.empty:
        # Lấy thông tin
        ten = result['Ho_va_ten_dem'].iloc[0] + ' ' + result['Ten'].iloc[0]
        lop = result['Lop'].iloc[0]
        scores = result[SCORE_COLUMNS].iloc[0].to_dict()
        
        return {
            'MSSV': mssv_input,
            'Họ và Tên': ten,
            'Lớp': lop,
            'Điểm số': scores
        }
    else:
        return None

# 5. Giao diện Streamlit (Không thay đổi)
st.title('🤖 Chatbot Tra Cứu Điểm Số (Excel)')
st.markdown('---')

st.header('Nhập Mã Số Sinh Viên (MSSV)')

mssv_input = st.text_input('MSSV của bạn:', placeholder='Ví dụ: 221121302202')

if st.button('Tra Cứu Điểm'):
    if mssv_input:
        with st.spinner('Đang tìm kiếm...'):
            data = lookup_scores(mssv_input)
            
            if data:
                st.success(f'✅ Tìm thấy thông tin của sinh viên: **{data["Họ và Tên"]}** - Lớp **{data["Lớp"]}**')
                
                st.subheader('Bảng Điểm Chi Tiết')
                score_df = pd.DataFrame(data['Điểm số'].items(), columns=['Mục Điểm', 'Kết Quả'])
                st.dataframe(score_df, hide_index=True)
                
            else:
                st.error(f'❌ Không tìm thấy điểm số cho MSSV: **{mssv_input}**.')
    else:
        st.warning('Vui lòng nhập Mã Số Sinh Viên để tra cứu.')