# ✅ CHECKLIST FIX LỖI RAILWAY PRODUCTION

## 🔴 VẤN ĐỀ HIỆN TẠI
- ❌ Database connection refused (localhost)
- ❌ Email timeout (16 giây → HTTP 499)
- ❌ App không chạy được trên Railway

---

## 📝 CHECKLIST FIX (Làm theo thứ tự)

### ☑️ 1. FIX CODE (ĐÃ XONG - Commit & Push)
- [x] Thêm error handling cho email sending
- [x] Thêm timeout cho SMTP (10 giây)
- [x] App không bị crash khi email fail
- [x] Tạo script test email

**📤 Action:** 
```bash
git add .
git commit -m "Fix: Add email error handling and timeout to prevent hanging"
git push origin main
```

---

### ☑️ 2. CẤU HÌNH RAILWAY DATABASE

**Vào Railway Dashboard → Your Project**

- [ ] **2.1. Thêm MySQL Database**
  - Click "New" → "Database" → "Add MySQL"
  - Đợi MySQL deploy xong (khoảng 1-2 phút)

- [ ] **2.2. Link Database với Web Service**
  - Click vào **web service** (không phải MySQL service)
  - Tab "Variables"
  - Click "New Variable" → "Add Reference"
  - Chọn: MySQL service
  - Chọn biến: `DATABASE_URL`
  - Click "Add"

- [ ] **2.3. Verify**
  - Trong Variables tab, sẽ thấy:
    ```
    DATABASE_URL = ${{MySQL.DATABASE_URL}}
    ```

---

### ☑️ 3. CẤU HÌNH EMAIL (Gmail)

- [ ] **3.1. Tạo App Password**
  1. Vào: https://myaccount.google.com/
  2. Bên trái: "Security"
  3. Tìm "2-Step Verification" → Bật (nếu chưa có)
  4. Quay lại "Security" → "2-Step Verification"
  5. Scroll xuống → "App passwords"
  6. Select app: "Mail"
  7. Select device: "Other" → Nhập "Mahika"
  8. Click "Generate"
  9. **Copy mật khẩu 16 ký tự** (VD: abcd efgh ijkl mnop)
  10. Bỏ hết khoảng trắng → `abcdefghijklmnop`

- [ ] **3.2. Thêm vào Railway Variables**
  - Vào web service → Tab "Variables"
  - Thêm từng biến:
    ```
    MAIL_SERVER = smtp.gmail.com
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = your-email@gmail.com
    MAIL_PASSWORD = abcdefghijklmnop
    ```
  - ⚠️ `MAIL_PASSWORD` phải là App Password 16 ký tự, KHÔNG phải password Gmail thường!

---

### ☑️ 4. CẤU HÌNH CÁC BIẾN KHÁC

**Vào Railway Variables, thêm:**

- [ ] **4.1. Secret Key** (BẮT BUỘC)
  ```bash
  # Tạo secret key:
  python3 -c "import secrets; print(secrets.token_hex(32))"
  
  # Copy kết quả và add vào Railway:
  SECRET_KEY = <paste-secret-key-here>
  ```

- [ ] **4.2. PayOS** (nếu dùng payment)
  ```
  PAYOS_CLIENT_ID = your-client-id
  PAYOS_API_KEY = your-api-key  
  PAYOS_CHECKSUM_KEY = your-checksum-key
  PAYOS_RETURN_URL = https://mahika-website.up.railway.app/payment/return
  PAYOS_CANCEL_URL = https://mahika-website.up.railway.app/payment/cancel
  ```

- [ ] **4.3. Download Files**
  ```
  DOWNLOAD_FILE_URL = your-google-drive-url
  DOWNLOAD_FILE_NAME = App.exe
  PAYMENT_AMOUNT = 50000
  ```

---

### ☑️ 5. KHỞI TẠO DATABASE

- [ ] **5.1. Vào Railway Shell**
  - Click web service → Menu "..." → "Shell"

- [ ] **5.2. Tạo tables**
  ```bash
  python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Database initialized!')"
  ```

- [ ] **5.3. Tạo admin user**
  ```bash
  python3 create_admin.py
  ```

---

### ☑️ 6. RESTART & TEST

- [ ] **6.1. Restart Web Service**
  - Click web service → Menu "..." → "Restart"
  - Đợi service deploy lại (1-2 phút)

- [ ] **6.2. Test Website**
  - Vào: https://mahika-website.up.railway.app
  - Thử register tài khoản mới
  - Kiểm tra email có nhận được không

- [ ] **6.3. Kiểm tra Logs**
  - Click web service → Tab "Logs"
  - Xem có lỗi gì không

---

## 🧪 TEST LOCAL TRƯỚC KHI DEPLOY

### Test Email (Local)
```bash
# Tạo file .env với các biến email
cp .env.example .env  # Nếu có
# Hoặc tạo .env mới với:
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-16-char-app-password

# Test email
python3 test_email.py
```

Nếu thấy:
- ✅ "SUCCESS! Email sent successfully!" → OK, deploy lên Railway
- ❌ "FAILED to send email" → Fix email config trước

---

## 📊 KIỂM TRA HOÀN THÀNH

Sau khi làm xong tất cả, test các chức năng:

- [ ] Website load được (không có lỗi 500)
- [ ] Đăng ký tài khoản mới → Nhận email verification
- [ ] Login được
- [ ] Resend verification không bị timeout
- [ ] Forgot password → Nhận email reset
- [ ] Dashboard hiển thị đúng
- [ ] Admin login được

---

## 🐛 NẾU VẪN LỖI

### Lỗi Database
```
✅ Check: MySQL service đang running
✅ Check: DATABASE_URL đã được set
✅ Check: Database đã có tables (chạy lại bước 5.2)
```

### Lỗi Email (vẫn timeout)
```
✅ Check: MAIL_PASSWORD là App Password 16 ký tự
✅ Check: Không có khoảng trắng trong password
✅ Check: 2-Step Verification đã bật
✅ Test local với: python3 test_email.py
```

### Lỗi 500
```
✅ Xem Logs trên Railway
✅ Check tất cả biến môi trường đã đủ
✅ Thử redeploy: git push --force (sau khi backup)
```

---

## 📞 CONTACT

Nếu stuck, check:
1. Railway Logs → xem lỗi gì
2. Railway Variables → đảm bảo đã set đủ
3. MySQL service → đảm bảo đang running
4. Test email local trước

---

**Version:** 1.0  
**Updated:** Oct 21, 2025

