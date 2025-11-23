# trong file app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import ham 


app = Flask(__name__)
# Đây là khóa bí mật để mã hóa session, hãy đổi thành một chuỗi ngẫu nhiên
app.secret_key = 'your_very_secret_random_key_here'

# --- Decorator để bảo vệ trang ---
# Trang này yêu cầu đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để tiếp tục.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Trang này chỉ cho phép Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Logic MỚI: Nếu bạn là 'NhanVien', bạn bị CHẶN.
        if session.get('role') == 'NhanVien': 
            flash('Bạn không có quyền truy cập trang này.', 'danger')
            return redirect(url_for('trang_nhan_vien'))
        # Nếu không phải 'NhanVien' (ví dụ: QuanLyCapCao), bạn được VÀO.
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---
@app.route('/')
def index():
    # Nếu đã đăng nhập, chuyển hướng luôn, không cần vào trang login
    if 'user_id' in session:
        if session.get('role') == 'Admin':
            return redirect(url_for('trang_quan_tri'))
        else:
            return redirect(url_for('trang_nhan_vien'))
    # Nếu chưa, thì tới trang login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Gọi hàm từ ham.py
        ma_nv, quyen_han = ham.kiem_tra_dang_nhap(username, password)
        
        if ma_nv and quyen_han:
            session['user_id'] = ma_nv
            session['role'] = quyen_han
            
            # ===== ĐÂY LÀ LOGIC ĐÚNG =====
            if quyen_han == 'NhanVien':
                # Nếu LÀ Nhân viên -> đi tới trang NHÂN VIÊN
                flash(f'Đăng nhập thành công, chào mừng nhân viên {ma_nv}!', 'success')
                return redirect(url_for('trang_nhan_vien'))
            else:
                # Nếu KHÔNG LÀ Nhân viên (tức là 'QuanLyCapCao', v.v.) -> đi tới trang ADMIN
                flash('Đăng nhập thành công với tư cách Quản lý!', 'success')
                return redirect(url_for('trang_quan_tri'))
        
        else:
            # Đăng nhập thất bại
            flash('Tài khoản hoặc mật khẩu không chính xác.', 'danger')
            return render_template('login.html') # Tải lại trang login

    # Nếu là request GET, chỉ hiển thị trang login
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('login'))

# --- Các trang được bảo vệ ---

@app.route('/admin/dashboard')
@login_required
@admin_required # Chỉ Admin được vào
def trang_quan_tri():
    # Trang này sẽ load layout.html và hiển thị nội dung của Admin
    # Ví dụ: Quản lý tài khoản, xem báo cáo, v.v.
    return render_template('admin_dashboard.html')

@app.route('/employee/dashboard', methods=['GET', 'POST']) # Thêm methods
@login_required
def trang_nhan_vien():
    # Lấy MaNV của người đang đăng nhập từ session
    ma_nv = session.get('user_id')
    if not ma_nv:
        flash('Lỗi phiên đăng nhập, vui lòng đăng nhập lại.', 'danger')
        return redirect(url_for('login'))

    # --- Xử lý khi người dùng GỬI (submit) form ---
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        dia_chi = request.form['dia_chi']
        sdt = request.form['sdt']
        email = request.form['email']
        
        # Gọi hàm cập nhật từ ham.py
        success = ham.cap_nhat_thong_tin_ca_nhan(ma_nv, dia_chi, sdt, email)
        
        if success:
            flash('Cập nhật thông tin cá nhân thành công!', 'success')
        else:
            flash('Có lỗi xảy ra, không thể cập nhật.', 'danger')
        
        # Tải lại trang để thấy thay đổi (hoặc ở lại)
        return redirect(url_for('trang_nhan_vien'))

    # --- Xử lý khi người dùng TẢI (load) trang (mặc định là GET) ---
    # Lấy thông tin nhân viên để hiển thị
    employee_data = ham.lay_thong_tin_ca_nhan(ma_nv)
    
    if not employee_data:
        flash('Không tìm thấy thông tin nhân viên.', 'danger')
        return redirect(url_for('logout')) # Hoặc một trang lỗi

    # Truyền dữ liệu nhân viên vào template
    return render_template('employee_dashboard.html', employee=employee_data)

# Thêm các route khác cho "Bảng Lương", "Cài Đặt" ở đây
# Ví dụ:
@app.route('/salary')
@login_required
def bang_luong():
    # Lấy MaNV từ session
    ma_nv = session['user_id']
    # Gọi hàm từ ham.py để lấy lương (ví dụ: data = ham.lay_bang_luong(ma_nv))
    # ...
    return render_template('bang_luong.html', salary_data=data)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)