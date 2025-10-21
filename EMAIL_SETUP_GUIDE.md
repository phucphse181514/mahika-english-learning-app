# 📧 RAILWAY EMAIL CONFIGURATION GUIDE

## ✅ ĐÃ FIX

### 1. **Async Email** - HTTP 499 Timeout Fixed
- Email giờ gửi trong background thread
- Response time: 16s → 0.2s
- No more worker timeout

### 2. **Brevo Support** - Production-Ready SMTP
- Config hỗ trợ cả Gmail và Brevo
- MAIL_DEFAULT_SENDER riêng biệt với MAIL_USERNAME
- Professional email service cho production

---

## 🚀 SETUP RAILWAY VARIABLES

### Option 1: Brevo (Recommended for Production)

```bash
MAIL_SERVER=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=[your-brevo-smtp-login]
MAIL_PASSWORD=[your-brevo-smtp-key]
MAIL_DEFAULT_SENDER=[your-verified-email]
```

**Get Brevo credentials:**
1. Sign up: https://www.brevo.com/
2. Verify your sender email
3. Settings → SMTP & API → Generate SMTP key
4. Copy Login and Key

### Option 2: Gmail (For Testing)

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=[your-gmail]
MAIL_PASSWORD=[16-char-app-password]
```

**Get Gmail App Password:**
1. Enable 2-Step Verification
2. Generate App Password at: https://myaccount.google.com/apppasswords

---

## ✅ REQUIRED RAILWAY VARIABLES

```bash
# Database (auto-set by Railway MySQL)
DATABASE_URL=${{MySQL.DATABASE_URL}}

# Security
SECRET_KEY=[generate with: python3 -c "import secrets; print(secrets.token_hex(32))"]

# Email (choose Brevo or Gmail above)
MAIL_SERVER=...
MAIL_PORT=...
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_DEFAULT_SENDER=...  # Important for Brevo!
```

---

## 🧪 TEST

### Local Test:
```bash
# Create .env with your MAIL_* variables
python3 test_email.py
```

### Production Test:
1. Deploy to Railway
2. Register new account
3. Check email (< 2 minutes)

---

## 📊 BENEFITS

| Before | After |
|--------|-------|
| ❌ HTTP 499 timeout | ✅ HTTP 200 success |
| 16s response | 0.2s response |
| Gmail only | Gmail + Brevo |
| Worker killed | Async background |

---

## 🐛 TROUBLESHOOTING

### "Sender not verified" (Brevo)
→ Verify email in Brevo dashboard first

### "Authentication failed"  
→ Check MAIL_USERNAME and MAIL_PASSWORD

### "Connection timeout"
→ Check MAIL_SERVER and MAIL_PORT correct

### Email not received
→ Check spam folder  
→ Check Brevo dashboard statistics

---

**Status:** ✅ Production Ready  
**Version:** 1.0

