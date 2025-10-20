# ✅ TẤT CẢ ĐÃ SẴN SÀNG - LÀM THEO 3 BƯỚC SAU

## BƯỚC 1: Push code lên Railway (nếu chưa)

```bash
git add .
git commit -m "Ready for Railway deployment"
git push
```

## BƯỚC 2: Tạo bảng + Admin trong Railway MySQL

### Cách đơn giản nhất (khuyến nghị):

1. Mở Railway: https://railway.app
2. Chọn Project của bạn
3. Click vào **MySQL** service (bên trái)
4. Click tab **"Query"** hoặc **"Data"**
5. Mở file `RAILWAY_SETUP.sql` trong VS Code
6. **Copy toàn bộ** nội dung file SQL
7. **Paste** vào Railway Query Editor
8. Click **"Run"** hoặc **"Execute"**
9. ✅ Xong! (Tạo 2 bảng + tài khoản admin cùng lúc)

### Thông tin admin sau khi tạo:

- Email: `admin@gmail.com`
- Password: `Admin@123`

## BƯỚC 3: Mở web và đăng nhập

1. Vào: `https://mahika-production.up.railway.app`
2. Click "Đăng nhập"
3. Nhập:
   - Email: `admin@gmail.com`
   - Password: `Admin@123`
4. ✅ Thành công!

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **ĐỔI MẬT KHẨU ADMIN** ngay sau khi đăng nhập lần đầu
2. Đảm bảo các **biến môi trường** đã đặt trong Railway:
   - `SECRET_KEY`
   - `DATABASE_URL` (Railway tự tạo)
   - `MAIL_*` (nếu muốn gửi email)
   - `PAYOS_*` (nếu muốn thanh toán)
   - `DOWNLOAD_FILE_URL` (link Google Drive)

---

## 🔧 Nếu gặp lỗi

### Web không mở được:

- Vào Railway → Web service → **Logs** → xem lỗi gì
- Kiểm tra `DATABASE_URL` đã có chưa

### Không tạo được bảng bằng SQL:

- Đảm bảo đã chọn đúng **MySQL service** (không phải Web service)
- Tab "Query" hoặc "Data" phải có ô nhập SQL

### Cần help:

Đọc file `RAILWAY_QUICKSTART.md` có hướng dẫn chi tiết hơn.

---

## 📋 Checklist cuối cùng

- [ ] Code đã push lên Railway
- [ ] MySQL service đã tạo trong Railway
- [ ] Đã chạy file `RAILWAY_SETUP.sql` trong Railway Query
- [ ] Web đã deploy thành công (check Logs không có lỗi fatal)
- [ ] Mở được trang chủ
- [ ] Đăng nhập admin thành công
- [ ] Đã đổi mật khẩu admin

**DONE! 🎉**
