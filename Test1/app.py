from flask import Flask, render_template, request, redirect, session, url_for
from ham import kiem_tra_tai_khoan

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = kiem_tra_tai_khoan(username, password)
        if user:
            session['MaNV'] = user['MaNV']
            session['RoleID'] = user['RoleID']
            if user['RoleID'] == 1:  # 1 = Admin
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('employee_home'))
        else:
            return render_template('login.html', error='Sai tài khoản hoặc mật khẩu!')
    return render_template('login.html')

@app.route('/employee')
def employee_home():
    return render_template('employee/dashboard.html')

@app.route('/admin')
def admin_home():
    return render_template('admin/dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
