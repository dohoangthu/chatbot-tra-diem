import pandas as pd
import streamlit as st

# 1. Đặt tên file Excel mới (chú ý tên file phải chính xác)
FILE_PATH = '261_ELC3020_diem.xlsx' 

# 2. CẬP NHẬT CÁC CỘT ĐIỂM MỚI
# Dựa trên file mới của bạn, tôi đã thay đổi danh sách này
SCORE_COLUMNS = [
    'Data_mining', 
    'Laptop_THPT', 
    'Tu_duy_Dashboard', 
    'Tien_xu_ly_du_lieu',
    'Bieu_do_nang_cao', 
    'Chuong1', 
    'Diem_danh', 
    'Diem_cong',
    # Các cột mới cập nhật
    'TP1_cu_(20%)', 
    'TP2_(cu_20%)', 
    'TP1_(moi_10%)', 
    'TP2_(moi_30%)'
]

# 3. Đọc file Excel
try:
    # Đọc file Excel
    df = pd.read_excel(FILE_PATH)
    
    # Chuẩn hóa tên cột: Xóa khoảng trắng thừa ở đầu/cuối tên cột (nếu có) để tránh lỗi
    df.columns = df.columns.str.strip()
    
    # Đảm bảo cột MSSV (MSV) có định dạng chuỗi
    df['MSV'] = df['MSV'].astype(str)

except FileNotFoundError:
    st.error(f"Lỗi nghiêm trọng: Không tìm thấy file '{FILE_PATH}'.")
    st.error("Vui lòng kiểm tra lại tên file và đảm bảo nó nằm cùng thư mục với code.")
    st.stop()
except Exception as e:
    st.error(f"Lỗi khi đọc file Excel: {e}")
    st.stop()

# 4. Hàm tra cứu
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
        
        # Lấy điểm số, xử lý trường hợp cột không tồn tại để tránh crash ứng dụng
        scores = {}
        for col in SCORE_COLUMNS:
            if col in result.columns:
                scores[col] = result[col].iloc[0]
            else:
                scores[col] = "Không có dữ liệu" # Hoặc để trống tùy bạn

        return {
            'MSSV': mssv_input,
            'Họ và Tên': ten,
            'Lớp': lop,
            'Điểm số': scores
        }
    else:
        return None

# 5. Giao diện Streamlit
st.set_page_config(page_title="Tra Cứu Điểm ELC3020", page_icon="🎓")

st.title('🤖 Tra Cứu Điểm_ELC3020')
st.markdown('---')

st.header('Nhập Mã Số Sinh Viên (MSSV)')

mssv_input = st.text_input('MSSV của bạn:', placeholder='Ví dụ: 221121302202')

if st.button('Tra Cứu Điểm', type="primary"):
    if mssv_input:
        with st.spinner('Đang tìm kiếm...'):
            data = lookup_scores(mssv_input)
            
            if data:
                st.success(f'✅ Tìm thấy: **{data["Họ và Tên"]}** - Lớp **{data["Lớp"]}**')
                
                st.subheader('Bảng Điểm Chi Tiết')
                
                # Tạo DataFrame từ dict điểm số
                score_df = pd.DataFrame(list(data['Điểm số'].items()), columns=['Thành Phần', 'Điểm'])
                
                # Định dạng hiển thị bảng cho đẹp hơn
                st.dataframe(
                    score_df, 
                    hide_index=True, 
                    use_container_width=True
                )
                
            else:
                st.error(f'❌ Không tìm thấy dữ liệu cho MSSV: **{mssv_input}**.')
    else:
        st.warning('⚠️ Vui lòng nhập Mã Số Sinh Viên.')