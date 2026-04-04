import pandas as pd
import streamlit as st

# 1. Cấu hình file và cột
FILE_PATH = 'ELC3020_50K22.1_Diem.xlsx' 

SCORE_COLUMNS = [
    'Diem_danh_1', 
    'Diem_danh_2', 
    'Kiem_tra_chuong_1', 
    'Kiem_tra_Tien_xu_ly_du_lieu',
    'Kiem_tra_Data_mining', 
    'Thanh_phan_1',  # Cột cần bôi đậm
    'Bieu_do_nang_cao (15% TP2)', 
    'Tu_duy_phan_tich_xay_dung_dashboard (15% TP2)',
    'Thi_giua_ky (70% TP2)', 
    'Diem_cong_TP2 (x 1/3)', 
    'Thanh_phan_2'   # Cột cần bôi đậm
]

@st.cache_data
def load_data():
    try:
        df = pd.read_excel(FILE_PATH)
        df.columns = df.columns.str.strip()
        df['MSSV'] = df['MSSV'].astype(str)
        df['Họ và Tên'] = df['Ho va ten dem'].fillna('') + " " + df['Ten'].fillna('')
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc file: {e}")
        return None

# Hàm để định dạng in đậm dòng cụ thể
def highlight_important_rows(row):
    # Nếu tên thành phần là Thanh_phan_1 hoặc Thanh_phan_2 thì in đậm
    if row['Thành phần'] in ['Thanh_phan_1', 'Thanh_phan_2']:
        return ['font-weight: bold; background-color: #f0f2f6'] * len(row)
    return [''] * len(row)

# 2. Giao diện ứng dụng
st.set_page_config(page_title="Tra cứu điểm", page_icon="🎓")

st.title('🎓 Tra cứu Điểm ELC3020')
st.markdown('**Khoa Thương mại điện tử - Đại học Kinh tế Đà Nẵng**')

df = load_data()

if df is not None:
    mssv_input = st.text_input('Nhập Mã số sinh viên (MSSV):', placeholder='Ví dụ: 241124022129')

    if st.button('Tra cứu', type="primary"):
        if mssv_input:
            result = df[df['MSSV'] == mssv_input.strip()]
            
            if not result.empty:
                student = result.iloc[0]
                st.success(f"✅ Sinh viên: **{student['Họ và Tên']}**")
                
                col1, col2 = st.columns(2)
                col1.metric("Lớp", student['Lop'])
                col2.metric("MSSV", student['MSSV'])
                
                st.divider()
                st.subheader('📊 Bảng điểm chi tiết')
                
                # Tạo DataFrame để hiển thị dọc cho dễ nhìn trên điện thoại
                display_data = []
                for col in SCORE_COLUMNS:
                    if col in df.columns:
                        val = student[col]
                        display_val = val if pd.notna(val) else "-"
                        display_data.append({"Thành phần": col, "Điểm": display_val})
                
                score_df = pd.DataFrame(display_data)

                # Áp dụng hàm bôi đậm và hiển thị
                styled_df = score_df.style.apply(highlight_important_rows, axis=1)
                
                # Sử dụng st.table để hiển thị bảng tĩnh và rõ ràng
                st.table(styled_df)
                
            else:
                st.warning("⚠️ Không tìm thấy MSSV này. Vui lòng kiểm tra lại.")

st.markdown("---")
st.caption("Tra cứu điểm học phần Nhập môn KH DL trong Kinh doanh.")
