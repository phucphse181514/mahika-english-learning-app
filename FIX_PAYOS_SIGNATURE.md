# 🔧 FIX: PayOS Signature Error

## ❌ VẤN ĐỀ:

```
PayOS Error: Mã kiểm tra(signature) không hợp lệ
```

## ✅ ĐÃ SỬA:

### 1. **Sửa create_payos_signature() function**

- ✅ Format đúng theo PayOS requirement
- ✅ Logging chi tiết để debug

### 2. **Sửa payment description**

- ❌ Cũ: `"Mahika App - Premium License"` (29 ký tự - quá dài!)
- ✅ Mới: `"Mahika App Premium"` (19 ký tự - OK!)
- ⚠️ PayOS giới hạn: **≤ 25 ký tự**

### 3. **Sửa inconsistency**

- ❌ Cũ: signature_data và payment_data dùng **khác nhau** description
- ✅ Mới: Cả hai dùng **CÙNG** description

---

## 🚀 DEPLOY NGAY:

```bash
git add .
git commit -m "fix: PayOS signature error - update description and signature logic"
git push
```

---

## 🔍 RAILWAY ENV VARIABLES CẦN SET:

```bash
# Payment description - PHẢI ≤ 25 ký tự
PAYMENT_DESCRIPTION=Mahika App Premium

# Hoặc để mặc định (code sẽ dùng "Mahika App Premium")
```

---

## ✅ VERIFY SAU KHI DEPLOY:

### 1. Check Railway Logs:

```bash
railway logs
```

Tìm:

```
📝 [SIGNATURE] Data string: amount=5000&cancelUrl=...&description=Mahika App Premium&orderCode=...&returnUrl=...
🔐 [SIGNATURE] Generated: [signature_hash]
```

### 2. Test Payment:

1. Vào `/payment/checkout`
2. Click "Create Payment"
3. Xem logs có error không
4. Nếu OK → Sẽ redirect đến PayOS payment page

---

## 🐛 NẾU VẪN LỖI:

### Check 1: Description length

```python
len("Mahika App Premium")  # = 19 ký tự ✅
len("Mahika App - Premium License")  # = 29 ký tự ❌
```

### Check 2: Signature data format

Phải theo format chính xác:

```
amount={amount}&cancelUrl={url}&description={desc}&orderCode={code}&returnUrl={url}
```

### Check 3: Checksum key

- Verify `PAYOS_CHECKSUM_KEY` trên Railway
- Copy chính xác từ PayOS dashboard: https://my.payos.vn
- Không có space hoặc newline

### Check 4: Data types

- `amount`: integer (5000, không phải "5000")
- `orderCode`: integer
- URLs: string
- description: string

---

## 📝 TEST LOCAL (Optional):

```bash
# Sửa checksum_key trong file
vim test_payos_signature.py

# Run test
python test_payos_signature.py
```

Output:

```
📝 Data string: amount=5000&cancelUrl=...&description=Mahika App Premium&...
🔐 Signature: [your_signature]
```

Compare signature này với signature PayOS expect.

---

## ✅ SUMMARY:

**Root cause:**

1. Description quá dài (29 > 25 ký tự)
2. signature_data và payment_data dùng khác nhau description

**Fix:**

1. ✅ Rút ngắn description: `"Mahika App Premium"` (19 ký tự)
2. ✅ Dùng cùng description cho cả signature_data và payment_data
3. ✅ Add logging để debug

**Deploy:**

```bash
git add .
git commit -m "fix: PayOS signature - shorten description to 19 chars"
git push
```

---

**Should work now! 🎉**
