"""
Test PayOS signature generation
"""
import hmac
import hashlib

def create_payos_signature(data, checksum_key):
    """Create PayOS signature theo format chính thức"""
    sorted_keys = sorted(data.keys())
    parts = []
    for key in sorted_keys:
        value = str(data[key])
        parts.append(f"{key}={value}")
    
    data_string = "&".join(parts)
    print(f"📝 Data string: {data_string}")
    
    signature = hmac.new(
        checksum_key.encode('utf-8'),
        data_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"🔐 Signature: {signature}")
    return signature

# Test data
test_data = {
    "amount": 5000,
    "cancelUrl": "https://mahika-website.up.railway.app/payment/cancel",
    "description": "Mahika App Premium",  # 19 ký tự - OK!
    "orderCode": 151762612887,
    "returnUrl": "https://mahika-website.up.railway.app/payment/return"
}

print("\n=== TEST PAYOS SIGNATURE ===\n")
print("Test data:")
for key, value in test_data.items():
    print(f"  {key}: {value}")
print()

# Thay YOUR_CHECKSUM_KEY bằng key thực từ PayOS dashboard
checksum_key = "YOUR_CHECKSUM_KEY"
signature = create_payos_signature(test_data, checksum_key)

print("\n✅ Signature generated successfully!")
print(f"\n📋 Copy signature này và test trên PayOS:")
print(signature)
