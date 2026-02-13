#!/usr/bin/env python3
"""
Simplified test to get payment URL
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

API_KEY = '9d1be5cb29642744ec425ab74d909bb5'
SITE_KEY = '6Leg2IkcAAAAAMh5olydKqPSz0lI7ysYRrIo_9ea'

print("🚀 Starting simplified test...")

# Setup Chrome
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.binary_location = '/usr/bin/chromium'

driver = webdriver.Chrome(options=options)
driver.get("https://www.orange.tn/recharge-en-ligne")
time.sleep(3)

print("📱 Filling form...")

# Fill phone
driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="55 555 555"]').send_keys("53028939")
phones = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder*="55 555 555"]')
if len(phones) >= 2:
    phones[1].send_keys("53028939")

# Click 20 DT
buttons = driver.find_elements(By.TAG_NAME, 'button')
for btn in buttons:
    if '20' in btn.text:
        driver.execute_script("arguments[0].click();", btn)
        break

time.sleep(1)

# Click Valider
for btn in driver.find_elements(By.TAG_NAME, 'button'):
    if 'Valider' in btn.text:
        driver.execute_script("arguments[0].click();", btn)
        break

time.sleep(2)

print("🔓 Solving CAPTCHA...")

# Submit to 2Captcha
url = f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={SITE_KEY}&pageurl=https://www.orange.tn/recharge-en-ligne&json=1"
resp = requests.get(url).json()
captcha_id = resp['request']
print(f"   ID: {captcha_id}")

# Poll for result
for i in range(30):
    time.sleep(3)
    url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
    resp = requests.get(url).json()
    if resp['status'] == 1:
        token = resp['request']
        print(f"✅ Solved! Token length: {len(token)}")
        break
    print(f"   Attempt {i+1}/30...")
else:
    print("❌ Timeout")
    driver.quit()
    exit(1)

# Inject token
print("💉 Injecting token...")
driver.execute_script(f"""
    document.getElementById('g-recaptcha-response').value = '{token}';
    
    // Enable all buttons
    document.querySelectorAll('button[disabled]').forEach(b => {{
        b.disabled = false;
        b.removeAttribute('disabled');
    }});
""")

time.sleep(2)

# Click Payer
print("💳 Clicking Payer...")
payer = driver.find_element(By.XPATH, '//button[contains(text(), "Payer")]')
driver.execute_script("arguments[0].click();", payer)

# Wait and check URL
print("⏳ Waiting for response...")
time.sleep(5)

url = driver.current_url
print(f"\n📍 Current URL: {url}")

if 'clictopay' in url:
    print(f"✅ SUCCESS! Payment URL: {url}")
else:
    print("⚠️  No redirect yet, checking page...")
    source = driver.page_source
    if 'clictopay' in source:
        import re
        match = re.search(r'https://ipay\.clictopay\.com[^"\'<>\s]*', source)
        if match:
            print(f"✅ Found in source: {match.group()}")
        else:
            print("❌ URL pattern not found")
    else:
        print("❌ No clictopay URL found")

driver.quit()
print("\n✅ Test complete")
