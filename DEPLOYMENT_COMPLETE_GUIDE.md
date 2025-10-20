# 🚀 HƯỚNG DẪN HOÀN TẤT DEPLOYMENT

## ✅ ĐÃ LÀM XONG:
- ✅ Code đã push lên GitHub
- ✅ Railway project đã tạo (mahika-db)
- ✅ MySQL service đã chạy
- ✅ Web service đang deploy (railway up)

---

## 📋 CÁC BƯỚC CÒN LẠI (sau khi Railway build xong):

### BƯỚC 1: Kiểm tra Web Service đã deploy chưa (2-5 phút)

1. Mở Railway Dashboard: https://railway.app
2. Vào project "mahika-db"
3. Sẽ thấy 2 services:
   - **MySQL** (đã chạy)
   - **web** hoặc tên repo (đang build/deploy)
4. Click vào web service → tab **"Deployments"**
5. Đợi đến khi thấy:
   - Status: **"Success"** hoặc **"Active"** ✅
   - Hoặc **"Failed"** ❌ (nếu lỗi → xem logs)

### BƯỚC 2: Lấy domain của web

1. Trong web service → tab **"Settings"**
2. Phần **"Domains"**:
   - Nếu chưa có → click **"Generate Domain"**
   - Nếu có rồi → copy domain (ví dụ: `mahika-production.up.railway.app`)

### BƯỚC 3: Tạo bảng + Admin

**Cách 1: Dùng Railway CLI (từ máy bạn)**

```bash
# Sau khi web service deploy xong, chạy:
railway run python quick_init.py
```

Nếu thành công sẽ thấy: `✓ Tables created successfully!`

Sau đó tạo admin:

```bash
railway run python -c "
import sys
sys.path.insert(0, '.')
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    user = User.query.filter_by(email='admin@gmail.com').first()
    if not user:
        user = User(email='admin@gmail.com', is_verified=True, has_paid=True, is_admin=True)
        user.set_password('Admin@123')
        db.session.add(user)
    else:
        user.set_password('Admin@123')
        user.is_admin = True
        user.is_verified = True
        user.has_paid = True
    db.session.commit()
    print('✓ Admin created: admin@gmail.com / Admin@123')
"
```

**Cách 2: Dùng Railway Web Dashboard (nếu CLI không work)**

1. Vào MySQL service → tab "Database" → tab "Data"
2. Click nút **"Create table"**
3. Tạo 2 bảng theo file `SIMPLE_SETUP.sql`

Hoặc:

1. Click nút **"Connect"** (góc trên phải)
2. Chọn connect method (sẽ mở MySQL CLI hoặc query editor)
3. Copy/paste file `SIMPLE_SETUP.sql`

### BƯỚC 4: Cập nhật env variables cho production

Vào web service → **Variables** → sửa 2 biến này:

```bash
# Thay domain bạn vừa lấy ở bước 2
PAYOS_RETURN_URL=https://YOUR-DOMAIN.up.railway.app/payment/return
PAYOS_CANCEL_URL=https://YOUR-DOMAIN.up.railway.app/payment/cancel
```

Sau đó click **"Redeploy"** để áp dụng thay đổi.

### BƯỚC 5: Kiểm tra web

1. Mở: `https://YOUR-DOMAIN.up.railway.app`
2. Nếu thấy trang chủ Mahika → ✅ Thành công!
3. Click **"Đăng nhập"**
4. Nhập:
   - Email: `admin@gmail.com`
   - Password: `Admin@123`
5. Nếu đăng nhập thành công → ✅ HOÀN TẤT!

---

## 🔧 NẾU GẶP LỖI:

### Lỗi: "Application Error" hoặc "502 Bad Gateway"

1. Vào web service → **Logs**
2. Tìm dòng lỗi màu đỏ
3. Thường gặp:
   - **ModuleNotFoundError**: thiếu package trong `requirements.txt`
   - **Can't connect to MySQL**: `DATABASE_URL` chưa đúng
   - **Port binding error**: Railway cần `PORT` env var

**Fix:**
- Check `requirements.txt` có đầy đủ packages
- Check Variables có `DATABASE_URL`
- Đảm bảo `main.py` dùng `os.environ.get('PORT', 5000)`

### Lỗi: Không tạo được bảng

Nếu `railway run python quick_init.py` lỗi:

1. Vào Railway Dashboard → MySQL → Database → Data
2. Click **"Connect"** → chọn MySQL client
3. Chạy từng lệnh SQL trong `SIMPLE_SETUP.sql`

### Lỗi: Không đăng nhập được admin

Password hash có thể sai. Tạo lại:

```bash
# Local: tạo hash mới
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Admin@123'))"

# Copy hash ra
# Vào Railway MySQL → chạy SQL:
UPDATE users SET password_hash = 'HASH_VỪA_TẠO' WHERE email = 'admin@gmail.com';
```

---

## 📞 NEXT STEPS SAU KHI WEB CHẠY:

1. ✅ Đổi mật khẩu admin ngay
2. ✅ Test luồng đăng ký user mới
3. ✅ Test email verification (cần config Gmail)
4. ✅ Test PayOS payment (dùng sandbox keys)
5. ✅ Test download file (Google Drive link)
6. ✅ Thêm domain tùy chỉnh (nếu có)

---

## 🎯 CHECKLIST CUỐI CÙNG:

- [ ] Web service deploy thành công
- [ ] Domain đã generate
- [ ] Bảng users và payments đã tạo
- [ ] Admin user đã tạo (admin@gmail.com)
- [ ] Đăng nhập admin thành công
- [ ] PAYOS_RETURN_URL và CANCEL_URL đã đổi sang domain Railway
- [ ] Đã đổi mật khẩu admin

**DONE! 🎉**

---

## 💡 TIPS:

- **Logs quan trọng**: luôn check Logs khi có lỗi
- **Env variables**: không commit `.env` lên Git
- **Database backup**: Railway có auto backup, nhưng nên export định kỳ
- **Scaling**: Railway free tier giới hạn 500 hours/month
- **Monitoring**: dùng Railway metrics để xem traffic

Good luck! 🚀
