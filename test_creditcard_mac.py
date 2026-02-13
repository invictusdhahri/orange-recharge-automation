#!/usr/bin/env python3
"""
Mac-specific test with automatic ChromeDriver management
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Install webdriver-manager if needed
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_WEBDRIVER_MANAGER = True
except ImportError:
    print("⚠️  webdriver-manager not installed!")
    print("Run: pip3 install webdriver-manager")
    exit(1)

from orange_creditcard import OrangeCreditCardRecharge

# Load .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Get credentials
api_key = os.getenv('TWOCAPTCHA_API_KEY')
phone = os.getenv('TEST_PHONE', '53028939')
amount = int(os.getenv('TEST_AMOUNT', '20'))

if not api_key:
    print("❌ No API key found in .env file!")
    print("Create .env file with: TWOCAPTCHA_API_KEY=your_key")
    exit(1)

print("="*60)
print("Orange Credit Card Recharge Test (Mac)")
print("="*60)
print(f"Phone:  {phone}")
print(f"Amount: {amount} DT")
print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
print("="*60)
print()

# Custom recharger with webdriver-manager
class MacOrangeCreditCardRecharge(OrangeCreditCardRecharge):
    """Mac-optimized version with automatic ChromeDriver"""
    
    def _setup_driver(self):
        """Setup Chrome driver with automatic driver management"""
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        # Don't use headless on Mac for testing
        # chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Anti-detection
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use webdriver-manager to handle ChromeDriver
        service = ChromeService(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_cdp_cmd('Network.enable', {})
        
        # Hide webdriver property
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        from selenium.webdriver.support.ui import WebDriverWait
        self.wait = WebDriverWait(self.driver, 20)


# Initialize recharger
print("🚀 Starting recharge with auto CAPTCHA solving...")
print("   (will try free audio first, fallback to 2Captcha)")
print()

recharger = MacOrangeCreditCardRecharge(twocaptcha_api_key=api_key)

result = recharger.recharge(
    phone_number=phone,
    amount=amount,
    captcha_method='auto'
)

# Show result
print()
print("="*60)
print("RESULT")
print("="*60)
print(f"Status: {result['status']}")

if result.get('payment_url'):
    print(f"✅ Payment URL obtained!")
    print(f"   {result['payment_url']}")
elif result.get('message'):
    print(f"Message: {result['message']}")

if result.get('current_url'):
    print(f"Current URL: {result['current_url']}")

print("="*60)
