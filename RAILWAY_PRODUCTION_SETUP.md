# 🚀 HƯỚNG DẪN CẤU HÌNH RAILWAY PRODUCTION

## ⚠️ CÁC LỖI THƯỜNG GẶP

### 1. Lỗi Database Connection Refused

```
Can't connect to MySQL server on 'localhost' ([Errno 111] Connection refused)
```

**Nguyên nhân:** Chưa cấu hình biến môi trường DATABASE_URL trên Railway

### 2. Lỗi Email không gửi được

**Nguyên nhân:** Chưa cấu hình biến môi trường MAIL_USERNAME, MAIL_PASSWORD

---

## 📋 BƯỚC 1: CẤU HÌNH DATABASE

### Cách 1: Sử dụng MySQL Plugin của Railway (KHUYÊN DÙNG)

1. **Thêm MySQL Database vào project:**

   - Vào Railway Dashboard → Project của bạn
   - Click **"New"** → **"Database"** → **"Add MySQL"**
   - Railway sẽ tự động tạo MySQL database

2. **Link MySQL service với Web service:**

   - Click vào service **web app** của bạn (không phải MySQL service)
   - Vào tab **"Variables"**
   - Click **"New Variable"** → **"Add Reference"**
   - Chọn MySQL service
   - Chọn biến **`DATABASE_URL`** hoặc **`MYSQL_URL`**
   - Click **"Add"**

3. **Kiểm tra biến môi trường:**
   - Trong tab Variables của web service, bạn sẽ thấy:
     ```
     DATABASE_URL = ${{MySQL.DATABASE_URL}}
     ```
   - Hoặc các biến riêng lẻ:
     ```
     MYSQLHOST
     MYSQLPORT
     MYSQLDATABASE
     MYSQLUSER
     MYSQLPASSWORD
     ```

### Cách 2: Sử dụng MySQL External (nếu bạn có DB riêng)

Nếu bạn đã có MySQL database từ nơi khác, thêm các biến này vào Railway:

```bash
DATABASE_URL=mysql://username:password@host:3306/database_name
```

Hoặc từng biến riêng:

```bash
DB_HOST=your-mysql-host.com
DB_PORT=3306
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

---

## 📧 BƯỚC 2: CẤU HÌNH EMAIL (Gmail)

### 2.1. Tạo App Password cho Gmail

1. **Đăng nhập Gmail** của bạn
2. **Vào Google Account Settings**: https://myaccount.google.com/
3. **Bật 2-Step Verification** (nếu chưa bật):
   - Security → 2-Step Verification → Turn On
4. **Tạo App Password**:
   - Security → 2-Step Verification → App passwords
   - Select app: **"Mail"**
   - Select device: **"Other (Custom name)"** → Nhập "Mahika App"
   - Click **"Generate"**
   - Copy mật khẩu 16 ký tự (ví dụ: `abcd efgh ijkl mnop`)

### 2.2. Thêm biến môi trường vào Railway

Vào tab **"Variables"** của web service và thêm:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcdefghijklmnop  # App Password (bỏ khoảng trắng)
```

⚠️ **LƯU Ý:**

- `MAIL_PASSWORD` phải là **App Password** (16 ký tự), KHÔNG phải mật khẩu Gmail thường
- Bỏ hết khoảng trắng trong App Password

---

## 🔐 BƯỚC 3: CẤU HÌNH CÁC BIẾN BẢO MẬT KHÁC

Thêm các biến sau vào Railway Variables:

### Secret Key (BẮT BUỘC)

```bash
SECRET_KEY=your-super-secret-random-key-here-change-this
```

💡 **Tạo Secret Key ngẫu nhiên:**

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### PayOS Configuration (nếu dùng payment)

```bash
PAYOS_CLIENT_ID=your-client-id
PAYOS_API_KEY=your-api-key
PAYOS_CHECKSUM_KEY=your-checksum-key
PAYOS_RETURN_URL=https://your-domain.railway.app/payment/return
PAYOS_CANCEL_URL=https://your-domain.railway.app/payment/cancel
```

### Download File Configuration

```bash
DOWNLOAD_FILE_URL=your-google-drive-direct-download-url
DOWNLOAD_FILE_NAME=App.exe
PAYMENT_AMOUNT=50000
```

---

## ✅ BƯỚC 4: KHỞI TẠO DATABASE

Sau khi cấu hình xong, bạn cần tạo tables trong database:

### Option 1: Sử dụng Railway Shell

1. Vào web service → Click **"..."** → **"Shell"**
2. Chạy lệnh:

```bash
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### Option 2: Chạy script từ local

1. Tải biến môi trường từ Railway:

   - Click web service → Variables → **"Raw Editor"**
   - Copy tất cả
   - Paste vào file `.env` local

2. Chạy script:

```bash
python3 recreate_db.py
```

---

## 👤 BƯỚC 5: TẠO ADMIN USER

Sau khi database đã có tables, tạo admin user:

### Option 1: Qua Railway Shell

```bash
python3 create_admin.py
```

### Option 2: Qua Local (với .env từ Railway)

```bash
python3 create_admin.py
```

---

## 🧪 BƯỚC 6: KIỂM TRA

### 6.1. Kiểm tra Database

```bash
python3 test_railway_connection.py
```

### 6.2. Kiểm tra Email

Đăng ký tài khoản mới trên website → Kiểm tra email có nhận được không

### 6.3. Kiểm tra Logs

Vào Railway Dashboard → Service → **"Logs"** để xem log runtime

---

## 📝 DANH SÁCH BIẾN MÔI TRƯỜNG ĐẦY ĐỦ

Copy template này và điền thông tin của bạn:

```bash
# Database (Railway MySQL sẽ tự động set)
DATABASE_URL=${{MySQL.DATABASE_URL}}

# Security
SECRET_KEY=your-64-character-random-string-here

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password

# PayOS
PAYOS_CLIENT_ID=your-client-id
PAYOS_API_KEY=your-api-key
PAYOS_CHECKSUM_KEY=your-checksum-key
PAYOS_RETURN_URL=https://your-domain.railway.app/payment/return
PAYOS_CANCEL_URL=https://your-domain.railway.app/payment/cancel

# Download
DOWNLOAD_FILE_URL=your-google-drive-url
DOWNLOAD_FILE_NAME=App.exe
PAYMENT_AMOUNT=50000

# Optional
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: Database không connect

- ✅ Kiểm tra MySQL service đã running chưa
- ✅ Kiểm tra biến `DATABASE_URL` đã được set
- ✅ Restart web service sau khi thêm biến

### Lỗi: Email không gửi được

- ✅ Kiểm tra đã bật 2-Step Verification
- ✅ Kiểm tra App Password không có khoảng trắng
- ✅ Kiểm tra MAIL_USERNAME là email đúng
- ✅ Thử gửi email test từ Gmail thường xem có bị block không

### Lỗi: 500 Internal Server Error

- ✅ Xem Logs trên Railway
- ✅ Kiểm tra tất cả biến môi trường đã đủ
- ✅ Kiểm tra database đã có tables

### Database tables chưa tồn tại

```bash
# Vào Railway Shell và chạy:
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## 📞 HỖ TRỢ

Nếu vẫn gặp lỗi, check:

1. **Logs** trên Railway Dashboard
2. **Variables** đã đủ và đúng chưa
3. **MySQL service** có đang running không
4. Thử redeploy lại web service

---

**Cập nhật:** October 2025
**Version:** 1.0
