# HƯỚNG DẪN CHẠY WEB TRÊN RAILWAY (ĐƠN GIẢN)

## Bước 1: Đẩy code lên Railway

Đảm bảo code đã được push lên GitHub hoặc Railway đã connect với repo của bạn.

## Bước 2: Cài đặt biến môi trường trên Railway

Vào Railway Dashboard → Project của bạn → Variables → thêm các biến sau:

### Bắt buộc:

- `SECRET_KEY` = `your-secret-key-change-this-in-production`
- `DATABASE_URL` = (Railway tự tạo khi bạn thêm MySQL plugin)

### Email (để gửi verification):

- `MAIL_SERVER` = `smtp.gmail.com`
- `MAIL_PORT` = `587`
- `MAIL_USE_TLS` = `True`
- `MAIL_USERNAME` = `your-email@gmail.com`
- `MAIL_PASSWORD` = `your-app-password`

### PayOS:

- `PAYOS_CLIENT_ID` = `your-payos-client-id`
- `PAYOS_API_KEY` = `your-payos-api-key`
- `PAYOS_CHECKSUM_KEY` = `your-payos-checksum-key`
- `PAYOS_RETURN_URL` = `https://mahika-production.up.railway.app/payment/return`
- `PAYOS_CANCEL_URL` = `https://mahika-production.up.railway.app/payment/cancel`

### Download file (Google Drive):

- `DOWNLOAD_FILE_URL` = `https://drive.google.com/uc?export=download&id=YOUR_FILE_ID`
- `DOWNLOAD_FILE_NAME` = `Mahika.exe`

### Payment:

- `PAYMENT_AMOUNT` = `50000` (50,000 VND)

## Bước 3: Tạo bảng trong MySQL (CHỌN 1 CÁCH)

### CÁCH 1: Dùng SQL (ĐƠN GIẢN NHẤT) ⭐

1. Vào Railway Dashboard → chọn MySQL service
2. Click tab "Query" hoặc "Data"
3. Mở file `RAILWAY_SETUP.sql` trong repo này
4. Copy toàn bộ nội dung
5. Paste vào Query Editor và chấm "Run" hoặc "Execute"
6. Xong! (Tạo bảng + admin cùng lúc)

### CÁCH 2: Dùng Railway Shell

1. Vào Railway Dashboard → chọn Web service
2. Tìm icon ">\_" hoặc tab "Deployments" → click "View Logs" → tìm nút "Shell"
3. Trong shell, chạy:

```bash
python scripts/init_db.py
python scripts/create_admin.py --email admin@gmail.com --password Admin@123
```

## Bước 4: Kiểm tra web

Mở: `https://mahika-production.up.railway.app`

Đăng nhập admin:

- Email: `admin@gmail.com`
- Password: `Admin@123`

## Lưu ý

- **ĐỔI MẬT KHẨU ADMIN NGAY** sau khi đăng nhập lần đầu!
- Nếu web lỗi, xem logs tại Railway Dashboard → Web service → Logs
- Nếu không kết nối được DB, kiểm tra `DATABASE_URL` đã tồn tại chưa

## Troubleshooting

### Web không chạy:

- Kiểm tra Railway Logs
- Đảm bảo `gunicorn` có trong `requirements.txt`
- Kiểm tra `DATABASE_URL` đã set chưa

### Không tạo được bảng:

- Dùng CÁCH 1 (SQL) ở trên - đơn giản nhất
- Hoặc kiểm tra MySQL service đã chạy chưa

### Quên mật khẩu admin:

- Chạy lại: `python scripts/create_admin.py --email admin@gmail.com --password NewPassword123`
