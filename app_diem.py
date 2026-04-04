import pandas as pd
import streamlit as st

# 1. Cấu hình file (Bạn có thể đổi tên file tại đây cho khớp với GitHub)
FILE_PATH = 'ELC3020_50K22.1_Diem.xlsx' 

# Danh sách các cột điểm cần xử lý
SCORE_COLUMNS = [
    'Diem_danh_1', 
    'Diem_danh_2', 
    'Kiem_tra_chuong_1', 
    'Kiem_tra_Tien_xu_ly_du_lieu',
    'Kiem_tra_Data_mining', 
    'Thanh_phan_1', 
    'Bieu_do_nang_cao (15% TP2)', 
    'Tu_duy_phan_tich_xay_dung_dashboard (15% TP2)',
    'Thi_giua_ky (70% TP2)', 
    'Diem_cong_TP2 (x 1/3)', 
    'Thanh_phan_2'
]

@st.cache_data
def load_data():
    try:
        # Đọc file Excel
        df = pd.read_excel(FILE_PATH)
        df.columns = df.columns.str.strip()
        
        # Chuyển MSSV sang chuỗi
        df['MSSV'] = df['MSSV'].astype(str)
        
        # Ghép Họ và Tên
        df['Họ và Tên'] = df['Ho va ten dem'].fillna('') + " " + df['Ten'].fillna('')
        
        # --- LÀM TRÒN ĐIỂM: 1 chữ số thập phân ---
        for col in SCORE_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(1)
                
        return df
    except Exception as e:
        st.error(f"Lỗi: {e}")
        return None

# Hàm định dạng: Bôi đen và tô màu nền cho dòng quan trọng
def style_row(row):
    targets = ['Thanh_phan_1', 'Thanh_phan_2']
    if row['Thành phần'] in targets:
        # Trả về style in đậm và nền vàng nhạt cho toàn bộ dòng
        return ['font-weight: bold; background-color: #fff4cc; color: #d73a49'] * len(row)
    return [''] * len(row)

# --- GIAO DIỆN ---
st.set_page_config(page_title="Tra cứu điểm DUE", layout="centered")

st.title('📊 Tra cứu Điểm ELC3020')
st.markdown('**DUE - Khoa Thương mại điện tử**')

df = load_data()

if df is not None:
    mssv_input = st.text_input('Nhập Mã số sinh viên (MSSV):', placeholder='Ví dụ: 241124022129')

    if st.button('Tìm kiếm', type="primary") or mssv_input:
        if mssv_input:
            result = df[df['MSSV'] == mssv_input.strip()]
            
            if not result.empty:
                student = result.iloc[0]
                st.success(f"Sinh viên: **{student['Họ và Tên']}**")
                
                # Hiển thị thông tin cơ bản bằng cột
                c1, c2 = st.columns(2)
                c1.write(f"**Lớp:** {student['Lop']}")
                c2.write(f"**MSSV:** {student['MSSV']}")
                
                st.divider()
                
                # Chuyển bảng điểm sang dạng dọc để dễ xem trên mobile
                display_list = []
                for col in SCORE_COLUMNS:
                    if col in df.columns:
                        val = student[col]
                        display_list.append({
                            "Thành phần": col.replace('_', ' '), 
                            "Điểm số": val if pd.notna(val) else "-"
                        })
                
                score_df = pd.DataFrame(display_list)

                # Áp dụng bôi đen/màu sắc
                styled_df = score_df.style.apply(style_row, axis=1)
                
                # Hiển thị bảng
                st.table(styled_df)
                
            else:
                st.error("Không tìm thấy MSSV này. Bạn vui lòng kiểm tra lại mã số.")

st.markdown("---")
st.caption("Dữ liệu được cập nhật từ file giảng viên.")
