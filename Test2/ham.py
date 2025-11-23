# trong file ham.py
import pyodbc
from werkzeug.security import check_password_hash, generate_password_hash # Rất quan trọng cho bảo mật

# --- Cấu hình kết nối MS SQL Server ---
# (Hãy đảm bảo bạn đã cài đặt ODBC Driver for SQL Server)
def get_db_connection():
    DB_CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=QLNS;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(DB_CONN_STR)


# --- Hàm kiểm tra đăng nhập và lấy quyền ---
# Đây là hàm quan trọng nhất
# trong ham.py

# Trong file ham.py
# (Nhớ import thư viện: from werkzeug.security import check_password_hash)

def kiem_tra_dang_nhap(username, password):
    print("----- BẮT ĐẦU KIỂM TRA ĐĂNG NHẬP -----")
    print(f"Tài khoản nhận được: {username}")
    print(f"Mật khẩu nhận được: {password}")

    conn = get_db_connection()
    if not conn:
        print("[LỖI] Không thể kết nối DB.")
        return None, None

    cursor = conn.cursor()
    sql_query = """
        SELECT A.MaNV, A.MatKhau, C.MucQuyenHan
        FROM Account AS A
        INNER JOIN Employee AS E ON A.MaNV = E.MaNV
        INNER JOIN ChucVu AS C ON E.RoleID = C.RoleID
        WHERE A.TaiKhoan = ?
    """
    
    try:
        cursor.execute(sql_query, (username,))
        user_data = cursor.fetchone()
        
        if user_data:
            print(f"[THÀNH CÔNG] Tìm thấy dữ liệu: {user_data}")
        else:
            print("[THẤT BẠI] Không tìm thấy dữ liệu. (Lỗi JOIN hoặc Sai TaiKhoan)")
            print("----- KẾT THÚC KIỂM TRA -----")
            return None, None

        ma_nv = user_data.MaNV
        # Đổi tên biến cho rõ nghĩa: đây là mật khẩu thô
        password_from_db = user_data.MatKhau
        quyen_han = user_data.MucQuyenHan
        
        print(f"Mật khẩu trong DB: {password_from_db}")

        # --- BẮT ĐẦU SỬA LỖI ---

        # (BÌNH LUẬN KHỐI NÀY VÌ BẠN KHÔNG DÙNG HASH)
        # if check_password_hash(password_from_db, password):
        #     print("[THÀNH CÔNG] Mật khẩu KHỚP.")
        #     print("----- KẾT THÚC KIỂM TRA -----")
        #     return ma_nv, quyen_han
        # else:
        #     print("[THẤT BẠI] Mật khẩu KHÔNG KHỚP.")
        #     print("----- KẾT THÚC KIỂM TRA -----")
        #     return None, None
            
        # (BỎ BÌNH LUẬN KHỐI NÀY VÌ BẠN DÙNG MẬT KHẨU THÔ)
        if password_from_db == password:
            print("[THÀNH CÔNG] Mật khẩu thô KHỚP.")
            print("----- KẾT THÚC KIỂM TRA -----")
            return ma_nv, quyen_han
        else:
            print("[THẤT BẠI] Mật khẩu thô KHÔNG KHỚP.")
            print("----- KẾT THÚC KIỂM TRA -----")
            return None, None
        
        # --- KẾT THÚC SỬA LỖI ---

    except Exception as e:
        print(f"[LỖI] Lỗi exception khi query: {e}")
        return None, None
    finally:
        print("Đóng kết nối DB.")
        cursor.close()
        conn.close()
        
# --- (Tùy chọn) Hàm để tạo mật khẩu băm ---
# Bạn dùng hàm này khi tạo tài khoản mới
def tao_mat_khau_bam(password):
    return generate_password_hash(password)

# trong file ham.py (thêm vào)

def lay_thong_tin_ca_nhan(ma_nv):
    """
    Lấy tất cả thông tin của một nhân viên từ MaNV.
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    # Lấy thông tin từ bảng Employee dựa trên ERD của bạn
    sql_query = """
        SELECT MaNV, HoTen, NamSinh, DiaChi, SoDienThoai, email
        FROM Employee
        WHERE MaNV = ?
    """
    
    try:
        cursor.execute(sql_query, (ma_nv,))
        # fetchone() trả về một đối tượng Row, có thể truy cập bằng tên cột
        employee_data = cursor.fetchone()
        return employee_data
    except Exception as e:
        print(f"Lỗi khi lấy thông tin nhân viên: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def cap_nhat_thong_tin_ca_nhan(ma_nv, dia_chi, sdt, email):
    """
    Cập nhật các thông tin cho phép chỉnh sửa của nhân viên.
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    sql_update = """
        UPDATE Employee
        SET DiaChi = ?, SoDienThoai = ?, email = ?
        WHERE MaNV = ?
    """
    
    try:
        cursor.execute(sql_update, (dia_chi, sdt, email, ma_nv))
        conn.commit() # Rất quan trọng: Phải commit sau khi UPDATE
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật thông tin: {e}")
        conn.rollback() # Hoàn tác nếu có lỗi
        return False
    finally:
        cursor.close()
        conn.close()
        
    