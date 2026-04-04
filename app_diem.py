import pandas as pd
import streamlit as st
import os

# 1. Tự động tìm file Excel trong thư mục (để tránh sai tên file)
excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
FILE_PATH = excel_files[0] if excel_files else 'ELC3020_50K22.1_Diem.xlsx'

# Danh sách cột điểm (Copy chính xác từ file của bạn)
SCORE_COLUMNS = [
    'Diem_danh_1', 'Diem_danh_2', 'Kiem_tra_chuong_1', 
    'Kiem_tra_Tien_xu_ly_du_lieu', 'Kiem_tra_Data_mining', 
    'Thanh_phan_1', 'Bieu_do_nang_cao (15% TP2)', 
    'Tu_duy_phan_tich_xay_dung_dashboard (15% TP2)',
    'Thi_giua_ky (70% TP2)', 'Diem_cong_TP2 (x 1/3)', 'Thanh_phan_2'
]

@st.cache_data
def load_data():
    try:
        df = pd.read_excel(FILE_PATH)
        # Xóa khoảng trắng thừa trong tên cột
        df.columns = df.columns.str.strip()
        
        # Chuyển MSSV sang chuỗi và xóa khoảng trắng
        df['MSSV'] = df['MSSV'].astype(str).str.strip()
        
        # Ghép tên (Dùng cột Ho va ten dem và Ten)
        df['Họ và Tên'] = df['Ho va ten dem'].fillna('') + " " + df['Ten'].fillna('')
        
        # Làm tròn 1 chữ số thập phân cho các cột điểm
        for col in SCORE_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(1)
        return df
    except Exception as e:
        st.error(f"Lỗi đọc file: {e}")
        return None

# Hàm bôi đen và tô màu dòng quan trọng
def highlight_row(row):
    # Kiểm tra nếu tên thành phần là Thanh_phan_1 hoặc Thanh_phan_2
    if any(tp in row['Thành phần'] for tp in ['Thanh_phan_1', 'Thanh_phan_2']):
        return ['background-color: #f0f7ff; font-weight: bold; color: #1f77b4'] * len(row)
    return [''] * len(row)

# --- GIAO DIỆN ---
st.set_page_config(page_title="Tra cứu điểm ELC3020", layout="centered")
st.title('📊 Tra cứu Điểm ELC3020')
st.info("Khoa Thương mại điện tử - Đại học Kinh tế Đà Nẵng")

df = load_data()

if df is not None:
    mssv_input = st.text_input('Nhập Mã số sinh viên (MSSV):', placeholder='Ví dụ: 241124022129')

    if st.button('Xem kết quả', type="primary") or mssv_input:
        if mssv_input:
            # Tra cứu chính xác
            result = df[df['MSSV'] == mssv_input.strip()]
            
            if not result.empty:
                student = result.iloc[0]
                st.success(f"Sinh viên: **{student['Họ và Tên']}**")
                
                c1, c2 = st.columns(2)
                c1.write(f"**Lớp:** {student['Lop']}")
                c2.write(f"**MSSV:** {student['MSSV']}")
                
                st.divider()
                
                # Chuẩn bị bảng điểm dọc
                display_list = []
                for col in SCORE_COLUMNS:
                    if col in df.columns:
                        val = student[col]
                        # Thay dấu gạch dưới bằng khoảng trắng cho đẹp
                        clean_name = col.replace('_', ' ')
                        display_list.append({
                            "Thành phần": clean_name, 
                            "Điểm số": val if pd.notna(val) else "-"
                        })
                
                score_df = pd.DataFrame(display_list)
                
                # Áp dụng bôi đen
                styled_df = score_df.style.apply(highlight_row, axis=1)
                st.table(styled_df)
            else:
                st.error("Không tìm thấy MSSV này. Bạn vui lòng kiểm tra lại.")
        else:
            st.warning("Vui lòng nhập MSSV.")

st.divider()
st.caption("© 2026 - Giảng viên: Đỗ Hoàng Thu - DUE")
