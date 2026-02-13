#!/usr/bin/env python3
"""
Test 2Captcha API directly without Selenium
"""
import time
import requests

API_KEY = "9d1be5cb29642744ec425ab74d909bb5"
SITE_KEY = "6Leg2IkcAAAAAMh5olydKqPSz0lI7ysYRrIo_9ea"
PAGE_URL = "https://www.orange.tn/recharge-en-ligne"

print("🧪 Testing 2Captcha API directly...")
print(f"Site Key: {SITE_KEY}")
print(f"Page URL: {PAGE_URL}")
print()

# 1. Submit CAPTCHA
print("📤 Submitting CAPTCHA to 2Captcha...")
submit_url = f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={SITE_KEY}&pageurl={PAGE_URL}&json=1"
response = requests.get(submit_url, timeout=10)
result = response.json()

print(f"Response: {result}")

if result['status'] != 1:
    print(f"❌ Submission failed!")
    exit(1)

captcha_id = result['request']
print(f"✅ CAPTCHA submitted! ID: {captcha_id}")
print()

# 2. Poll for result
print("⏳ Polling for result...")
for attempt in range(60):
    time.sleep(2)
    
    result_url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
    response = requests.get(result_url, timeout=10)
    result = response.json()
    
    elapsed = attempt * 2
    print(f"[{elapsed}s] Status: {result['status']}, Response: {result}")
    
    if result['status'] == 1:
        token = result['request']
        print()
        print("="*60)
        print("✅ SOLVED!")
        print("="*60)
        print(f"Token length: {len(token)} characters")
        print(f"Token preview: {token[:100]}...")
        print("="*60)
        exit(0)
    
    elif result['status'] == 0:
        error = result.get('request', 'Unknown')
        if error != 'CAPCHA_NOT_READY':
            print(f"❌ Error: {error}")
            exit(1)

print()
print("❌ Timeout after 120 seconds")
