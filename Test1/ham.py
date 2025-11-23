import pyodbc


DB_CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=QLNS;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

def get_connection():
    return pyodbc.connect(DB_CONN_STR)


def kiem_tra_tai_khoan(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT A.MaNV, A.RoleID, E.HoTen
        FROM Account A
        JOIN Employee E ON A.MaNV = E.MaNV
        WHERE A.TaiKhoan = ? AND A.MatKhau = ?
    """
    cursor.execute(query, (username, password))
    row = cursor.fetchone()
    if row:
        return {'MaNV': row.MaNV, 'RoleID': row.RoleID, 'HoTen': row.HoTen}
    return None

# Lấy thông tin cá nhân nhân viên
def get_thong_tin_nv(manv):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Employee WHERE MaNV = ?"
    cursor.execute(query, (manv,))
    row = cursor.fetchone()
    if row:
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))
    return None

# Admin: Lấy danh sách nhân viên
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
